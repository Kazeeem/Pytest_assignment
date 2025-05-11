# built-in libraries
from uuid import UUID
# Installed libraries
from passlib.hash import bcrypt
# code libraries/folders
from database import users
from schemas.user import User, UserCreate, UserUpdate, ChangePassword, UserLogin


class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        user = users.get(str(user_id))
        if not user:
            return None
        return user

    @staticmethod
    def create_user(self, user_in: UserCreate):
        user = User(
            id=str(UUID(int=len(users) + 1)),
            **user_in.model_dump(exclude={'password'}),  # Exclude the plain password
            password=self.hash_password(user_in.password)  # Set the hashed password
        )
        users[user.id] = user
        return user

    @staticmethod
    def update_user(user_id: UUID, user_in: UserUpdate):
        user = users.get(str(user_id))
        if not user:
            return None

        user.name = user_in.name
        user.email = user_in.email
        user.username = user_in.username
        user.phone = user_in.phone
        user.age = user_in.age
        return user

    @staticmethod
    def delete_user(user_id: UUID):
        user = users.get(str(user_id))
        if not user:
            return None

        del users[user.id]
        return True

    @staticmethod
    def change_password(self, user_id: UUID, password: ChangePassword):
        user = users.get(str(user_id))
        if not user:
            return None

        if not self.verify_password(password.new_password, user.password):
            raise None

        if password.new_password != password.confirm_new_password:
            raise None

        user.password = self.hash_password(password.new_password)
        return user

    @staticmethod
    def login(self, user_in: UserLogin):
        user = users.get(user_in.username)

        if not user:
            return None

        if not self.verify_password(user_in.password, user.password):
            raise None

        return user

    @staticmethod
    def hash_password(plain_text_password: str) -> str:
        return bcrypt.hash(plain_text_password)

    @staticmethod
    def verify_password(plain_text_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_text_password, hashed_password)


user_service = UserService()
