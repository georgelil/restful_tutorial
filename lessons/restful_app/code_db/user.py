import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """
        checks for username in database

        Parameters
        ----------
        username : str
           username to look for
        Returns
        --------
        User : User or None
            returns user object if found, else None
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SElECT * FROM users WHERE username=?'
        results = cursor.execute(query, (username,))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SElECT * FROM users WHERE id=?'
        results = cursor.execute(query, (_id,))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='field required')
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='field required')

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'user {} already exists'.format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'user: {} created successfully'.format(data['username'])}, 201
