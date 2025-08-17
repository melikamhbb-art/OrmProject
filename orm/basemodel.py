
from orm.database import Database
from orm.fields import Field, IntegerField, CharField, BooleanField

class ValidationError(Exception):
    pass

class BaseModel:
    table_name = None

    # ----- Table creation -----
    @classmethod
    def _iter_fields(cls):
        for name, field in cls.__dict__.items():
            if isinstance(field, Field):
                field.name = name
                yield name, field

    @classmethod
    def create_table(cls):
        columns = []
        for _, field in cls._iter_fields():
            columns.append(field.get_sql())
        query = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({', '.join(columns)});"
        Database.execute(query)

    # ----- Instance init -----
    def __init__(self, **kwargs):
        for name, field in self.__class__._iter_fields():
            value = kwargs.get(name, field.default() if callable(field.default) else field.default)
            setattr(self, name, value)

    # ----- Validation -----
    def _validate(self):
        for name, field in self.__class__._iter_fields():
            value = getattr(self, name)

            # Nullability
            if value is None and not field.null and not field.primary_key:
                raise ValidationError(f"Field '{name}' cannot be NULL")

            if value is None:
                continue

            # Basic type checks
            if isinstance(field, IntegerField) and not isinstance(value, int):
                raise ValidationError(f"Field '{name}' must be int")
            if isinstance(field, CharField) and not isinstance(value, str):
                raise ValidationError(f"Field '{name}' must be str")
            if isinstance(field, BooleanField) and not isinstance(value, (bool, int)):
                raise ValidationError(f"Field '{name}' must be bool or 0/1")

            # Max length check for CharField
            if isinstance(field, CharField) and field.max_length is not None:
                if len(value) > field.max_length:
                    raise ValidationError(f"Field '{name}' exceeds max_length={field.max_length}")

    # ----- Persistence -----
    def save(self):
        self._validate()

        fields = []
        values = []
        placeholders = []

        pk_name, pk_value = None, None
        for name, field in self.__class__._iter_fields():
            if field.primary_key:
                pk_name = name
                pk_value = getattr(self, name)
                continue  # handle separately for INSERT
            fields.append(name)
            values.append(getattr(self, name))
            placeholders.append("?")

        # Insert when PK not set or record doesn't exist
        do_insert = pk_value is None
        if not do_insert and pk_name:
            existing = self.get(**{pk_name: pk_value})
            do_insert = existing is None

        if do_insert:
            # INSERT (omit PK so SQLite assigns rowid if INTEGER PRIMARY KEY)
            query = f"INSERT INTO {self.table_name} ({', '.join(fields)}) VALUES ({', '.join(placeholders)});"
            cur = Database.execute(query, values)
            # set PK after insert if it exists and was None
            if pk_name is not None and pk_value is None:
                try:
                    setattr(self, pk_name, cur.lastrowid)
                except Exception:
                    pass
        else:
            # UPDATE (set all fields, filter by PK)
            set_clause = ", ".join([f"{f}=?" for f in fields])
            params = [getattr(self, f) for f in fields]
            params.append(pk_value)
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {pk_name}=?;"
            Database.execute(query, params)
        return self

    @classmethod
    def get(cls, **kwargs):
        if not kwargs:
            raise ValueError("get() requires at least one condition")
        condition = " AND ".join([f"{k}=?" for k in kwargs])
        query = f"SELECT * FROM {cls.table_name} WHERE {condition} LIMIT 1;"
        row = Database.execute(query, list(kwargs.values())).fetchone()
        return cls(**dict(row)) if row else None

    @classmethod
    def filter(cls, **kwargs):
        if not kwargs:
            query = f"SELECT * FROM {cls.table_name};"
            rows = Database.execute(query).fetchall()
        else:
            condition = " AND ".join([f"{k}=?" for k in kwargs])
            query = f"SELECT * FROM {cls.table_name} WHERE {condition};"
            rows = Database.execute(query, list(kwargs.values())).fetchall()
        return [cls(**dict(r)) for r in rows]

    def delete(self):
        # Delete by primary key
        pk_name, pk_value = None, None
        for name, field in self.__class__._iter_fields():
            if field.primary_key:
                pk_name = name
                pk_value = getattr(self, name)
                break
        if pk_value is None:
            raise ValidationError("Cannot delete without primary key set")
        Database.execute(f"DELETE FROM {self.table_name} WHERE {pk_name}=?;", [pk_value])

    # Quality-of-life helpers
    @classmethod
    def all(cls):
        return cls.filter()
