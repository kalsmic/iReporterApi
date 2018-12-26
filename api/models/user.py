"""FIle contains model for user"""
from datetime import date

from werkzeug.security import generate_password_hash, check_password_hash

from api.helpers.auth_token import encode_token, get_current_identity
from api.helpers.responses import duplicate_email, duplicate_user_name

users = []
user_id = 1


class User:
    """class defines the user data structure"""

    def __init__(self, **kwargs):
        global user_id
        self.user_id = user_id
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.other_names = kwargs["other_names"]
        self.email = kwargs["email"]
        self.phone_number = kwargs["phone_number"]
        self.password = generate_password_hash(kwargs["password"])
        self.user_name = kwargs["user_name"]
        self.registered = date.today()
        self.is_admin = 0
        user_id += 1

    def get_user_details(self):
        return {
            "id": self.user_id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "othernames": self.other_names,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "username": self.user_name,
            "registered": self.registered,
            "isAdmin": self.is_admin,
        }


def check_if_user_exists(user_name, email):
    """user_name and email must be unique"""
    for user in users:
        if user.email == email:
            return duplicate_email
        elif user.user_name == user_name:
            return duplicate_user_name


def is_valid_credentials(user_name, password):
    for user in users:
        if user.user_name == user_name and check_password_hash(
            user.password, password
        ):
            if user.is_admin == 1:
                return encode_token(user.user_id, 1)
            return encode_token(user.user_id, 0)


# create an adnin user since there's no option for signing him up
admin = User(
    first_name="Administrator",
    last_name="admin",
    email="admin@ireporter.com",
    phone_number="07731235678",
    password="Password123",
    user_name="admin",
    other_names="",
)
admin.is_admin = 1
users.append(admin)


def check_if_is_admin():
    user_id = get_current_identity()
    for user in users:
        if user.user_id == user_id and user.user_name == "admin":
            return True
    return False


user_object_by_id_dict = {user.user_id: user for user in users}
email_object_dictionary = {user.email: user for user in users}
user_name_object_dictionary = {user.user_name: user for user in users}
