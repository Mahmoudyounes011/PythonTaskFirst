from .db import get_db
import mysql.connector

class Project:
    @staticmethod
    def create(project_data, user):
        if not user['is_admin']:
            raise PermissionError("Only admins can create projects")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('''
                INSERT INTO projects (name, description, created_by)
                VALUES (%s, %s, %s)
            ''', (
                project_data['name'],
                project_data.get('description', ''),
                user['id']
            ))
            project_id = cursor.lastrowid
            conn.commit()

            cursor.execute('''
                SELECT 
                    p.id AS project_id,
                    p.name,
                    p.description,
                    p.created_at,
                    u.first_name AS created_by_first_name,
                    u.last_name AS created_by_last_name
                FROM projects p
                JOIN users u ON p.created_by = u.id
                WHERE p.id = %s
            ''', (project_id,))
            
            project_with_creator = cursor.fetchone()
            return project_with_creator

        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def update(project_id, project_data, user):
        if not user['is_admin']:
            raise PermissionError("Only admins can update projects")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:

            cursor.execute('SELECT * FROM projects WHERE id = %s AND created_by = %s', (project_id, user['id']))
            if not cursor.fetchone():
                raise PermissionError("Not authorized to update this project")

            cursor.execute('''
                UPDATE projects
                SET name = %s, description = %s
                WHERE id = %s
            ''', (
                project_data['name'],
                project_data.get('description', ''),
                project_id
            ))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(project_id, user):
        if not user['is_admin']:
            raise PermissionError("Only admins can delete projects")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:

            cursor.execute('SELECT * FROM projects WHERE id = %s AND created_by = %s', (project_id, user['id']))
            if not cursor.fetchone():
                raise PermissionError("Not authorized to delete this project")

            cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            raise Exception(f"Database error: {err.msg}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(project_id, user):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            if user['is_admin']:
                cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
            else:

                cursor.execute('''
                    SELECT p.*
                    FROM projects p
                    JOIN tasks t ON t.project_id = p.id
                    WHERE p.id = %s AND t.assigned_to = %s
                    LIMIT 1
                ''', (project_id, user['id']))
            project = cursor.fetchone()
            if not project:
                raise ValueError("Project not found or access denied")
            return project
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_by_name(name):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM projects WHERE name LIKE %s', (f'%{name}%',))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
