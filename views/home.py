
import streamlit as st





def show_home():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()



    st.markdown("""
    <style>
    html, body, [class^='css'] {
        font-family: 'Plus Jakarta Sans', 'Inter', Arial, sans-serif !important;
        background: #FFF7F3;
    }
    .home-main-row { display: flex; flex-direction: row; min-height: 100vh; }
    .home-left-img {
        flex: 1;
        min-height: 100vh;
        background: #FFF7F3;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
    }
    .home-img {
        border-radius: 32px;
        box-shadow: 0 8px 32px rgba(193,122,116,0.13);
        width: 90%;
        max-width: 520px;
        height: 480px;
        object-fit: cover;
        margin: auto;
        display: block;
    }
    .home-right-content {
        flex: 1;
        min-height: 100vh;
        height: 100vh;
        background: #FFF;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .home-btn {
        width: 340px;
        height: 64px;
        border-radius: 18px;
        border: none;
        background: #C17A74;
        color: #fff;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 32px;
        box-shadow: 0 4px 24px rgba(193,122,116,0.09);
        cursor: pointer;
        transition: background 0.2s, transform 0.2s;
    }
    .home-btn:hover {
        background: #a85f4e;
        transform: scale(1.03);
    }
    @media (max-width: 900px) {
        .home-main-row { flex-direction: column; }
        .home-left-img, .home-right-content { min-height: 320px; height: 320px; }
        .home-img { height: 320px; }
        .home-btn { width: 98vw; max-width: 98vw; }
    }
    </style>
    <div class="home-main-row">
        <div class="home-left-img">
            <img class="home-img" src="https://res.cloudinary.com/di80pp52x/image/upload/v1764693185/pexels-annetnavi-792777_cqgh7l.jpg" alt="Wedding" />
        </div>
        <div class="home-right-content">
            <button class="home-btn" id="coupleBtn">I am Couple</button>
            <button class="home-btn" id="guestBtn">I am Guest</button>
        </div>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('coupleBtn').onclick = function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'couple'}, '*');
        };
        document.getElementById('guestBtn').onclick = function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'guest'}, '*');
        };
    });
    </script>
    """, unsafe_allow_html=True)

    # Streamlit navigation logic for buttons (only one set, unique keys)
    colA, colB = st.columns(2)
    with colA:
        if st.button("I am Couple", key="couple_btn_home"):
            st.session_state.page = "couple_login"
            st.rerun()
    with colB:
        if st.button("I am Guest", key="guest_btn_home"):
            st.session_state.page = "guest_registry"
            st.rerun()
