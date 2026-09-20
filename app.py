
from backend_agent import main
import streamlit as st
import requests

from agents import Runner


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .info-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .product-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    .success-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #28a745;
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD AI AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return main()


ecommerce_agent = get_agent()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 E-Commerce Customer Support</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Get product information, ask questions, or submit an order request.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# HERO IMAGE
# ============================================================

st.image(
    "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d"
    "?auto=format&fit=crop&w=1600&q=80",
    use_container_width=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📌 Navigation")

    option = st.radio(
        "What would you like to do?",
        [
            "Chatbot",
            "Send a Request"
        ]
    )

    st.divider()

    if option == "Chatbot":

        st.subheader("💬 Example Questions")

        st.write("• What products do you sell?")
        st.write("• How much is a bag of cement?")
        st.write("• Do you deliver to Benin City?")
        st.write("• How can I place an order?")
        st.write("• What payment methods do you accept?")

    else:

        st.subheader("🛒 Order Information")

        st.info(
            "Fill in the customer and product information below "
            "to submit an order request."
        )


# ============================================================
# CHATBOT
# ============================================================

if option == "Chatbot":

    st.markdown(
        '<div class="section-title">💬 Chat with our AI Assistant</div>',
        unsafe_allow_html=True
    )

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])


    # Chat input
    user_message = st.chat_input(
        "Ask about our products, prices, delivery, or orders..."
    )


    if user_message:

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )


        # Display user message
        with st.chat_message("user"):
            st.write(user_message)


        # Run AI agent ONCE
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                result = Runner.run_sync(
                    ecommerce_agent,
                    user_message
                )

                final_response = result.final_output

                st.write(final_response)


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_response
            }
        )


# ============================================================
# ORDER REQUEST
# ============================================================

else:

    st.markdown(
        '<div class="section-title">🛒 Send an Order Request</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter the customer details and the products being ordered."
    )


    # --------------------------------------------------------
    # CUSTOMER INFORMATION
    # --------------------------------------------------------

    st.subheader("👤 Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        customer_name = st.text_input(
            "Customer Name",
            placeholder="Enter customer's full name"
        )

        customer_email = st.text_input(
            "Customer Email",
            placeholder="example@gmail.com"
        )

        customer_phone = st.text_input(
            "Customer Phone",
            placeholder="08012345678"
        )


    with col2:

        delivery_address = st.text_input(
            "Delivery Address",
            placeholder="Enter delivery address"
        )

        amount = st.number_input(
            "Total Amount",
            min_value=0.0,
            step=1000.0,
            format="%.2f"
        )

        order_reference = st.text_input(
            "Order Reference",
            placeholder="ORD-0016"
        )


    st.divider()


    # --------------------------------------------------------
    # PRODUCT INFORMATION
    # --------------------------------------------------------

    st.subheader("📦 Product Information")

    products_num = st.number_input(
        "Number of Products",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


    products = []


    for i in range(int(products_num)):

        st.markdown(
            f"### Product {i + 1}"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            product_name = st.text_input(
                "Product Name",
                key=f"product_name_{i}",
                placeholder="e.g. Cement"
            )


        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1,
                key=f"quantity_{i}"
            )


        with col3:

            unit_price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=0.0,
                step=500.0,
                key=f"unit_price_{i}"
            )


        products.append(
            {
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price
            }
        )


    st.divider()


    # --------------------------------------------------------
    # ORDER SUMMARY
    # --------------------------------------------------------

    st.subheader("📋 Order Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.metric(
            "Products",
            len(products)
        )


    with summary_col2:

        total_quantity = sum(
            product["quantity"]
            for product in products
        )

        st.metric(
            "Total Quantity",
            total_quantity
        )


    with summary_col3:

        calculated_total = sum(
            product["quantity"] * product["unit_price"]
            for product in products
        )

        st.metric(
            "Calculated Total",
            f"₦{calculated_total:,.2f}"
        )


    # --------------------------------------------------------
    # SEND REQUEST
    # --------------------------------------------------------

    st.subheader("🚀 Submit Request")


    if st.button(
        "📤 Send Order Request",
        use_container_width=True,
        type="primary"
    ):

        # Basic validation
        if not customer_name.strip():

            st.error("Please enter the customer name.")

        elif not customer_email.strip():

            st.error("Please enter the customer email.")

        elif not customer_phone.strip():

            st.error("Please enter the customer phone number.")

        elif not delivery_address.strip():

            st.error("Please enter the delivery address.")

        elif not order_reference.strip():

            st.error("Please enter the order reference.")

        elif any(
            product["product_name"].strip() == ""
            for product in products
        ):

            st.error("Please enter a name for every product.")

        else:

            # ------------------------------------------------
            # CREATE ORDER
            # ------------------------------------------------

            order = {

                "customer_name": customer_name,

                "customer_email": customer_email,

                "customer_phone": customer_phone,

                "delivery_address": delivery_address,

                "amount": amount,

                "payment_status": "pending",

                "delivery_status": "pending",

                "rider_id": None,

                "order_reference": order_reference,

                "products": products
            }


            # ------------------------------------------------
            # SEND TO N8N
            # ------------------------------------------------

            webhook_url = (
                "https://startle-alive-unease.ngrok-free.dev"
                "/webhook-test/"
                "c3305ae5-101d-4434-a53c-d8d752c11956"
            )


            with st.spinner("Sending order request..."):

                try:

                    response = requests.post(
                        webhook_url,
                        json=order,
                        timeout=30
                    )


                    if response.status_code == 200:

                        st.success(
                            "✅ Order request sent successfully!"
                        )

                        st.balloons()


                    else:

                        st.error(
                            f"❌ Request failed. "
                            f"Status code: {response.status_code}"
                        )

                        st.write(
                            "n8n response:"
                        )

                        st.code(
                            response.text
                        )


                except requests.exceptions.RequestException as error:

                    st.error(
                        "❌ Could not connect to the n8n webhook."
                    )

                    st.code(
                        str(error)
                    )

