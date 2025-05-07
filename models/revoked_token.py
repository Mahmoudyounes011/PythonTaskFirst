from .db import get_db

class RevokedToken:
    @staticmethod
    def add(jti):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO revoked_tokens (jti) VALUES (%s)', (jti,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def is_jti_blacklisted(jti):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM revoked_tokens WHERE jti = %s', (jti,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()