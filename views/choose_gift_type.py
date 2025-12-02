import streamlit as st
from views.couple_banner import show_couple_banner

def show_choose_gift_type():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    st.markdown(
        """
        <div style="max-width:600px;margin:0 auto;padding:32px 0;">
            <h1 style="font-size:2.3rem;color:#C17A74;font-weight:800;margin-bottom:18px;text-align:center;">Add a New Gift</h1>
            <p style="font-size:1.15rem;color:#7A5C5C;font-weight:500;text-align:center;margin-bottom:32px;">
                Select the type of gift you want to add to your wedding registry.<br>
                Choose between a product item or a cash fund for your guests to contribute.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div style="display:flex;flex-direction:column;align-items:center;">
                <span style="font-size:2.1rem;color:#C17A74;">🛍️</span>
                <span style="font-size:1.12rem;color:#C17A74;font-weight:600;margin-bottom:12px;">Product Item</span>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Add Product Item", key="choose_product", use_container_width=True):
            st.session_state.gift_type = "product"
            st.session_state.page = "add_gift"
            st.rerun()
    with col2:
        st.markdown(
            """
            <div style="display:flex;flex-direction:column;align-items:center;">
                <span style="font-size:2.1rem;color:#C17A74;">💰</span>
                <span style="font-size:1.12rem;color:#C17A74;font-weight:600;margin-bottom:12px;">Cash Fund</span>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Add Cash Fund", key="choose_cash", use_container_width=True):
            st.session_state.gift_type = "cash"
            st.session_state.page = "add_gift"
            st.rerun()
