import psycopg2
import pandas as pd
import bcrypt
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

# =========================
# DB CONNECTION
# =========================
conn = psycopg2.connect(
    host="localhost",
    database="Client_QueryDB",
    user="postgres",
    password="12345"
)

# =========================
# LOGIN
# =========================
def check_login(username, password, role):
    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT password_hash, role,phono FROM login WHERE username = %s",
            (username,)
        )

        row = cur.fetchone()
        cur.close()

        if not row:
            return False, "User not found"
        db_hash, db_role,phono = row

        if bcrypt.checkpw(password.encode(), db_hash.encode()):
            if role == db_role:
                return True, db_role,phono
            else:
                return False, "Invalid Role"
        else:
            return False, "Invalid password"

    except Exception as e:
        return False, f"Login Error: {str(e)}"


# =========================
# UPDATE PASSWORD
# =========================
def update_password(username, old_pwd, new_pwd):
    try:
        new_hash = bcrypt.hashpw(new_pwd.encode(), bcrypt.gensalt()).decode()

        query = "SELECT update_password_secure(%s, %s, %s) AS result;"
        df = pd.read_sql(query, conn, params=(username, old_pwd, new_hash))

        conn.commit()

        return df['result'][0]

    except Exception as e:
        conn.rollback()
        return f"Error: {str(e)}"


# =========================
# INSERT USER
# =========================
def insert_user(username, password, role, phono, created_by):
    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        cur = conn.cursor()
        cur.execute(
            "SELECT insert_user_fn(%s, %s, %s, %s, %s)",
            (username, password_hash, role, created_by, phono)
        )

        result = cur.fetchone()[0]

        conn.commit()
        cur.close()

        return result

    except Exception as e:
        conn.rollback()
        return f"Error: {str(e)}"


# =========================
# INSERT QUERY
# =========================
def insert_query(email, phono, category, description):
    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT insert_query(%s, %s, %s, %s);",
            (email, phono, category, description)
        )

        result = cur.fetchone()[0]

        conn.commit()
        cur.close()

        return result

    except Exception as e:
        conn.rollback()
        return f"Error: {str(e)}"


# =========================
# GET FILTERED QUERIES
# =========================
def get_queries(phono=None, status=None):
    try:
        query = "SELECT * FROM get_queries_filter(%s, %s);"
        return pd.read_sql(query, conn, params=(phono, status))

    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})


# =========================
# GET ALL QUERIES
# =========================
def get_all_queries():
    try:
        return pd.read_sql("SELECT * FROM get_all_queries();", conn)

    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})


# =========================
# CLOSE QUERY
# =========================
def close_query(query_id):
    try:
        query = "SELECT close_query(%s) AS result;"
        df = pd.read_sql(query, conn, params=(query_id,))

        conn.commit()

        return df['result'][0]

    except Exception as e:
        conn.rollback()
        return f"Error: {str(e)}"