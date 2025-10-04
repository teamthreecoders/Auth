from re import match


class UserCRUD:
    # Create a new user
    @staticmethod
    def create_user(db_conn,*,id:str,email: str, phone: str, hashed_password: str,role:str):
        sql = """
        INSERT INTO users (id,email, phone, hashed_password,role)
        VALUES (%s,%s, %s, %s,%s)
        """
        db_conn.cursor.execute(sql, (id,email, phone, hashed_password,role))
        rowCnt = db_conn.cursor.rowcount
        db_conn.commit()
        db_conn.commit()
        return rowCnt

    # Get user by email
    @staticmethod
    def get_user_by_email(db_conn,*, email: str):
        sql = "SELECT ID,email,phone,hashed_password,is_verified,is_2fa_enabled,role FROM users WHERE email = %s"
        db_conn.cursor.execute(sql, (email,))
        return db_conn.cursor.fetchone()
    
    @staticmethod
    def get_user_by_phone(db_conn,*, phone: str):
        sql = "SELECT * FROM users WHERE phone = %s"
        print(phone)
        db_conn.cursor.execute(sql, (phone,))
        return db_conn.cursor.fetchone()

    # Get user by id
    @staticmethod
    def get_user_by_id(db_conn,*, user_id: str):
        sql = "SELECT * FROM users WHERE id = %s"
        db_conn.cursor.execute(sql, (user_id,))
        return db_conn.cursor.fetchone()

    # Update user info
    @staticmethod
    def update_user(db_conn,*, user_id: int, email: str = None, phone: str = None):
        fields = []
        values = []
        if email:
            fields.append("email = %s")
            values.append(email)
        if phone:
            fields.append("phone = %s")
            values.append(phone)
        values.append(user_id)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
        db_conn.cursor.execute(sql, values)
        db_conn.db.commit()
        return True

    # Delete user
    @staticmethod
    def delete_user(db_conn,*, user_id: int):
        sql = "DELETE FROM users WHERE id = %s"
        db_conn.cursor.execute(sql, (user_id,))
        db_conn.db.commit()
        return True

    # Get all users
    @staticmethod
    def get_all_users(db_conn):
        sql = "SELECT * FROM users"
        db_conn.cursor.execute(sql)
        return db_conn.cursor.fetchall()

    @staticmethod
    def is_2fa_enabled(db_conn,*, user_id: str):
        sql = "SELECT is_2fa_enabled FROM users WHERE email = %s;"
        db_conn.cursor.execute(sql, (user_id,))
        return db_conn.cursor.fetchone()

