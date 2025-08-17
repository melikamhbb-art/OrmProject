import unittest
from orm.database import Database
from models.user import User
from models.post import Post


class TestPostModel(unittest.TestCase):
    def setUp(self):
        """
        قبل از هر تست:
        - جدول posts و users پاک و دوباره ساخته می‌شن
        """
        Database.execute("DROP TABLE IF EXISTS posts;")
        Database.execute("DROP TABLE IF EXISTS users;")
        User.create_table()
        Post.create_table()

    def tearDown(self):
        """بعد از هر تست تمیزکاری"""
        Database.execute("DROP TABLE IF EXISTS posts;")
        Database.execute("DROP TABLE IF EXISTS users;")

    def test_create_post(self):
        """تست ایجاد یک پست جدید"""
        user = User(name="Ali", email="ali@example.com")
        user.save()

        post = Post(user_id=user.id, title="Hello", content="This is my first post!")
        post.save()

        self.assertIsNotNone(post.id)

        fetched = Post.get(id=post.id)
        self.assertEqual(fetched.title, "Hello")
        self.assertEqual(fetched.user_id, user.id)

    def test_update_post(self):
        """تست آپدیت پست"""
        user = User(name="Sara", email="sara@example.com")
        user.save()

        post = Post(user_id=user.id, title="Old Title", content="Old content")
        post.save()

        post.title = "New Title"
        post.save()

        fetched = Post.get(id=post.id)
        self.assertEqual(fetched.title, "New Title")

    def test_delete_post(self):
        """تست حذف پست"""
        user = User(name="Test", email="test@example.com")
        user.save()

        post = Post(user_id=user.id, title="Temp", content="Temp post")
        post.save()
        pid = post.id

        post.delete()

        self.assertIsNone(Post.get(id=pid))

    def test_filter_posts_by_user(self):
        """تست فیلتر پست‌ها بر اساس user_id"""
        user = User(name="Ali", email="ali@ex.com")
        user.save()

        # سه پست برای علی
        for i in range(3):
            Post(user_id=user.id, title=f"T{i}", content="...").save()

        posts = Post.filter(user_id=user.id)
        self.assertEqual(len(posts), 3)

    def test_null_content_allowed(self):
        """تست اینکه content می‌تونه null باشه"""
        user = User(name="X", email="x@ex.com")
        user.save()

        post = Post(user_id=user.id, title="No Content", content=None)
        post.save()

        fetched = Post.get(id=post.id)
        self.assertIsNone(fetched.content)


if __name__ == "__main__":
    unittest.main()
