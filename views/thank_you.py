import streamlit as st
from database import get_connection, fetch_one

def show_thank_you(registry_id=None, couple_id=None):
    # Hide sidebar
    st.markdown("""
    <style>
    [data-testid="stSidebar"], .css-1lcbmhc {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

    # Get couple info from DB
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    couple = None
    if couple_id:
        couple = fetch_one(cur, "SELECT your_first_name, your_last_name, partner_first_name, partner_last_name, photo_url FROM couples WHERE couple_id=%s", (couple_id,))
    elif registry_id:
        reg = fetch_one(cur, "SELECT couple_id FROM registries WHERE registry_id=%s", (registry_id,))
        if reg:
            couple = fetch_one(cur, "SELECT your_first_name, your_last_name, partner_first_name, partner_last_name, photo_url FROM couples WHERE couple_id=%s", (reg['couple_id'],))
    conn.close()

    if couple:
        first_names = []
        if couple.get('your_first_name'):
            first_names.append(couple.get('your_first_name').strip())
        if couple.get('partner_first_name'):
            first_names.append(couple.get('partner_first_name').strip())
        name = " & ".join([n for n in first_names if n]) if first_names else "The Happy Couple"
        photo = couple.get('photo_url') if couple.get('photo_url') else None
    else:
        name = "The Happy Couple"
        photo = None

    st.markdown("""
    <style>
    .block-container, .main, .css-1dp5vir, .css-12oz5g7, .css-1lcbmhc {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }
    body, html {
        padding: 0 !important;
        margin: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    img = (
        f"<img src='{photo}' alt='Couple Photo' style='width:100vw;height:100vh;object-fit:cover;display:block;margin:0;padding:0;border:none;background:none;'/>"
        if photo and photo.strip()
        else "<div style='width:100vw;height:100vh;background:#fff;display:flex;align-items:center;justify-content:center;color:#B07269;font-size:7rem;margin:0;padding:0;border:none;'>💑</div>"
    )
    st.markdown(
        f"""
        <div style='display:flex;flex-direction:row;width:100vw;height:100vh;margin:0;padding:0;'>
            <div style='flex:1;overflow:hidden;height:100vh;margin:0;padding:0;'>
                {img}
            </div>
            <div style='flex:1;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding-left:180px;background:#fff;height:100vh;margin:0;padding:0;box-sizing:border-box;'>
                <div style='font-family:\"Dancing Script\",cursive;font-size:3.2rem;color:#B07269;font-weight:700;margin-bottom:18px;'>Thank You</div>
                <div style='font-size:1.25rem;color:#7A5C5C;font-family:Plus Jakarta Sans,Inter,sans-serif;margin-bottom:18px;'>For choosing a gift that adds joy to our new journey.<br>Your love, generosity, and blessings mean the world to us.<br>We are so grateful to share this milestone with you.</div>
                <div style='font-size:1.45rem;color:#C17A74;font-weight:700;font-family:Plus Jakarta Sans,Inter,sans-serif;margin-top:24px;'>— {name}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Add Google Fonts for Dancing Script
    st.markdown("""
    <link href='https://fonts.googleapis.com/css?family=Dancing+Script:700&display=swap' rel='stylesheet'>
    <style>
    .streamlit-expanderHeader {font-family: 'Plus Jakarta Sans', sans-serif;}
    </style>
    """, unsafe_allow_html=True)
