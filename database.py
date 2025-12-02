
import streamlit as st
import mysql.connector

def get_connection():
    """Create and return a MySQL connection."""
    try:
        return mysql.connector.connect(
            host="db-mysql-itom-do-user-28250611-0.j.db.ondigitalocean.com",
            user="group06",
            password="Pass2025_group06",
            database="group06",
            port=25060,
        )
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None


def fetch_one(cur, query, params=None):
    """Executes a query and returns a single row (dict)."""
    cur.execute(query, params or ())
    result = cur.fetchone()
    try:
        cur.fetchall()  # Clear unread results
    except Exception:
        pass
    return result


def fetch_all(cur, query, params=None):
    """Executes a query and returns all rows."""
    cur.execute(query, params or ())
    return cur.fetchall()
