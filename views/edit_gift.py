import streamlit as st
from database import get_connection
from views.couple_banner import show_couple_banner

def show_edit_gift():
    # Back button to return to dashboard
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard"):
        st.session_state.page = "couple_dashboard"
        st.rerun()
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    item_id = st.session_state.get("edit_gift_id")
    if not item_id:
        st.error("No gift selected for editing.")
        return

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM registry_items WHERE item_id=%s", (item_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()

    if not item:
        st.error("Gift not found.")
        return

    st.header("Edit Gift")
    st.markdown("---")

    gift_name = st.text_input("Product Name", value=item["item_name"])
    gift_desc = st.text_area("Description (optional)", value=item["description"])
    gift_price = st.number_input("Price ($)", min_value=1.0, value=float(item.get("target_amount", 1)))
    product_url = st.text_input("Online Purchase URL (optional)", value=item.get("product_url", ""))
    max_qty = st.number_input("Maximum Quantity", min_value=1, value=int(item.get("max_quantity", 1)))
    image_url = st.text_input("Image URL", value=item.get("image_url", ""))
    allow_online = st.checkbox("Allow Online Purchase", value=bool(item.get("allow_online", 1)))
    allow_offline = st.checkbox("Allow Offline Purchase", value=bool(item.get("allow_offline", 1)))

    if st.button("Save Changes"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE registry_items SET item_name=%s, description=%s, image_url=%s, target_amount=%s, allow_online=%s, allow_offline=%s, product_url=%s, max_quantity=%s WHERE item_id=%s
                """,
                (gift_name, gift_desc, image_url, gift_price, allow_online, allow_offline, product_url, max_qty, item_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            st.success("Gift updated successfully!")
            st.session_state.page = "couple_dashboard"
            st.rerun()
        except Exception as e:
            st.error(f"Database Error: {e}")
