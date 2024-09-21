
import uuid

class User:
    def __init__(self, user):
        self.id = str(uuid.uuid4())
        self.name = user['name']
        self.age = user['age']
        self.allergies = user['allergies']
        self.conditions = user['conditions']

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        user = User(user)
        self.users[user.id] = user
        return user

    def get_all_users(self):
        return [vars(user) for user in self.users.values()]