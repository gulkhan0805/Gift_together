import streamlit as st
from database import get_connection
from views.couple_banner import show_couple_banner

def show_delete_gift():
    item_id = st.session_state.get("delete_gift_id")
    if not item_id:
        st.error("No gift selected for deletion.")
        return

    st.header("Delete Gift")
    st.warning("Are you sure you want to delete this gift? This action cannot be undone.")
    if st.button("Confirm Delete", key="confirm_delete_btn"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM registry_items WHERE item_id=%s", (item_id,))
            conn.commit()
            cur.close()
            conn.close()
            st.success("Gift deleted successfully!")
            st.session_state.page = "couple_dashboard"
            st.rerun()
        except Exception as e:
            st.error(f"Database Error: {e}")

show_couple_banner()
