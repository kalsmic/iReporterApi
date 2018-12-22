"""FIle contains model for user"""
import re
from datetime import date

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from api.helpers import encode_token,get_current_identity,decode_token

users = []

class User:
    """class defines the user data structure"""
    Id = 0

    def __init__(self, **kwargs):
        self.id = User.Id + 1
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = kwargs['othernames']
        self.email = kwargs['email']
        self.phoneNumber = kwargs['phoneNumber']
        self.password = kwargs['password']
        self.username = kwargs["username"]
        self.registered = date.today()
        self.isAdmin = 0

    def get_user_details(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "othernames": self.othernames,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "username": self.username,
            "registered": self.registered,
            "isAdmin": self.isAdmin
        }

    def set_user_id(self, value):
        # Assign a valid user object an id
        self.id = value

    def validate_input_data(self):
        error = None
        if not self.firstname or not self.lastname or not self.firstname.isalpha() or not self.lastname.isalpha():
            # checks if name fields  do not contains any space,or is empty
            error = "Name fields cannot be empty or contain any space or number character"

        elif self.othernames and not self.othernames.isalpha():
            # other name is optional but must be contain only letters if provided
            error = "Name must contain letter characters only"

        elif not self.username or self.username.isspace():
            # email must not contain any space or be empty
            error = "username cannot be empty or contain any a space in it"

        elif not self.email or not re.match('[^@]+@[^@]+\.[^@]+', self.email):
            # email must be of valid pattern
            error = "please provide a valid email"

        elif not self.phoneNumber:
            error = "phoneNumber cannot be empty"

        elif not len(self.phoneNumber) == 10 or not self.phoneNumber.isdigit():
            error = "phoneNumber must be a string of ten numbers only"

        elif self.is_not_valid_password():
            error = self.is_not_valid_password()
        return error

    def is_not_valid_password(self):
        """test password strength"""
        error = None

        if len(self.password) < 8:
            error = "Password Must contain a Minimum 8 characters."

        elif not re.search("[A-Z]", self.password):
            error = "Password must contain atleast one upper case letter"
        elif not re.search("[0-9]", self.password):
            error = "Password must contain atleast one number"
        elif not re.search("[a-z]", self.password):
            error = "Password must contain atleast lower case letter"
        return error




def check_if_user_exists(new_user_object):
    """username and email must be unique"""
    for user in users:
        if user.email == new_user_object.email:
            return "Email address exists"
        elif user.username == new_user_object.username:
            return "Username already taken"


def sign_up_user(user_obj):
    """create new user account"""
    # hash user's password
    user_obj.password = generate_password_hash(user_obj.password, method='sha256')
    # assign user id
    User.Id += 1

    # Add user object to the list
    users.append(user_obj)


def is_valid_credentials(username, password):
    for user in users:
        if user.username == username and check_password_hash(user.password, password):
            if user.isAdmin==1:
                return encode_token(user.id,1)
            return encode_token(user.id,0)


# create an adnin user since there's no option for signing him up
admin = User(firstname='Administrator',lastname='admin',email='admin@ireporter.com',phoneNumber='07731235678',
             password='Password123', username='admin',othernames="")
admin.isAdmin =  1
sign_up_user(admin)

user1 = User(firstname='userOne',lastname='userone',email='userOne@ireporter.com',phoneNumber='07731235678',
             password='Password123', username='user1',othernames="")
sign_up_user(user1)
user2 = User(firstname='userTwo',lastname='usertwo',email='userTwo@ireporter.com',phoneNumber='07731235678',
             password='Password123', username='user2',othernames="")
sign_up_user(user2)

def check_if_is_admin():
    user_id =get_current_identity()
    for user in users:
        if user.id == user_id and  user.username =="admin":
            return  True
    return False


user_object_by_id_dict = {user.id: user for user in users}
email_object_dictionary = {user.email: user for user in users}
username_object_dictionary = {user.username: user for user in users}
