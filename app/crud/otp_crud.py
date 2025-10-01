class OTPCrud:
    @staticmethod
    def create_otp(db_conn,txn_id:str,email:str,hashed_otp:str):
        query  = 'INSERT INTO otp_txns (txn_id,hashed_otp,email,is_used,create_ts,expire_ts)VALUES(%s,%s,%s,0,CURRENT_TIMESTAMP(6),DATE_ADD(CURRENT_TIMESTAMP(6), INTERVAL 3 MINUTE));'
        db_conn.cursor.execute(query,(txn_id,hashed_otp,email))
        rowCnt = db_conn.cursor.rowcount
        db_conn.commit()
        return rowCnt

    @staticmethod
    def fetch_otp(db_conn,txn_id):
        query = """
        SELECT
    email,hashed_otp
    FROM
        otp_txns
    where
        txn_id = %s
        AND NOT is_used AND NOT is_verified
        AND expire_ts > create_ts
        AND CURRENT_TIMESTAMP() <= expire_ts;
        """
        db_conn.cursor.execute(query,(txn_id,))
        row = db_conn.cursor.fetchone()
        if row:
            return row
        else:
            return None
    @staticmethod
    def is_otp_validated(db_conn,*,txn_id,email):
        query = """
        SELECT
            *
        FROM
            otp_txns
        where
        txn_id = %s
        AND email = %s
        AND NOT is_used
        AND NOT is_used AND is_verified
        AND expire_ts > create_ts
        AND CURRENT_TIMESTAMP() <= expire_ts;
        """
        db_conn.cursor.execute(query,(txn_id,email,))
        row = db_conn.cursor.fetchone()
        if row:
            return row
        else:
            return None

    @staticmethod
    def update_is_verify(db_conn,txn_id):
        query = """
        UPDATE
            otp_txns
        SET
            is_verified = 1
        WHERE
            txn_id = %s
            AND NOT is_verified;"""

        db_conn.cursor.execute(query,(txn_id,))
        rowCnt = db_conn.cursor.rowcount
        db_conn.commit()
        return rowCnt


    @staticmethod
    def update_is_used(db_conn,txn_id):
        query = """
        UPDATE
            otp_txns
        SET
            is_used = 1
        WHERE
            txn_id = %s
            AND NOT is_used;"""

        db_conn.cursor.execute(query,(txn_id,))
        rowCnt = db_conn.cursor.rowcount
        db_conn.commit()
        return rowCnt



    @staticmethod
    def delete_otp(db_conn,txn_id):
        query = """
        DELETE FROM
            otp_txns
        WHERE txn_id = %s;"""

        db_conn.cursor.execute(query,(txn_id,))
        rowCnt = db_conn.cursor.rowcount
        db_conn.commit()
        return rowCnt



