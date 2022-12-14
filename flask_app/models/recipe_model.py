from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import DATABASE, EMAIL_REGEX, PASSWORD_REGEX
from flask import flash
from flask_app.models import user_model


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
            SELECT *
            FROM recipes
            JOIN users
            ON recipes.user_id = users.id
        """
        response = MySQLConnection(DATABASE).query_db(query)
        output = []
        if response:
            for row in response:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.creator = this_user
                output.append(this_recipe)
            return output

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT *
            From recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id=%(id)s;
        """
        response = MySQLConnection(DATABASE).query_db(query, data)
        output = []
        if response:
            for row in response:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.creator = this_user
                output.append(this_recipe)
            return output[0]
        return False

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (name, description, instruction, under, created_at, user_id)
            VALUE (%(name)s,%(description)s,%(instruction)s,%(under)s, %(created_at)s, %(user_id)s);
        """
        return MySQLConnection(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes
            SET
                name=%(name)s,
                description=%(description)s,
                instruction=%(instruction)s,
                under=%(under)s,
                created_at=%(created_at)s,
                user_id=%(user_id)s
            WHERE id=%(id)s
        """
        return MySQLConnection(DATABASE).query_db(query, data)

    @classmethod
    def remove(cls, data):
        query = """
            DELETE
            FROM recipes
            WHERE id=%(id)s
        """
        return MySQLConnection(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 3:
            flash("Name must be 3 or more characters", "rec")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be 3 or more characters", "rec")
            is_valid = False
        if len(data['instruction']) < 3:
            flash("instructions must be 3 or more characters", "rec")
            is_valid = False

        return is_valid
