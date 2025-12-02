import streamlit as st
from database import get_connection

def show_register_couple():
    st.header("Register Your Wedding")
    st.markdown("---")
    st.markdown("Please enter your couple details:")
    your_first_name = st.text_input("Your First Name")
    your_last_name = st.text_input("Your Last Name")
    partner_first_name = st.text_input("Partner's First Name")
    partner_last_name = st.text_input("Partner's Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone (optional)")

    if st.button("Save Couple Details"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO couples (your_first_name, your_last_name, partner_first_name, partner_last_name, email, password, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (your_first_name, your_last_name, partner_first_name, partner_last_name, email, password, phone)
            )
            conn.commit()
            cur.close()
            conn.close()
            st.success("Couple registered! Now enter your registry details.")
            st.session_state.couple_email = email
            st.session_state.page = "register_registry"
            st.rerun()
        except Exception as e:
            st.error(f"Database Error: {e}")
