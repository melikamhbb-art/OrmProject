from orm.basemodel import BaseModel
from orm.fields import IntegerField, CharField

class Comment(BaseModel):
    table_name = "comments"

    id = IntegerField(primary_key=True)
    post_id = IntegerField(null=False)  # ⚡  فیلتر بر اساس پست ارور نده
    user_id = IntegerField(null=False)  # ⚡ اضافه 
    content = CharField(max_length=512)
