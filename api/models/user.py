"""FIle contains model for user"""

from werkzeug.security import generate_password_hash

from api.helpers.responses import (
    duplicate_email,
    duplicate_user_name,
    duplicate_phone_number,
)
from database.db import Database


class User:
    """class defines the user data structure"""

    def __init__(self, **kwargs):
        self.db = Database()

    def insert_user(self, **kwargs):
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        other_names = kwargs["other_names"]
        email = kwargs["email"]
        phone_number = kwargs["phone_number"]
        user_name = kwargs.get("user_name")
        user_password = generate_password_hash(kwargs["password"])

        # is_admin = kwargs.get('is_admin')
        sql = (
            "INSERT INTO users ("
            "first_name,"
            "last_name, "
            "other_names,"
            "email, phone_number, user_name,"
            "user_password )VALUES ("
            f"'{first_name}', '{last_name}','{other_names}',"
            f"'{email}', '{phone_number}','{user_name}',"
            f"'{user_password}') returning "
            "id,first_name as firstname,"
            "last_name as lastname, "
            "other_names as othernames,"
            "email, phone_number as phoneNumber, "
            "user_name as userName, "
            "registered_on as registered"
        )
        self.db.cursor.execute(sql)
        new_user = self.db.cursor.fetchone()
        return new_user

    def check_if_user_exists(self, user_name, email, phone_number):
        """user_name and email must be unique"""
        user_exists_sql = (
            "SELECT user_name,email, phone_number from users where "
            f"user_name ='{user_name}' OR email='{email}' OR"
            f" phone_number='{phone_number}';"
        )
        self.db.cursor.execute(user_exists_sql)
        user_exists = self.db.cursor.fetchone()
        error = {}

        if user_exists and user_exists.get("user_name") == user_name:
            error["username"] = duplicate_user_name

        if user_exists and user_exists.get("email") == email:
            error["email"] = duplicate_email

        if user_exists and user_exists.get("phone_number") == phone_number:
            error["phoneNumber"] = duplicate_phone_number
        return error
