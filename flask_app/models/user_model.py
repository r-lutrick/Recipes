from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import DATABASE, EMAIL_REGEX, PASSWORD_REGEX
from flask import flash


# User Model
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
            SELECT *
            FROM users;
        """
        response = MySQLConnection(DATABASE).query_db(query)
        output = []
        if response:
            for row in response:
                output.append(cls(row))
        return output

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE users.id = %(id)s;
        """
        response = MySQLConnection(DATABASE).query_db(query, data)
        if response:
            return cls(response[0])
        return False

    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s;
        """
        response = MySQLConnection(DATABASE).query_db(query, data)
        if response:
            return cls(response[0])
        return False

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUE (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        return MySQLConnection(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be 2 or more characters", "reg")
            is_valid = False
        elif not str.isalpha(data['first_name']):
            flash("First name can only contain letters", "reg")
            is_valid = False

        if len(data['last_name']) < 2:
            flash("Last name must be 2 or more characters", "reg")
            is_valid = False
        elif not str.isalpha(data['last_name']):
            flash("Last name can only contain letters", "reg")
            is_valid = False

        if len(data['email']) <= 2:
            flash("E-mail must be 2 or more characters", "reg")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address, ex: email@email.com", "reg")
            is_valid = False
        else:
            stuff = {
                'email': data['email']
            }
            potential_user = User.get_by_email(stuff)
            if potential_user:
                flash("email exists, please login", "reg")
                is_valid = False

        if len(data['password']) <= 8:
            flash("Password must be 8 or more characters", "reg")
            is_valid = False
        elif not PASSWORD_REGEX.match(data['password']):
            flash(
                "Password must have at least 1 number and 1 uppercase letter", "reg")
            is_valid = False

        return is_valid
