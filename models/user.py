from .db import get_db
import bcrypt
import mysql.connector

class User:
    @staticmethod
    def create(user_data):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            hashed_pw = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('''
                INSERT INTO users 
                (first_name, last_name, email, phone_number, password, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                user_data['first_name'],
                user_data['last_name'],
                user_data['email'],
                user_data['phone_number'],
                hashed_pw,
                user_data['address']
            ))
            
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_by_email(email):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verify_password(stored_pw, input_pw):
        return bcrypt.checkpw(input_pw.encode('utf-8'), stored_pw.encode('utf-8'))
    
    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            if not user:
                raise ValueError("User not found")
            return user
        except mysql.connector.Error as err:
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()