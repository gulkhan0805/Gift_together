import streamlit as st
from database import get_connection, fetch_all, fetch_one

def show_guest_registry():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    st.markdown(
        """
        <div style="max-width:700px;margin:0 auto;padding:32px 0 0 0;">
            <h1 style="font-size:2.5rem;color:#C17A74;font-weight:800;margin-bottom:10px;text-align:center;">Search the Couple Whose Big Day You’re Celebrating</h1>
            <p style="font-size:1.18rem;color:#7A5C5C;font-weight:500;text-align:center;margin-bottom:32px;">
                Search their names to reveal the gifts, memories, and experiences they’re dreaming of.<br>
                Choose something meaningful and help turn their “someday” into “right now.”
        </div>
        """,
        unsafe_allow_html=True,
    )

    conn = get_connection()
    if not conn:
        return

    cur = conn.cursor(dictionary=True)

    couples = fetch_all(cur, "SELECT * FROM couples")
    if not couples:
        st.error("No couples are registered yet.")
        conn.close()
        return

    couple_names = {
        f"{c['your_first_name']} & {c['partner_first_name']}": c["couple_id"]
        for c in couples
    }
    couple_choice = st.selectbox("Who are you shopping for today?", list(couple_names.keys()))
    couple_id = couple_names[couple_choice]

    registry = fetch_one(
        cur, "SELECT * FROM registries WHERE couple_id=%s", (couple_id,)
    )

    if not registry:
        st.info("This couple has not set up a registry yet.")
        conn.close()
        return

    items = fetch_all(
        cur,
        "SELECT * FROM registry_items WHERE registry_id=%s",
        (registry["registry_id"],),
    )

    st.markdown(
        """
        <p class="tagline" style="margin-top:8px;font-size:1.12rem;color:#7A5C5C;font-weight:500;">
            Choose a gift or contribute to a shared experience. Prices and availability are updated in real time.
        </p>
        <!-- Removed pink section divider for cleaner look -->
        """,
        unsafe_allow_html=True,
    )

    for item in items:
        st.markdown("<div class='wedding-card' style='background:#fff;'>", unsafe_allow_html=True)
        st.markdown(f"<span class='price-badge'>${item['target_amount']}</span>", unsafe_allow_html=True)
        if item["item_type"].upper() == "CASH_FUND":
            st.markdown(f"<span style='font-size:1.15rem;font-weight:700;color:#C17A74;'> {item['item_name']} (Cash Fund)</span>", unsafe_allow_html=True)
            if item["description"]:
                st.markdown(f"<span style='color:#7A5C5C;font-size:1.05rem;'>{item['description']}</span>", unsafe_allow_html=True)
            contributed = item["total_contributed_amount"] or 0
            remaining = max((item["target_amount"] or 0) - contributed, 0)
            st.write(f"Contributed: **${contributed}**")
            st.write(f"Remaining: **${remaining}**")

            if item["image_url"]:
                st.image(item["image_url"], width=220)

            if remaining > 0:
                if st.button("Contribute to this Fund", key=f"fund-{item['item_id']}"):
                    st.session_state.selected_item_id = item["item_id"]
                    st.session_state.gift_mode = "GROUP"
                    st.session_state.page = "otp_flow"
                    st.rerun()
            else:
                st.success("This fund is fully contributed! 🎉")

            st.markdown("</div>", unsafe_allow_html=True)
            continue

        # PRODUCT
        if item["target_amount"] > 500:
            st.markdown("<span class='group-badge'>Group Gift</span>", unsafe_allow_html=True)

        st.markdown(f"**{item['item_name']}**", unsafe_allow_html=True)
        if item["description"]:
            st.write(item["description"])

        if item["image_url"]:
            st.image(item["image_url"], width=220)

        if item["target_amount"] <= 500:
            remaining = (
                item.get("max_quantity", 1)
                - item.get("total_reserved_quantity", 0)
            )
            st.write(f"Remaining quantity: **{remaining}**")

            if item["allow_online"] and item["product_url"]:
                st.write(f"Online purchase link: {item['product_url']}")
            if item["allow_offline"]:
                st.write("Can be purchased offline / in-store.")

            if remaining > 0:
                if st.button("Gift this item", key=f"gift-{item['item_id']}"):
                    st.session_state.selected_item_id = item["item_id"]
                    st.session_state.gift_mode = "FULL"
                    st.session_state.page = "otp_flow"
                    st.rerun()
            else:
                st.success("This item is fully gifted! 🎉")
        else:
            # Group gift product > $500
            contributed = item["total_contributed_amount"] or 0
            target = item["target_amount"] or 0
            remaining = max(target - contributed, 0)

            st.write(f"Total Price: **${target}**")
            st.write(f"Contributed: **${contributed}**")
            st.write(f"Remaining: **${remaining}**")
            st.write("This is a **Group Gift**. You can contribute any amount within the range allowed by the couple.")

            if remaining > 0:
                if st.button("Contribute to this Gift", key=f"group-{item['item_id']}"):
                    st.session_state.selected_item_id = item["item_id"]
                    st.session_state.gift_mode = "GROUP"
                    st.session_state.page = "otp_flow"
                    st.rerun()
            else:
                st.success("This group gift is fully funded! 🎉")

        st.markdown("</div>", unsafe_allow_html=True)

    conn.close()
