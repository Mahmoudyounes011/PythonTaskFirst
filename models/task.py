from .db import get_db
import mysql.connector

class Task:
    @staticmethod
    def create(task_data, user):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            
            cursor.execute('''
                SELECT created_by FROM projects WHERE id = %s
            ''', (task_data['project_id'],))
            project = cursor.fetchone()

            if not project or project['created_by'] != user['id']:
                raise PermissionError("Only the project creator can create tasks")

            cursor.execute('''
                INSERT INTO tasks (title, description, status, due_date, project_id, created_by, assigned_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                task_data['title'],
                task_data.get('description', ''),
                task_data.get('status', 'pending'),
                task_data.get('due_date'),
                task_data['project_id'],
                user['id'],
                task_data['assigned_to']
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
    def update_status(task_id, user_id, new_status):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT assigned_to FROM tasks WHERE id = %s', (task_id,))
            task = cursor.fetchone()
            if not task or task['assigned_to'] != user_id:
                raise PermissionError("Only the assigned user can update the task status")

            cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (new_status, task_id))
            conn.commit()

        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_due_date(task_id, user_id, new_due_date):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT created_by FROM tasks WHERE id = %s', (task_id,))
            task = cursor.fetchone()
            if not task or task['created_by'] != user_id:
                raise PermissionError("Only the project creator can update due date")

            cursor.execute('UPDATE tasks SET due_date = %s WHERE id = %s', (new_due_date, task_id))
            conn.commit()

        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(task_id, user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT created_by FROM tasks WHERE id = %s', (task_id,))
            task = cursor.fetchone()
            if not task or task['created_by'] != user_id:
                raise PermissionError("Only the project creator can delete tasks")

            cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
            conn.commit()

        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def filter_tasks(filters):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            query = 'SELECT * FROM tasks WHERE 1=1'
            params = []

            if 'status' in filters:
                query += ' AND status = %s'
                params.append(filters['status'])

            if 'due_date' in filters:
                query += ' AND DATE(due_date) = %s'
                params.append(filters['due_date'])

            if 'project_id' in filters:
                query += ' AND project_id = %s'
                params.append(filters['project_id'])

            if 'assigned_to' in filters:
                query += ' AND assigned_to = %s'
                params.append(filters['assigned_to'])

            if 'title' in filters:
                query += ' AND title LIKE %s'
                params.append(f"%{filters['title']}%")

            if 'description' in filters:
                query += ' AND description LIKE %s'
                params.append(f"%{filters['description']}%")

            cursor.execute(query, tuple(params))
            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()
