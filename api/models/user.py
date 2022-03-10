"""FIle contains model for user"""

from werkzeug.security import generate_password_hash, check_password_hash

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

    def get_user_details(self, user_id):
        user_sql = (
            "SELECT user_name as username, first_name as firstname, "
            " last_name as lastname, other_names as othernames,"
            "email, phone_number, is_admin FROM users "
            f"WHERE id='{user_id}';"
        )
        self.db.cursor.execute(user_sql)
        user_details = self.db.cursor.fetchone()
        return user_details

    def is_valid_credentials(self, user_name, user_password):
        sql = (
            "SELECT id,user_name ,user_password, is_admin FROM users where user_name="
            f"'{user_name}';"
        )
        self.db.cursor.execute(sql)

        user_db_details = self.db.cursor.fetchone()

        if (
            user_db_details
            and user_db_details.get("user_name") == user_name
            and check_password_hash(
                user_db_details.get("user_password"), user_password
            )
        ):

            return {
                "user_id": user_db_details.get("id")
            }
        return None

    def add_token_in_db(self, token, user_id):
        sql = (
            "INSERT INTO users_auth (token,user_id) "
            f"VALUES('{token}', '{user_id}');"
        )
        self.db.cursor.execute(sql)

    def get_no_of_users(self):
        sql = (
            "SELECT count(*) as users FROM users "
            "WHERE user_name != 'admin';"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def get_users(self):
        sql = (
            "SELECT first_name, last_name, other_names, "
            "email, phone_number, user_name, "
            "registered_on FROM users "
            "WHERE user_name != 'admin';"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()

    def get_user_mail_and_user_name(self,user_id):
        sql = (
            "SELECT email, user_name FROM users WHERE"
            f" id='{user_id}';"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()
