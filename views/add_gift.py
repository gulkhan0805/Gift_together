# modules/add_gift.py
import streamlit as st
import cloudinary
import cloudinary.uploader
from database import get_connection
from views.couple_banner import show_couple_banner


# ------------------------------------
# CLOUDINARY CONFIG (SIGNED UPLOAD)
# ------------------------------------
cloudinary.config(
    cloud_name="di80pp52x",
    api_key="997571313277177",
    api_secret="sLXRm-HIF1TH-OXSyqG3-TwxZWs",
    secure=True
)


# ------------------------------------
# CLOUDINARY UPLOAD FUNCTION
# ------------------------------------
def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="wedding_gifts/"  # optional
        )
        return result["secure_url"]
    except Exception as e:
        st.error(f"Cloudinary Upload Failed: {e}")
        return None


# ------------------------------------
# STREAMLIT ADD GIFT PAGE
# ------------------------------------
def show_add_gift():
    # Back button to return to dashboard
    if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_add_gift"):
        st.session_state.page = "couple_dashboard"
        st.rerun()
    from views.sidebar import show_sidebar
    with st.sidebar:
        show_sidebar()
    show_couple_banner()  # Display the couple banner at the top

    # Ensure registry_id is initialized
    if "registry_id" not in st.session_state:
        st.error("Registry ID missing. Please return to the dashboard and try again.")
        return
    gift_type = st.session_state.get("gift_type")
    if gift_type == "product":
        st.header("🛍️ Add a Product Gift")
        st.markdown("---")
        # ...existing product form code...
        # PRODUCT ITEM FLOW
        # ...existing code...
        # (no radio for type)
    elif gift_type == "cash":
        st.header("💰 Add a Cash Fund")
        st.markdown("---")
        # ...existing cash fund form code...
        # CASH FUND FLOW
        # ...existing code...
    else:
        st.error("No gift type selected. Please go back and choose a gift type.")
        return

    if gift_type == "product":
        st.subheader("Product Gift Details")

        # CATEGORY SELECTION
        PRODUCT_TEMPLATES = {

            "Home Essentials": [
                {
                    "name": "VINARN Blanket",
                    "image": "https://res.cloudinary.com/di80pp52x/image/upload/v1764481820/VINARN_Blanket_gwral5.webp",
                    "website_url": "https://www.ikea.com/us/en/images/products/vinarn-blanket__1202567_pe904944_s5.jpg",
                    "price": 24
                },
                {
                    "name": "BADBJORN Bath Towel",
                    "image": "https://res.cloudinary.com/di80pp52x/image/upload/v1764481819/BADBJORN_Bath_Towel_qn749v.webp",
                    "website_url": "https://www.ikea.com/us/en/images/products/badbjorn-bath-towel__1202567_pe904944_s5.jpg",
                    "price": 9
                },
                {
                    "name": "STJARNBRACKA Pillow",
                    "image": "https://res.cloudinary.com/di80pp52x/image/upload/v1764481820/STJARNBRACKA_Pillow_xrgkrq.webp",
                    "website_url": "https://www.ikea.com/us/en/images/products/stjarnbracka-pillow__1202567_pe904944_s5.jpg",
                    "price": 15
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Kitchen & Dining": [
                {
                    "name": "VARDAGEN Pot with lid",
                    "image": "https://www.ikea.com/us/en/images/products/vardagen-pot-with-lid__0710598_pe727849_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/vardagen-pot-with-lid__0710598_pe727849_s5.jpg",
                    "price": 39
                },
                {
                    "name": "365+ Mug White",
                    "image": "https://www.ikea.com/us/en/images/products/365-mug-white__0711330_pe728471_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/365-mug-white__0711330_pe728471_s5.jpg",
                    "price": 4
                },
                {
                    "name": "POKAL Glass Set",
                    "image": "https://www.ikea.com/us/en/images/products/pokal-glass-clear-glass__0710581_pe727832_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/pokal-glass-clear-glass__0710581_pe727832_s5.jpg",
                    "price": 12
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Appliances": [
                {
                    "name": "TILLREDA Portable Induction Cooktop",
                    "image": "https://www.ikea.com/us/en/images/products/tillreda-portable-induction-cooktop-white__0712188_pe728965_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/tillreda-portable-induction-cooktop-white__0712188_pe728965_s5.jpg",
                    "price": 65
                },
                {
                    "name": "FROJER Fan",
                    "image": "https://www.ikea.com/us/en/images/products/frojer-fan-white__1202865_pe905313_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/frojer-fan-white__1202865_pe905313_s5.jpg",
                    "price": 35
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Decor & Furnishing": [
                {
                    "name": "TERIALD Table Lamp",
                    "image": "https://www.ikea.com/us/en/images/products/teriald-table-lamp__1202567_pe904944_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/teriald-table-lamp__1202567_pe904944_s5.jpg",
                    "price": 29
                },
                {
                    "name": "STILREN Vase",
                    "image": "https://www.ikea.com/us/en/images/products/stilren-vase-white__1179665_pe897430_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/stilren-vase-white__1179665_pe897430_s5.jpg",
                    "price": 15
                },
                {
                    "name": "KRISTRUP Rug",
                    "image": "https://www.ikea.com/us/en/images/products/kristrup-rug-flatwoven-gray__1181987_pe897911_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/kristrup-rug-flatwoven-gray__1181987_pe897911_s5.jpg",
                    "price": 69
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Electronics": [
                {
                    "name": "SYMFONISK WiFi Speaker",
                    "image": "https://www.ikea.com/us/en/images/products/symfonisk-wifi-bookshelf-speaker-white-gen-2__1086393_pe860251_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/symfonisk-wifi-bookshelf-speaker-white-gen-2__1086393_pe860251_s5.jpg",
                    "price": 119
                },
                {
                    "name": "KOPPLA USB Charger",
                    "image": "https://www.ikea.com/us/en/images/products/koppla-2-port-usb-charger-white__0712272_pe728999_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/koppla-2-port-usb-charger-white__0712272_pe728999_s5.jpg",
                    "price": 8
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Travel & Experience": [
                {
                    "name": "DRAGGAN Cart",
                    "image": "https://www.ikea.com/us/en/images/products/draggan-cart-gray__0712410_pe729077_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/draggan-cart-gray__0712410_pe729077_s5.jpg",
                    "price": 39
                },
                {
                    "name": "SOMMARFLADER Cooler Bag",
                    "image": "https://www.ikea.com/us/en/images/products/sommarflader-cooler-bag-blue__1092653_pe863991_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/sommarflader-cooler-bag-blue__1092653_pe863991_s5.jpg",
                    "price": 12
                },
                {
                    "name": "Other",
                    "image": "https://via.placeholder.com/220x120?text=Other",
                    "website_url": "",
                    "price": 0
                }
            ],

            "Other": [
                {
                    "name": "KUGGIS Storage Box",
                    "image": "https://www.ikea.com/us/en/images/products/kuggis-box-with-lid-white__0710873_pe728144_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/kuggis-box-with-lid-white__0710873_pe728144_s5.jpg",
                    "price": 9
                },
                {
                    "name": "FRAKTA Shopping Bag",
                    "image": "https://www.ikea.com/us/en/images/products/frakta-shopping-bag-large-blue__0711192_pe728356_s5.jpg",
                    "website_url": "https://www.ikea.com/us/en/images/products/frakta-shopping-bag-large-blue__0711192_pe728356_s5.jpg",
                    "price": 1
                }
            ]
        }


        categories = list(PRODUCT_TEMPLATES.keys())
        selected_category = st.selectbox("Select a Category", categories)

        # Horizontal product gallery
        st.markdown(
            """
            <style>
            .scrolling-wrapper {overflow-x: auto; display: flex; flex-wrap: nowrap; padding-bottom: 10px;}
            .product-card {background: #fff; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-right: 18px; min-width: 220px; max-width: 220px; flex: 0 0 auto; padding: 16px; text-align: center; position: relative; transition: box-shadow 0.2s;}
            .product-card img {border-radius: 12px; width: 100%; height: 120px; object-fit: cover; margin-bottom: 10px;}
            .product-card .prod-name {font-size: 16px; font-weight: 600; margin-bottom: 6px;}
            .product-card .prod-price {font-size: 15px; color: #888; margin-bottom: 10px;}
            .product-card .select-btn {background: #c29589; color: #fff; border: none; border-radius: 8px; padding: 7px 18px; font-size: 15px; cursor: pointer; margin-top: 8px; transition: background 0.2s;}
            .product-card .select-btn:hover {background: #a97c6a;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Render all cards in a single scrolling-wrapper
        st.markdown(
            """
            <style>
            .scrolling-wrapper {overflow-x: auto; display: flex; flex-wrap: nowrap; padding-bottom: 10px;}
            .product-card {background: #fff; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-right: 18px; min-width: 220px; max-width: 220px; flex: 0 0 auto; padding: 16px; text-align: center; position: relative; transition: box-shadow 0.2s;}
            .product-card img {border-radius: 12px; width: 100%; height: 120px; object-fit: cover; margin-bottom: 10px;}
            .product-card .prod-name {font-size: 16px; font-weight: 600; margin-bottom: 6px;}
            .product-card .prod-price {font-size: 15px; color: #888; margin-bottom: 10px;}
            </style>
            """,
            unsafe_allow_html=True,
        )
        products = PRODUCT_TEMPLATES[selected_category]
        cols = st.columns(len(products))
        selected_product = st.session_state.get('selected_product')
        for idx, prod in enumerate(products):
            with cols[idx]:
                st.markdown(f"<div class='product-card'><img src='{prod['image']}' alt='{prod['name']}'/><div class='prod-name'>{prod['name']}</div><div class='prod-price'>${prod['price']}</div></div>", unsafe_allow_html=True)
                if st.button("Select", key=f"select_{selected_category}_{idx}"):
                    st.session_state['selected_product'] = prod
                    selected_product = prod

        # Autofill product details or show manual entry for 'Other'
        if selected_product:
            if selected_product['name'] == "Other":
                gift_name = st.text_input("Product Name", key="gift_name_other")
                gift_price = st.number_input("Price ($)", min_value=1, value=1, key="gift_price_other")
                product_url = st.text_input("Online Purchase URL (optional)", key="product_url_other")
                final_image_url = ""
            else:
                gift_name = st.text_input("Product Name", value=selected_product['name'], key=f"gift_name_{selected_product['name']}")
                gift_price = st.number_input("Price ($)", min_value=1, value=selected_product['price'], key=f"gift_price_{selected_product['name']}")
                product_url = st.text_input("Online Purchase URL (optional)", value=selected_product.get('website_url', ''), key=f"product_url_{selected_product['name']}")
                final_image_url = selected_product.get('image', '')
        else:
            gift_name = st.text_input("Product Name", key="gift_name_none")
            gift_price = st.number_input("Price ($)", min_value=1, value=1, key="gift_price_none")
            product_url = st.text_input("Online Purchase URL (optional)", key="product_url_none")
            final_image_url = ""

        gift_desc = st.text_area("Description (optional)")
        max_qty = st.number_input("Maximum Quantity", min_value=1, value=1)
        product_url = st.text_input("Online Purchase URL (optional)")
        allow_online = st.checkbox("Allow Online Purchase", value=True)
        allow_offline = st.checkbox("Allow Offline Purchase", value=True)

        # SAVE PRODUCT
        # If 'Other' is selected or no product selected, show image upload as last field before save
        if (selected_product and selected_product['name'] == "Other") or (not selected_product):
            st.markdown("**Product Image**")
            image_input_type = st.radio("Choose image input method:", ["Upload Image", "Paste Image URL"])
            final_image_url = ''
            uploaded_file = None
            pasted_image_url = ''
            if image_input_type == "Upload Image":
                uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])
                if uploaded_file is not None:
                    uploaded_url = upload_to_cloudinary(uploaded_file)
                    if uploaded_url:
                        st.success("Image uploaded!")
                        final_image_url = uploaded_url
                        st.image(final_image_url, caption="Uploaded Image", use_container_width=True)
            else:
                pasted_image_url = st.text_input("Paste an image URL")
                if pasted_image_url:
                    final_image_url = pasted_image_url
                    st.image(final_image_url, caption="Selected Image", use_container_width=True)

        if st.button("Save Product Gift"):
            if not gift_name:
                st.error("Product Name is required.")
                return
            if not final_image_url:
                st.error("Please upload or enter an image URL.")
                return
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO registry_items 
                    (registry_id, item_type, item_name, description, image_url,
                     target_amount, allow_online, allow_offline, product_url,
                     max_quantity, total_reserved_quantity, total_contributed_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        st.session_state.registry_id,
                        'PRODUCT',
                        gift_name,
                        gift_desc,
                        final_image_url,
                        gift_price,
                        allow_online,
                        allow_offline,
                        product_url,
                        max_qty,
                        0,  # total_reserved_quantity
                        0   # total_contributed_amount
                    ),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("Product added successfully!")
                st.session_state.page = "couple_dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Database Error: {e}")


    if gift_type == "cash":
        st.subheader("Cash Fund Details")

        fund_name = st.text_input("Fund Name")
        fund_desc = st.text_area("Description (optional)")
        target_amount = st.number_input("Total Target Amount ($)", min_value=1, value=1)

        if st.button("💾 Save Cash Fund"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                # Use static money image for cash fund
                money_img_url = "https://res.cloudinary.com/di80pp52x/image/upload/v1764467476/money_tslmib.jpg"
                cur.execute(
                    """
                    INSERT INTO registry_items 
                    (registry_id, item_type, item_name, description, image_url, target_amount,
                     allow_online, allow_offline, max_quantity, total_reserved_quantity,
                     total_contributed_amount)
                    VALUES (%s,'cash_fund',%s,%s,%s,%s,1,1,1,0,0)
                    """,
                    (st.session_state.registry_id, fund_name, fund_desc, money_img_url, target_amount),
                )

                conn.commit()
                cur.close()
                conn.close()

                st.success("Cash fund added successfully!")
                st.session_state.page = "couple_dashboard"
                st.rerun()

            except Exception as e:
                st.error(f"Database Error: {e}")
