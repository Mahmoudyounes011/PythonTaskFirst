from .db import get_db
import mysql.connector
from datetime import datetime

class Todo:
    @staticmethod
    def create(data):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                INSERT INTO todos 
                (title, description, completed, user_id, created_at)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                data['title'],
                data.get('description', ''),
                data.get('completed'),
                data['user_id'],
                datetime.now()
            ))
            todo_id = cursor.lastrowid
            conn.commit()
            
            cursor.execute('''
                SELECT id, title, description, completed, created_at 
                FROM todos 
                WHERE id = %s
            ''', (todo_id,))
            new_todo = cursor.fetchone()
            
            return new_todo  
        
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT * FROM todos 
                WHERE user_id = %s
                ORDER BY created_at DESC
            ''', (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(todo_id, user_id, data):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                UPDATE todos SET
                title = %s,
                description = %s,
                completed = %s
                WHERE id = %s AND user_id = %s
            ''', (
                data.get('title'),
                data.get('description'),
                data.get('completed'),
                todo_id,
                user_id
            ))
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()