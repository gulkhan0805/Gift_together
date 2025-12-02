import streamlit as st
from database import get_connection, fetch_one

def show_register_registry():
    st.header("Registry Details")
    st.markdown("---")
    st.markdown("Please enter your registry details:")
    registry_name = st.text_input("Registry Name")
    location = st.text_input("Location")

    st.subheader("Select Event Type")
    event_types = [
        {"label": "Wedding", "icon": "💍"},
        {"label": "Engagement", "icon": "💑"},
        {"label": "Anniversary", "icon": "🎉"},
        {"label": "Birthday", "icon": "🎂"},
        {"label": "Other", "icon": "✨"},
    ]
    cols = st.columns(len(event_types))
    selected_event_type = None
    for i, et in enumerate(event_types):
        with cols[i]:
            if st.button(f"{et['icon']} {et['label']}", key=f"event_type_{et['label']}"):
                st.session_state.selected_event_type = et['label']
    if "selected_event_type" in st.session_state:
        selected_event_type = st.session_state.selected_event_type
        st.success(f"Selected Event Type: {selected_event_type}")

    event_date = st.date_input("Event Date")
    uploaded_img = st.file_uploader("Upload Couple Photo", type=["jpg", "jpeg", "png"])
    photo_url = ""
    if uploaded_img:
        import cloudinary
        import cloudinary.uploader
        cloudinary.config(
            cloud_name="di80pp52x",
            api_key="997571313277177",
            api_secret="sLXRm-HIF1TH-OXSyqG3-TwxZWs",
            secure=True
        )
        try:
            result = cloudinary.uploader.upload(
                uploaded_img,
                folder="couple_photos/"  # optional
            )
            photo_url = result["secure_url"]
            st.image(photo_url, width=120)
        except Exception as e:
            st.error(f"Cloudinary Upload Failed: {e}")

    if st.button("Save Registry Details"):
        if not selected_event_type:
            st.error("Please select an event type.")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Get couple_id from email
            cur.execute("SELECT couple_id FROM couples WHERE email=%s", (st.session_state.couple_email,))
            result = cur.fetchone()
            if result:
                couple_id = result[0]
                cur.execute(
                    "INSERT INTO registries (couple_id, registry_name, event_type, event_date, location) VALUES (%s, %s, %s, %s, %s)",
                    (couple_id, registry_name, selected_event_type, event_date, location)
                )
                if photo_url:
                    cur.execute("UPDATE couples SET photo_url=%s WHERE couple_id=%s", (photo_url, couple_id))
                conn.commit()
                cur.close()
                conn.close()
                st.success("Registry created! Redirecting to dashboard...")
                st.session_state.couple_id = couple_id
                st.session_state.page = "couple_dashboard"
                st.rerun()
            else:
                st.error("Couple not found. Please register again.")
        except Exception as e:
            st.error(f"Database Error: {e}")
