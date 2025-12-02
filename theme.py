
import streamlit as st

def inject_custom_css():
    css = """
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif !important;
    }

    body {
        background: #FAF5F1 !important;
    }

    section[data-testid="stSidebar"] {
        background: #F3EBE4 !important;
        border-right: 1px solid #E1D5CC;
    }

    h1, h2, h3 {
        color: #333333 !important;
        font-weight: 700 !important;
    }

    .wedding-card {
        background: #FFFFFF;
        padding: 22px 24px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        margin-bottom: 22px;
        transition: 0.22s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .wedding-card::before {
        content: "";
        position: absolute;
        width: 140px;
        height: 140px;
        background: radial-gradient(circle at top left, rgba(255, 182, 193, 0.22), transparent 60%);
        top: -40px;
        left: -40px;
    }
    .wedding-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.10);
    }

    .metric-card {
        background: #FFFFFF;
        padding: 16px 18px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    .metric-label {
        font-size: 13px;
        color: #777777;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #333333;
    }

    .price-badge {
        background: #F8E9E9;
        color: #C7887F;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 8px;
    }

    .group-badge {
        background: #E3F7EC;
        color: #2F7A4A;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }

    .section-divider {
        height: 1px;
        background: #E6E0D8;
        margin: 26px 0;
    }

    .stButton>button {
        background: linear-gradient(120deg, #C7887F, #b07269);
        color: #FFFFFF;
        border-radius: 999px;
        padding: 8px 22px;
        border: none;
        font-weight: 600;
        font-size: 15px;
        transition: 0.18s ease-in-out;
    }
    .stButton>button:hover {
        filter: brightness(0.96);
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .tagline {
        color: #666666;
        font-size: 15px;
    }

    .centered-container {
        max-width: 520px;
        margin: 0 auto;
    }

    .hero {
        padding: 32px 28px;
        border-radius: 24px;
        background: linear-gradient(135deg, #FFE6E0, #FFF6EB);
        display: flex;
        flex-direction: row;
        gap: 24px;
        align-items: center;
    }
    .hero-text {
        flex: 2;
    }
    .hero-image-wrapper {
        flex: 1;
        text-align: right;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #555;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_metric_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
