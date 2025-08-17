
class Field:
    def __init__(self, field_type, primary_key=False, unique=False, null=False, default=None, max_length=None):
        self.field_type = field_type  # SQL type string (e.g., INTEGER, TEXT, VARCHAR(255))
        self.primary_key = primary_key
        self.unique = unique
        self.null = null
        self.default = default
        self.max_length = max_length
        self.name = None  # set later by BaseModel

    def get_sql(self):
        # Build the SQL definition for this field
        sql = f"{self.name} {self.field_type}"
        if self.primary_key:
            sql += " PRIMARY KEY"
        if self.unique:
            sql += " UNIQUE"
        # Avoid adding NOT NULL when explicitly nullable or when it's primary key (PRIMARY KEY is already NOT NULL in SQLite)
        if not self.null and not self.primary_key:
            sql += " NOT NULL"
        if self.default is not None and not callable(self.default):
            if isinstance(self.default, str):
                sql += f" DEFAULT '{self.default}'"
            elif isinstance(self.default, bool):
                sql += f" DEFAULT {1 if self.default else 0}"
            else:
                sql += f" DEFAULT {self.default}"
        return sql


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)


class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(f"VARCHAR({max_length})", max_length=max_length, **kwargs)


class BooleanField(Field):
    def __init__(self, **kwargs):
        # SQLite doesn't have a native BOOLEAN type; it stores as INTEGER 0/1
        super().__init__("INTEGER", **kwargs)
