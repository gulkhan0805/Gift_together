
import streamlit as st

from utils import init_session
from theme import inject_custom_css

from views.home import show_home
from views.couple_login import show_couple_login
from views.couple_dashboard import show_couple_dashboard
from views.guest_registry import show_guest_registry
from views.otp_flow import otp_flow
from views.finalize_gift import finalize_gift
from views.add_gift import show_add_gift
from views.edit_gift import show_edit_gift
from views.delete_gift import show_delete_gift
from views.choose_gift_type import show_choose_gift_type
from views.register_couple import show_register_couple
from views.register_registry import show_register_registry

st.set_page_config(
    page_title="Gift Together - Wedding Registry",
    layout="wide",
    page_icon="🎁",
)

def main():
    init_session()
    # Ensure page is set to 'home' on first load
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.session_state.page == "home":
        show_home()
    else:
        inject_custom_css()
        with st.sidebar:
            st.markdown("""
            <div style='height: 18px'></div>
            """, unsafe_allow_html=True)
        if st.session_state.page == "couple_login":
            show_couple_login()
        elif st.session_state.page == "couple_dashboard":
            show_couple_dashboard()
        elif st.session_state.page == "guest_registry":
            show_guest_registry()
        elif st.session_state.page == "otp_flow":
            otp_flow()
        elif st.session_state.page == "finalize_gift":
            finalize_gift()
        elif st.session_state.page == "add_gift":
            show_add_gift()
        elif st.session_state.page == "edit_gift":
            show_edit_gift()
        elif st.session_state.page == "delete_gift":
            show_delete_gift()
        elif st.session_state.page == "choose_gift_type":
            show_choose_gift_type()
        elif st.session_state.page == "register_couple":
            show_register_couple()
        elif st.session_state.page == "register_registry":
            show_register_registry()
        elif st.session_state.page == "thank_you":
            from views.thank_you import show_thank_you
            show_thank_you(
                registry_id=st.session_state.get("thank_you_registry_id"),
                couple_id=st.session_state.get("thank_you_couple_id")
            )



if __name__ == "__main__":
    main()
