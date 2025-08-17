import unittest
from orm.database import Database
from models.comment import Comment
from models.user import User
from models.post import Post

class TestCommentModel(unittest.TestCase):
    def setUp(self):
        # پاک کردن جداول قبلی و ساخت دوباره
        Database.execute("DROP TABLE IF EXISTS comments;")
        Database.execute("DROP TABLE IF EXISTS posts;")
        Database.execute("DROP TABLE IF EXISTS users;")
        User.create_table()
        Post.create_table()
        Comment.create_table()

        # ایجاد یک یوزر و پست نمونه
        self.user = User(name="Ali", email="ali@example.com").save()
        self.post = Post(title="Hello", content="Test Content", user_id=self.user.id).save()

    def test_create_comment(self):
        c = Comment(content="Nice!", user_id=self.user.id, post_id=self.post.id).save()
        self.assertIsNotNone(c.id)
        fetched = Comment.get(id=c.id)
        self.assertEqual(fetched.content, "Nice!")

    def test_update_comment(self):
        c = Comment(content="Old", user_id=self.user.id, post_id=self.post.id).save()
        c.content = "Updated"
        c.save()
        fetched = Comment.get(id=c.id)
        self.assertEqual(fetched.content, "Updated")

    def test_delete_comment(self):
        c = Comment(content="To Delete", user_id=self.user.id, post_id=self.post.id).save()
        cid = c.id
        c.delete()
        self.assertIsNone(Comment.get(id=cid))

    def test_filter_comments(self):
        for i in range(3):
            Comment(content=f"C{i}", user_id=self.user.id, post_id=self.post.id).save()
        all_comments = Comment.filter()
        self.assertGreaterEqual(len(all_comments), 3)
        one = Comment.filter(content="C1")
        self.assertEqual(len(one), 1)
        self.assertEqual(one[0].content, "C1")

if __name__ == "__main__":
    unittest.main()
