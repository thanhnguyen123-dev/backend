
import uuid

class User:
    current_id = 1

    def __init__(self, user):
        self.id = User.current_id  # Assign the current ID
        User.current_id += 1 
        self.name = user['name']
        self.age = user['age']
        self.allergies = user['allergies']
        self.conditions = user['conditions']
        self.prescriptions = []
    
    def to_dict(self):
        """Convert the User object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'allergies': self.allergies,
            'conditions': self.conditions,
            'prescriptions': self.prescriptions,
        }

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        user = User(user)
        self.users[user.id] = user
        return user

    def get_all_users(self):
        return [vars(user) for user in self.users.values()]
    
    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        else:
            return f"User id {user_id} not found."
        
    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if user:
            # Update user information
            user.name = data.get('name', user.name)
            user.age = data.get('age', user.age)
            user.allergies = data.get('allergies', user.allergies)
            user.conditions = data.get('conditions', user.conditions)
            user.prescriptions = data.get('prescriptions', user.prescriptions)
            return user
        else:
            raise ValueError("User not found")
    
    def update_prescriptions(self, user_id, prescriptions):
        if user_id in self.users:
            self.users[user_id].prescriptions.extend(prescriptions)
            return True
        return False
