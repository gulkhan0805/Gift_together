import streamlit as st
import pandas as pd
import random
from database import get_connection, fetch_one, fetch_all
from views.couple_banner import show_couple_banner


def show_couple_dashboard():
    # Move Logout button to sidebar
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()

    # Show couple banner
    show_couple_banner()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Load registry
    registry = fetch_one(
        cur,
        "SELECT * FROM registries WHERE couple_id=%s",
        (st.session_state.couple_id,)
    )

    if not registry:
        st.error("No registry found for this couple.")
        return

    registry_id = registry["registry_id"]
    st.session_state.selected_registry_id = registry_id
    st.session_state.registry_id = registry_id

    # Load all items
    items = fetch_all(cur,
        "SELECT * FROM registry_items WHERE registry_id=%s",
        (registry_id,)
    )

    # Add Gift Button
    colA, colB = st.columns([6, 2])
    with colB:
        if st.button("➕ Add Gift", use_container_width=True):
            # Ensure registry_id is set before redirect
            st.session_state.registry_id = registry_id
            st.session_state.page = "choose_gift_type"
            st.rerun()

    # TABS
    tab1, tab2, tab3 = st.tabs(["🎁 My Gifts", "🧑‍🤝‍🧑 Contributors", "📊 Analytics"])

    # ==========================================================================================
    # TAB 1 — BEAUTIFUL ZOLA-STYLE GIFT CATALOG
    # ==========================================================================================
    with tab1:
        st.subheader("Your Gift Catalog")

        if not items:
            st.info("No items added yet. Click 'Add Gift' to start your registry.")
        else:
            # Use Streamlit columns for card layout
            for idx, item in enumerate(items):
                reserved = item.get("total_reserved_quantity", 0) or 0
                max_qty = item.get("max_quantity", 1) or 1
                contributed = item.get("total_contributed_amount", 0) or 0
                target = item.get("target_amount", 0) or 0

                # Determine percent and status based on item type
                if item.get("item_type", "PRODUCT").upper() == "PRODUCT" and target <= 500:
                    percent = int((reserved / max_qty) * 100) if max_qty else 0
                else:
                    percent = int((contributed / target) * 100) if target else 0

                if percent >= 100:
                    status_text = "Fully Gifted"
                    bar_color = "#27ae60"  # green
                elif percent > 0:
                    status_text = "Partially Gifted"
                    bar_color = "#f7b731"  # yellow
                else:
                    status_text = "Not Gifted"
                    bar_color = "#d3d3d3"  # gray

                img = item["image_url"] if item["image_url"] else "https://via.placeholder.com/400x250.png?text=No+Image"


                # Custom layout: bigger image, less gap, buttons on right
                col_img, col_info, col_btns = st.columns([2,5,1])
                with col_img:
                    st.image(img, width=240)
                with col_info:
                    st.markdown(f"<div style='font-weight:700;font-size:1.18rem;margin-bottom:4px;'>{item['item_name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:1.05rem;margin-bottom:2px;'>Price: <b>${item['target_amount']}</b></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:1.05rem;margin-bottom:2px;'>Status: {status_text}</div>", unsafe_allow_html=True)
                    # Full-width bar, fill color according to percent, rest gray
                    st.markdown(f"""
                    <div style='width:100%;background:#fff;border-radius:8px;height:18px;position:relative;margin-bottom:8px;'>
                        <div style='position:absolute;top:0;left:0;width:100%;height:18px;border-radius:8px;background:#e0e0e0;'></div>
                        <div style='position:absolute;top:0;left:0;width:{percent}%;height:18px;border-radius:8px;background:{bar_color};transition:width 0.5s;'></div>
                        <span style='position:absolute;left:50%;top:0;transform:translateX(-50%);font-size:13px;color:#333;'>{percent}% complete</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btns:
                    st.markdown("""
                    <style>
                    .custom-btn {
                        width: 110px;
                        height: 44px;
                        background: #c97b6a;
                        color: #fff;
                        border: none;
                        border-radius: 22px;
                        font-size: 1.05rem;
                        font-family: inherit;
                        margin-bottom: 16px;
                        cursor: pointer;
                        transition: background 0.2s;
                    }
                    .custom-btn:hover {
                        background: #b06a5c;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    if st.button("Edit", key=f"edit_btn_{item['item_id']}"):
                        st.session_state.edit_gift_id = item['item_id']
                        st.session_state.page = "edit_gift"
                        st.rerun()
                    if st.button("Delete", key=f"delete_btn_{item['item_id']}"):
                        st.session_state.delete_gift_id = item['item_id']
                        st.session_state.page = "delete_gift"
                        st.rerun()
                st.markdown("---")

    # ==========================================================================================
    # TAB 2 — CONTRIBUTORS
    # ==========================================================================================
    with tab2:
        def show_contributors():
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT g.first_name, g.last_name, g.email, i.item_name, i.item_type, pr.quantity, pr.mode, i.image_url, NULL as amount, NULL as guest_avatar
                FROM product_reservations pr
                JOIN guests g ON pr.guest_id = g.guest_id
                JOIN registry_items i ON pr.item_id = i.item_id
                ORDER BY pr.created_at DESC
            """)
            product_contributors = cur.fetchall()
            cur.execute("""
                SELECT g.first_name, g.last_name, g.email, i.item_name, i.item_type, NULL as quantity, NULL as mode, i.image_url, cc.amount, NULL as guest_avatar
                FROM cash_contributions cc
                JOIN guests g ON cc.guest_id = g.guest_id
                JOIN registry_items i ON cc.item_id = i.item_id
                ORDER BY cc.created_at DESC
            """)
            cash_contributors = cur.fetchall()
            cur.close()
            conn.close()
            contributors = product_contributors + cash_contributors

            st.markdown("""
            <style>
            .contrib-table-wrap {max-width:100%;margin:0 auto;background:#fff;border-radius:18px;box-shadow:0 4px 24px rgba(0,0,0,0.07);padding:0 0 12px 0;overflow-x:auto;}
            .contrib-table {width:100%;border-collapse:collapse;font-family:'Inter','Segoe UI',Arial,sans-serif;}
            .contrib-table th {background:#f8f9fa;font-weight:700;padding:18px 10px 14px 10px;font-size:1.08rem;color:#444;border-bottom:2px solid #f0f0f0;text-align:left;border-right:none;position:relative;}
            .contrib-table td {padding:12px 10px;font-size:1.04rem;vertical-align:middle;background:#fff;border-bottom:1px solid #f3f3f3;height:64px;border-right:none;}
            .contrib-table tr:last-child td {border-bottom:none;}
            .contrib-row:hover td {background:#f6f8fa;}
            .contrib-avatar, .contrib-initials {width:36px;height:36px;border-radius:50%;object-fit:cover;display:inline-block;vertical-align:middle;margin-right:12px;background:#eaeaea;font-weight:700;font-size:1.05rem;color:#fff;text-align:center;line-height:36px;}
            .contrib-initials {background:#6c8ae4;}
            .contrib-name-email {display:flex;flex-direction:column;}
            .contrib-name {font-weight:700;font-size:1.08rem;display:inline-block;vertical-align:middle;}
            .contrib-email {font-size:0.97rem;color:#888;margin-top:2px;}
            .contrib-badge {display:inline-block;font-size:12px;font-weight:600;padding:4px 10px;border-radius:12px;margin-right:2px;}
            .badge-green {background:#e7fbe7;color:#2e7d32;}
            .badge-yellow {background:#fffbe7;color:#a97c1a;}
            .badge-orange {background:#ffe7d6;color:#d35400;}
            .contrib-search-header {padding:0;margin:0;}
            .contrib-search-input-header {width:98%;padding:7px 12px;font-size:1.02rem;border-radius:8px;border:1px solid #e0e0e0;background:#fff;outline:none;margin:0;}
            @media (max-width:900px){.contrib-table-wrap{max-width:100%;}.contrib-table th,.contrib-table td{font-size:0.98rem;padding:10px 6px;}}
            </style>
            """, unsafe_allow_html=True)

            def initials_avatar(first_name, last_name):
                initials = (first_name[:1] + last_name[:1]).upper()
                colors = ['#6c8ae4', '#e48a6c', '#6ce4b1', '#e4d36c', '#b16ce4', '#e46cc0', '#6ce4e1']
                bg = random.choice(colors)
                return f"<span class='contrib-initials' style='background:{bg};'>{initials}</span>"

            # Search will be handled by the HTML input in the table header only
            search_query = st.session_state.get('contrib_search_header', '')
            if search_query:
                search_query_lower = search_query.lower()
                contributors = [row for row in contributors if search_query_lower in (row.get('first_name','') + ' ' + row.get('last_name','')).lower() or search_query_lower in row.get('email','').lower() or search_query_lower in row.get('item_name','').lower()]

            table_html = "<div class='contrib-table-wrap'>"
            table_html += "<table class='contrib-table'><thead><tr>"
            table_html += f"<th class='contrib-search-header' colspan='5'><input class='contrib-search-input-header' type='text' value='{search_query.replace("'", "&#39;")}' placeholder='Search by name, email, or gift' oninput='window.dispatchEvent(new Event(\'input\'))'></th></tr>"
            table_html += "<tr><th>Guest</th><th>Gift</th><th>Gift Type</th><th>Contribution</th><th>Status</th></tr></thead><tbody>"
            for row in contributors:
                first_name = row.get('first_name', '')
                last_name = row.get('last_name', '')
                email = row.get('email', '')
                item_name = row.get('item_name', '')
                item_type = row.get('item_type', '')
                amount = row.get('amount', '')
                quantity = row.get('quantity', '')
                mode = row.get('mode', '')
                image_url = row.get('image_url', '')
                guest_avatar = row.get('guest_avatar', '')
                # Product image (larger)
                product_img_html = f"<img src='{image_url}' alt='Product Image' style='width:80px;height:80px;object-fit:cover;border-radius:12px;margin-right:18px;'/>" if image_url else ""
                if guest_avatar:
                    avatar_html = f"<img src='{guest_avatar}' class='contrib-avatar' alt='Avatar'/>"
                else:
                    avatar_html = initials_avatar(first_name, last_name)
                name_email_html = f"<span class='contrib-name'>{avatar_html}{first_name} {last_name}</span><span class='contrib-email'>{email}</span>"
                gift_html = f"<div style='display:flex;align-items:center;'>{product_img_html}<span>{item_name}</span></div>"
                gift_type_html = "Product" if item_type == "PRODUCT" else "Cash Fund"
                if item_type == "PRODUCT":
                    contrib_html = f"Quantity: <b>{quantity if quantity else 'None'}</b>"
                elif item_type == "CASH_FUND":
                    contrib_html = f"Amount: <b>${amount}</b>"
                else:
                    contrib_html = ""
                if item_type == "PRODUCT":
                    if mode and mode.lower() == "online":
                        badge = "<span class='contrib-badge badge-green'>Online</span>"
                    elif mode and mode.lower() == "offline":
                        badge = "<span class='contrib-badge badge-orange'>Offline</span>"
                    elif mode and mode.lower() == "pickup":
                        badge = "<span class='contrib-badge badge-orange'>Pickup</span>"
                    else:
                        badge = "<span class='contrib-badge badge-green'>Active</span>"
                elif item_type == "CASH_FUND":
                    badge = "<span class='contrib-badge badge-yellow'>Cash Fund</span>"
                else:
                    badge = ""
                table_html += f"<tr class='contrib-row'><td>{name_email_html}</td><td>{gift_html}</td><td>{gift_type_html}</td><td>{contrib_html}</td><td>{badge}</td></tr>"
            table_html += "</tbody></table></div>"
            st.markdown(table_html, unsafe_allow_html=True)

        show_contributors()

    # ==========================================================================================
    # TAB 3 — ANALYTICS
    # ==========================================================================================
    with tab3:
        st.subheader("Analytics Overview")
        st.info("Charts coming soon.")

    cur.close()
    conn.close()
