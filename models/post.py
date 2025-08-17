from orm.basemodel import BaseModel
from orm.fields import IntegerField, CharField

class Post(BaseModel):
    table_name = "posts"

    id = IntegerField(primary_key=True)
    user_id = IntegerField(null=False)  # ⚡ filter بر اساس کاربر ارور نده
    title = CharField(max_length=255)
    content = CharField(max_length=1024, null=True)
