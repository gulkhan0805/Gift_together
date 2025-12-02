import streamlit as st
from utils import generate_otp

def otp_flow():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()

    st.markdown(
        """
        <div style='max-width:600px;margin:32px auto 0 auto;padding:38px 38px 32px 38px;background:#fff;border-radius:28px;box-shadow:0 8px 32px rgba(193,122,116,0.13);'>
            <div style='display:flex;align-items:center;justify-content:center;margin-bottom:18px;'>
                <span style='font-size:2.8rem;margin-right:18px;'>🔐</span>
                <h2 style='margin:0;font-size:2.1rem;color:#C17A74;font-weight:800;'>Verify Your Details</h2>
            </div>
            <div style='font-size:1.18rem;color:#7A5C5C;font-weight:500;margin-bottom:18px;text-align:center;'>
                Enter your contact details below so the couple can send you a thank-you note and keep you updated about their big day.<br>
                We’ll send a secure one-time code to verify your info.
            </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    name = st.text_input("Your full name")
    email = st.text_input("Email (optional)")
    phone = st.text_input("Phone number (optional)")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("Send OTP", key="send_otp_btn"):
        if not email and not phone:
            st.error("Please provide at least an email or phone.")
        elif not name.strip():
            st.error("Please enter your name.")
        else:
            otp = generate_otp()
            st.session_state.pending_otp = otp
            st.session_state.guest_contact = {
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
            }
            st.info(f"OTP sent! (demo mode: **{otp}**) Check your email or phone for the code.")

    if st.session_state.get("pending_otp"):
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        user_otp = st.text_input("Enter the 6-digit code you received")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Verify Code", key="verify_otp_btn"):
            if user_otp == st.session_state.pending_otp:
                st.success("Verified 🎉 Redirecting to finalize your gift…")
                st.session_state.pending_otp = None
                st.session_state.page = "finalize_gift"
                st.rerun()
            else:
                st.error("That code doesn’t match. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)
