from .db import get_db
import mysql.connector

class Student:
    @staticmethod
    def create(data):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                INSERT INTO students (first_name, last_name, age, specialization)
                VALUES (%s, %s, %s, %s)
            ''', (data['first_name'], data['last_name'], data['age'], data['specialization']))
            
            conn.commit()
            student_id = cursor.lastrowid
            return Student.get_by_id(student_id)
            
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM students')
            return cursor.fetchall()
        except mysql.connector.Error as err:
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(student_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
            student = cursor.fetchone()
            if not student:
                raise ValueError("Student not found")
            return student
        except mysql.connector.Error as err:
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()