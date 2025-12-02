import streamlit as st

def show_sidebar():
    st.markdown(
        """
        <div style="text-align:center;padding-top:32px;padding-bottom:8px;">
            <span style="font-size:2.7rem;">💒</span>
            <h1 style="font-size:2rem;color:#C17A74;font-weight:800;margin-bottom:6px;margin-top:8px;">Wedding Dashboard</h1>
            <div style="font-size:1.08rem;color:#7A5C5C;font-weight:500;margin-bottom:18px;">Manage your registry and gifts</div>
            <hr style="border:none;border-top:1.5px solid #e5d6d0;margin:18px 0 18px 0;" />
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Only show Sign Out if couple is logged in and not on home or guest pages
    page = st.session_state.get("page", "home")
    couple_logged_in = st.session_state.get("couple_id") is not None
    if couple_logged_in and page not in ["home", "guest_registry"]:
        if st.button("Sign Out", key="logout_btn_sidebar", help="Sign out of your dashboard"):
            for k in list(st.session_state.keys()):
                if k != "page":
                    del st.session_state[k]
            st.session_state.page = "home"
            st.rerun()
