import streamlit as st

def show_couple_banner():
    couple = st.session_state.get("couple_info")
    if not couple:
        return
        st.markdown(
            """
            <div style="width:100%;margin:0 auto;margin-bottom:18px;">
                <div style="background:linear-gradient(120deg,#FFF7F3,#FCE8E4);border-radius:22px;padding:32px 0;text-align:center;box-shadow:0 4px 24px rgba(193,122,116,0.09);">
                    <span style="font-size:3.2rem;">💍</span>
                    <h2 style="font-size:2.1rem;color:#C17A74;font-weight:800;margin-bottom:8px;margin-top:12px;">Your Wedding Dashboard</h2>
                    <div style="font-size:1.15rem;color:#7A5C5C;font-weight:500;">Manage your registry, gifts, and memories in one place.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
