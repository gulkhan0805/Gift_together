import time
import streamlit as st
from database import get_connection, fetch_one

def finalize_gift():
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    conn = get_connection()
    if not conn:
        return

    cur = conn.cursor(dictionary=True)

    item_id = st.session_state.get("selected_item_id")
    contact = st.session_state.get("guest_contact")
    if not item_id or not contact:
        st.error("Missing gift selection or contact details.")
        return

    item = fetch_one(cur, "SELECT * FROM registry_items WHERE item_id=%s", (item_id,))

    # Determine if product or cash contribution
    is_product = item["item_type"].upper() == "PRODUCT"
    # Heading size reduced for better fit
    heading_html = (
        f"<div style='max-width:600px;margin:32px auto 0 auto;padding:38px 38px 32px 38px;background:#fff;border-radius:28px;box-shadow:0 8px 32px rgba(193,122,116,0.13);'>"
        "<div style='display:flex;align-items:center;justify-content:center;margin-bottom:18px;'>"
        "<span style='font-size:1.6rem;margin-right:12px;'>💞</span>"
        "<h2 style='margin:0;font-size:1.35rem;color:#b07269;font-weight:750;font-family:Plus Jakarta Sans,Inter,sans-serif;display:inline;'>Add Your Touch to Their Journey</h2>"
        "</div>"
        f"<div style='font-size:1.08rem;color:#b07269;font-weight:500;margin-bottom:18px;text-align:center;font-family:Plus Jakarta Sans,Inter,sans-serif;'>You’re contributing to: <span style='color:#C17A74;font-weight:700;'>{item['item_name']}</span><br>"
        "<span style='color:#7A5C5C;'>Every bit brings them one step closer to an unforgettable memory.</span>"
        "</div>"
    )
    # Product summary
    if is_product:
        if item["target_amount"] <= 500:
            total = item["max_quantity"]
            reserved = item["total_reserved_quantity"] + item.get("total_gifted_quantity", 0)
            left = max(total - reserved, 0)
            summary_html = (
                "<div style='display:flex;flex-direction:row;align-items:center;justify-content:center;gap:22px;margin-bottom:18px;'>"
                f"<div style='background:#F9E6E6;color:#B07269;font-size:1.18rem;font-weight:800;padding:18px 28px;border-radius:18px;box-shadow:0 4px 16px rgba(193,122,116,0.13);transition:box-shadow 0.2s;min-width:140px;text-align:center;'>Total Available<br><span style='font-size:1.35rem;color:#B07269;'>{total}</span></div>"
                f"<div style='background:#F7F3EF;color:#C17A74;font-size:1.18rem;font-weight:800;padding:18px 28px;border-radius:18px;box-shadow:0 4px 16px rgba(193,122,116,0.13);transition:box-shadow 0.2s;min-width:140px;text-align:center;'>Reserved<br><span style='font-size:1.35rem;color:#A67C6B;'>{reserved}</span></div>"
                f"<div style='background:#FCE8F0;color:#C17A74;font-size:1.18rem;font-weight:800;padding:18px 28px;border-radius:18px;box-shadow:0 4px 16px rgba(193,122,116,0.13);transition:box-shadow 0.2s;min-width:140px;text-align:center;'>What's Left<br><span style='font-size:1.35rem;color:#B07269;'>{left}</span></div>"
                "</div>"
            )
        else:
            # Group product: show monetary summary
            summary_html = f"""
                <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:18px;'>
                    <div style='background:#FCE8E4;color:#b07269;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;margin-bottom:8px;'>Total Needed: ${item['target_amount']:.2f}</div>
                    <div style='background:#F7E6E1;color:#C17A74;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;margin-bottom:8px;'>Amount Given So Far: ${item.get('total_contributed_amount', 0):.2f}</div>
                    <div style='background:#FCE8E4;color:#b07269;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;'>What's Left: ${max(item['target_amount']-item.get('total_contributed_amount',0),0):.2f}</div>
                </div>
            """
    else:
        # Cash contribution
        summary_html = f"""
            <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:18px;'>
                <div style='background:#FCE8E4;color:#b07269;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;margin-bottom:8px;'>Total Needed: ${item['target_amount']:.2f}</div>
                <div style='background:#F7E6E1;color:#C17A74;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;margin-bottom:8px;'>Amount Given So Far: ${item.get('total_contributed_amount', 0):.2f}</div>
                <div style='background:#FCE8E4;color:#b07269;font-size:1.08rem;font-weight:700;padding:8px 18px;border-radius:999px;'>What's Left: ${max(item['target_amount']-item.get('total_contributed_amount',0),0):.2f}</div>
            </div>
        """
    # Only show redesigned card for product with quantity
    if item["item_type"].upper() == "PRODUCT" and item["target_amount"] <= 500:
        image_url = item.get('image_url') or item.get('image')
        total = item["max_quantity"]
        reserved = item["total_reserved_quantity"] + item.get("total_gifted_quantity", 0)
        left = max(total - reserved, 0)
        # Fix: Use session state and rerun for interactive quantity selector
        if "gift_qty" not in st.session_state:
            st.session_state["gift_qty"] = 1
        qty = st.session_state["gift_qty"]

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        image_url = item.get('image_url') or item.get('image')
        st.markdown(f"""
        <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;'>
            <div style='margin-bottom:24px;'>
                {(f"<img src='{image_url}' alt='Product Image' style='width:340px;height:340px;object-fit:cover;border-radius:36px;box-shadow:0 4px 16px rgba(193,122,116,0.10);'/>" if image_url else "<div style='width:340px;height:340px;background:#F9E6E6;border-radius:36px;display:flex;align-items:center;justify-content:center;color:#B07269;font-size:5rem;'>🎁</div>")}
            </div>
            <div style='font-size:1.18rem;color:#B07269;font-weight:700;margin-bottom:8px;'>Remaining Quantity</div>
            <div style='font-size:1.25rem;color:#C17A74;font-weight:700;margin-bottom:22px;'>{left} left</div>
            <div style='font-size:1.18rem;color:#B07269;font-weight:700;margin-bottom:10px;'>Select Quantity</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.button("➖", key="qty_minus"):
                if st.session_state["gift_qty"] > 1:
                    st.session_state["gift_qty"] -= 1
                    st.rerun()
        with col2:
            st.markdown(f"<div style='text-align:center;font-size:1.5rem;font-weight:700;color:#B07269;background:#F8E8E8;padding:12px 0;border-radius:14px;'>{st.session_state['gift_qty']}</div>", unsafe_allow_html=True)
        with col3:
            if st.button("➕", key="qty_plus"):
                if st.session_state["gift_qty"] < left:
                    st.session_state["gift_qty"] += 1
                    st.rerun()

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:1.08rem;color:#B07269;font-weight:600;margin-bottom:8px;text-align:center;'>How will you purchase this gift?</div>", unsafe_allow_html=True)
        gift_mode = st.radio("", ["ONLINE", "OFFLINE"], horizontal=True, key="purchase_method")
        # Only show summary card for non-product flows
        if not (item["item_type"].upper() == "PRODUCT" and item["target_amount"] <= 500):
            st.markdown(heading_html + summary_html + "</div>", unsafe_allow_html=True)

    registry = fetch_one(
        cur, "SELECT * FROM registries WHERE registry_id=%s", (item["registry_id"],)
    )

    first_name = contact["name"].split(" ")[0] if contact["name"] else ""
    last_name = " ".join(contact["name"].split(" ")[1:]) if contact["name"] else ""
    cur.execute(
        """
        INSERT INTO guests (couple_id, first_name, last_name, email)
        VALUES (%s, %s, %s, %s)
        """,
        (
            registry["couple_id"],
            first_name,
            last_name,
            contact["email"],
        ),
    )
    guest_id = cur.lastrowid

    # ---------- PRODUCT ----------
    if item["item_type"].upper() == "PRODUCT":
        if item["target_amount"] <= 500:
            remaining = (
                item["max_quantity"]
                - item["total_reserved_quantity"]
                - item.get("total_gifted_quantity", 0)
            )

            if st.button("Confirm Gift"):
                cur.execute(
                    """
                    INSERT INTO product_reservations
                    (item_id, guest_id, quantity, mode, status, created_at)
                    VALUES (%s,%s,%s,%s,'RESERVED',NOW())
                    """,
                    (
                        item_id,
                        guest_id,
                        qty,
                        gift_mode,
                    ),
                )
                cur.execute(
                    """
                    UPDATE registry_items
                    SET total_reserved_quantity = total_reserved_quantity + %s
                    WHERE item_id=%s
                    """,
                    (qty, item_id),
                )
                conn.commit()
                st.success("Your gift has been reserved! Thank you 💕")
                st.session_state.thank_you_registry_id = registry["registry_id"]
                st.session_state.thank_you_couple_id = registry["couple_id"]
                st.session_state.page = "thank_you"

        else:
            # Group product: guests contribute any amount, update total_contributed_amount, status stays AVAILABLE
            contributed = item.get("total_contributed_amount", 0) or 0
            target = item.get("target_amount", 0) or 0
            remaining = max(target - contributed, 0)

            if remaining == 0:
                st.success("This group product is fully funded! 🎉")
                st.info("Taking you back to the registry…")
                time.sleep(2)
                st.session_state.page = "guest_registry"
                conn.close()
                st.rerun()

            image_url = item.get('image_url') or item.get('image')
            st.markdown("""
            <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:18px;'>
                <div style='margin-bottom:18px;'>
                    {img}
                </div>
                <div style='font-size:1.35rem;color:#b07269;font-weight:750;font-family:Plus Jakarta Sans,Inter,sans-serif;margin-bottom:8px;text-align:center;'>Add Your Touch to Their Journey</div>
                <div style='font-size:1.08rem;color:#C17A74;font-weight:700;margin-bottom:8px;text-align:center;'>You’re contributing to: <span style='color:#C17A74;font-weight:800;'>{name}</span></div>
                <div style='font-size:1.02rem;color:#C17A74;font-weight:600;margin-bottom:8px;text-align:center;'>This is a group gift—multiple guests can contribute any amount!</div>
            </div>
            """.format(
                img=(f"<img src='{image_url}' alt='Product Image' style='width:180px;height:180px;object-fit:cover;border-radius:24px;box-shadow:0 2px 8px rgba(193,122,116,0.10);'/>" if image_url else "<div style='width:180px;height:180px;background:#F9E6E6;border-radius:24px;display:flex;align-items:center;justify-content:center;color:#B07269;font-size:3rem;'>🎁</div>"),
                name=item['item_name']
            ), unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                st.markdown(f"<div style='background:#F9E6E6;color:#B07269;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>Total Needed<br><span style='font-size:1.13rem;color:#B07269;'>${target:.2f}</span></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='background:#F7F3EF;color:#C17A74;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>Given So Far<br><span style='font-size:1.13rem;color:#A67C6B;'>${contributed:.2f}</span></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div style='background:#FCE8F0;color:#C17A74;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>What's Left<br><span style='font-size:1.13rem;color:#B07269;'>{remaining:.2f}</span></div>", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;font-size:1.12rem;color:#B07269;font-weight:700;margin-bottom:10px;'>How much would you like to gift?</div>", unsafe_allow_html=True)
            amount = st.number_input(
                "Amount to gift",
                min_value=100,
                max_value=int(min(1000, remaining)),
                value=int(min(100, remaining)),
                step=1,
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("Send My Gift", key="confirm_contribution_btn"):
                if amount > remaining:
                    st.error(f"You cannot contribute more than the remaining amount (${remaining}).")
                else:
                    cur.execute(
                        """
                        INSERT INTO cash_contributions
                        (item_id, guest_id, amount, payment_method)
                        VALUES (%s,%s,%s,'ONLINE')
                        """,
                        (
                            item["item_id"],
                            guest_id,
                            amount,
                        ),
                    )
                    # Update total_contributed_amount
                    cur.execute(
                        """
                        UPDATE registry_items
                        SET total_contributed_amount = total_contributed_amount + %s
                        WHERE item_id=%s
                        """,
                        (amount, item_id),
                    )
                    # Check if fully funded
                    cur.execute(
                        "SELECT total_contributed_amount, target_amount FROM registry_items WHERE item_id=%s",
                        (item_id,),
                    )
                    status_check = cur.fetchone()
                    if status_check and status_check["total_contributed_amount"] >= status_check["target_amount"]:
                        cur.execute(
                            "UPDATE registry_items SET status='RESERVED' WHERE item_id=%s",
                            (item_id,),
                        )
                    else:
                        cur.execute(
                            "UPDATE registry_items SET status='AVAILABLE' WHERE item_id=%s",
                            (item_id,),
                        )
                    conn.commit()
                    st.success("Your contribution has been recorded. Thank you 💕")
                    st.session_state.thank_you_registry_id = registry["registry_id"]
                    st.session_state.thank_you_couple_id = registry["couple_id"]
                    st.session_state.page = "thank_you"
                    st.rerun()

    # ---------- CASH FUND ----------
    elif item["item_type"].lower() == "cash_fund":
        contributed = item["total_contributed_amount"] or 0
        target = item["target_amount"] or 0
        remaining = max(target - contributed, 0)

        if remaining == 0:
            st.error("This cash fund is already fully contributed!")
            st.info("Taking you back to the registry…")
            time.sleep(2)
            st.session_state.page = "guest_registry"
            conn.close()
            st.markdown("</div></div>", unsafe_allow_html=True)
            st.rerun()

        image_url = item.get('image_url') or item.get('image')
        st.markdown("""
        <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:18px;'>
            <div style='margin-bottom:18px;'>
                {img}
            </div>
            <div style='font-size:1.35rem;color:#b07269;font-weight:750;font-family:Plus Jakarta Sans,Inter,sans-serif;margin-bottom:8px;text-align:center;'>Add Your Touch to Their Journey</div>
            <div style='font-size:1.08rem;color:#C17A74;font-weight:700;margin-bottom:8px;text-align:center;'>You’re contributing to: <span style='color:#C17A74;font-weight:800;'>{name}</span></div>
            <div style='font-size:1.02rem;color:#C17A74;font-weight:600;margin-bottom:8px;text-align:center;'>This is a cash fund—multiple guests can contribute any amount!</div>
        </div>
        """.format(
            img=(f"<img src='{image_url}' alt='Fund Image' style='width:180px;height:180px;object-fit:cover;border-radius:24px;box-shadow:0 2px 8px rgba(193,122,116,0.10);'/>" if image_url else "<div style='width:180px;height:180px;background:#F9E6E6;border-radius:24px;display:flex;align-items:center;justify-content:center;color:#B07269;font-size:3rem;'>💰</div>"),
            name=item['item_name']
        ), unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.markdown(f"<div style='background:#F9E6E6;color:#B07269;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>Total Needed<br><span style='font-size:1.13rem;color:#B07269;'>${target:.2f}</span></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='background:#F7F3EF;color:#C17A74;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>Given So Far<br><span style='font-size:1.13rem;color:#A67C6B;'>${contributed:.2f}</span></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='background:#FCE8F0;color:#C17A74;font-size:1.02rem;font-weight:700;padding:10px 0 6px 0;border-radius:14px;text-align:center;min-width:90px;margin-bottom:0;'>What's Left<br><span style='font-size:1.13rem;color:#B07269;'>{remaining:.2f}</span></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:1.12rem;color:#B07269;font-weight:700;margin-bottom:10px;'>How much would you like to gift?</div>", unsafe_allow_html=True)
        amount = st.number_input(
            "Contribution amount",
            min_value=1,
            max_value=int(remaining),
            value=int(min(100, remaining)),
            step=1,
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Confirm Contribution"):
            if amount > remaining:
                st.error(f"You cannot contribute more than the remaining amount (${remaining}).")
            else:
                cur.execute(
                    """
                    INSERT INTO cash_contributions
                    (item_id, guest_id, amount, payment_method)
                    VALUES (%s,%s,%s,'ONLINE')
                    """,
                    (
                        item["item_id"],
                        guest_id,
                        amount,
                    ),
                )
                cur.execute(
                    """
                    UPDATE registry_items
                    SET total_contributed_amount = total_contributed_amount + %s
                    WHERE item_id=%s
                    """,
                    (amount, item_id),
                )
                cur.execute(
                    "SELECT total_contributed_amount, target_amount FROM registry_items WHERE item_id=%s",
                    (item_id,),
                )
                fund_status = cur.fetchone()
                if (
                    fund_status
                    and fund_status["total_contributed_amount"] >= fund_status["target_amount"]
                ):
                    try:
                        cur.execute(
                            "UPDATE registry_items SET status='RESERVED' WHERE item_id=%s",
                            (item_id,),
                        )
                    except Exception:
                        pass
                conn.commit()
                st.success("Your cash fund contribution has been recorded. Thank you 💕")
                st.session_state.thank_you_registry_id = registry["registry_id"]
                st.session_state.thank_you_couple_id = registry["couple_id"]
                st.session_state.selected_couple_id = registry["couple_id"]
                st.session_state.page = "thank_you"
                st.rerun()

    conn.close()
    st.markdown("</div>", unsafe_allow_html=True)  # wedding-card
    st.markdown("</div>", unsafe_allow_html=True)  # centered-container
