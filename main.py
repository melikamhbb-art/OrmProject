
from models.user import User

def demo():
    User.create_table()

    # Create
    u = User(name="Melika", email="melika@example.com").save()
    print("Created:", u.id, u.name, u.email)

    # Read
    got = User.get(email="melika@example.com")
    print("Read:", got.id, got.name, got.email)

    # Update
    got.name = "MELIKA"
    got.save()
    print("Updated:", got.id, got.name, got.email)

    # List
    for usr in User.all():
        print("Row:", usr.id, usr.name, usr.email)

    # Delete
    got.delete()
    print("Deleted:", got.id)

if __name__ == "__main__":
    demo()
