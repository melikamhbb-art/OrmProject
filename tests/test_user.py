import unittest
from orm.database import Database
from models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        """قبل از هر تست، جدول users رو ریست می‌کنیم."""
        Database.execute("DROP TABLE IF EXISTS users;")
        User.create_table()

    def test_create_user(self):
        """تست ساخت یوزر جدید و ذخیره در دیتابیس"""
        u = User(name="Ali", email="ali@example.com")
        u.save()

        # باید id اتوماتیک ساخته بشه
        self.assertIsNotNone(u.id)

        # بررسی صحت ذخیره در دیتابیس
        fetched = User.get(id=u.id)
        self.assertEqual(fetched.email, "ali@example.com")
        self.assertEqual(fetched.name, "Ali")

    def test_update_user(self):
        """تست آپدیت اطلاعات یوزر"""
        u = User(name="Ali", email="ali@example.com")
        u.save()

        # تغییر نام و ذخیره دوباره
        u.name = "Ali Reza"
        u.save()

        # بررسی صحت آپدیت
        fetched = User.get(id=u.id)
        self.assertEqual(fetched.name, "Ali Reza")

    def test_delete_user(self):
        """تست حذف یوزر"""
        u = User(name="X", email="x@example.com")
        u.save()
        uid = u.id

        # حذف از دیتابیس
        u.delete()

        # بررسی اینکه واقعا حذف شده
        self.assertIsNone(User.get(id=uid))

    def test_filter_all_and_by_field(self):
        """تست متد filter برای گرفتن همه و شرط خاص"""
        Database.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?);",
            [(f"User{i}", f"user{i}@ex.com") for i in range(3)]
        )

        # گرفتن همه
        all_users = User.filter()
        self.assertGreaterEqual(len(all_users), 3)

        # گرفتن فقط با شرط email
        one = User.filter(email="user1@ex.com")
        self.assertEqual(len(one), 1)
        self.assertEqual(one[0].name, "User1")

    def test_unique_email_constraint(self):
        """تست یونیک بودن ایمیل"""
        u1 = User(name="First", email="unique@ex.com")
        u1.save()

        # تلاش برای ذخیره یوزر با ایمیل تکراری
        u2 = User(name="Second", email="unique@ex.com")
        with self.assertRaises(Exception):  # باید خطا بده
            u2.save()

    def test_null_name_allowed(self):
        """تست null بودن name"""
        u = User(name=None, email="noname@ex.com")
        u.save()

        fetched = User.get(id=u.id)
        self.assertIsNone(fetched.name)
        self.assertEqual(fetched.email, "noname@ex.com")


if __name__ == "__main__":
    unittest.main()
