
import streamlit as st
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def init_session():
    defaults = {
        "page": "home",
        "user_type": None,
        "couple_id": None,
        "selected_registry_id": None,
        "guest_contact": None,
        "pending_otp": None,
        "selected_item_id": None,
        "gift_mode": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
