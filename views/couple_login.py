import streamlit as st
from database import get_connection, fetch_one

def show_couple_login():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    # Removed stray opening div that was not closed
    st.markdown(
        """
        <div class="wedding-card" style="background:linear-gradient(120deg,#FFF7F3,#FCE8E4);">
            <h1 style="margin-top:0;font-size:2.3rem;color:#C17A74;font-weight:800;">Couple Sign In</h1>
            <p style="color:#7A5C5C; font-size:1.15rem; margin-bottom:18px; font-weight:500;">
                Welcome back! Access your private dashboard to manage your registry, add gifts, and track contributions in style.
            </p>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")


    col1, col2 = st.columns([1, 2])
    with col1:
        login_clicked = st.button("Sign in", use_container_width=True)
    with col2:
        if st.button("Register Your Wedding", use_container_width=True):
            st.session_state.page = "register_couple"
            st.rerun()

    if login_clicked:
        conn = get_connection()
        if not conn:
            st.markdown("</div></div>", unsafe_allow_html=True)
            return

        try:
            cur = conn.cursor(dictionary=True)
            couple = fetch_one(
                cur,
                "SELECT * FROM couples WHERE email = %s AND password = %s",
                (email, password),
            )
            cur.close()
            conn.close()

            if couple:
                st.session_state.user_type = "couple"
                st.session_state.couple_id = couple["couple_id"]
                st.session_state.couple_info = {
                    "your_first_name": couple.get("your_first_name", ""),
                    "your_last_name": couple.get("your_last_name", ""),
                    "partner_first_name": couple.get("partner_first_name", ""),
                    "partner_last_name": couple.get("partner_last_name", ""),
                    # Add photo if available, e.g. "photo_url": couple.get("photo_url", "")
                }
                st.session_state.page = "couple_dashboard"
                st.success("Welcome back! Redirecting to your dashboard…")
                st.rerun()
            else:
                st.error("Invalid email or password. Please try again.")

        except Exception as e:
            st.error(f"Login error: {e}")

    st.markdown(
        """
        <p style="font-size:13px;color:#999;margin-top:12px;">
            Don’t worry, this is just a school project – no real accounts or payments.
        </p>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
