import streamlit as st
import os
from PIL import Image

# Function to display suitable cards
def display_cards(income, folder_mapping):
    if income < 2000:
        st.warning("Net income is below the minimum range for Maybank cards.")
        return

    # Determine income range and corresponding folder
    for income_range, folder in folder_mapping.items():
        if isinstance(income_range, tuple) and income_range[0] <= income <= income_range[1]:
            st.markdown(f"### Cards for Income Range: {income_range[0]} - {income_range[1]} MYR")
            card_folder = folder
            break
    else:
        if income >= 5000:
            st.markdown("### Cards for Income Range: 5000+ MYR")
            card_folder = folder_mapping['5000+']

    # Display card images from the folder
    if os.path.exists(card_folder):
        card_dirs = [os.path.join(card_folder, d) for d in os.listdir(card_folder) if os.path.isdir(os.path.join(card_folder, d))]
        
        for card_dir in card_dirs:
            # Load card image and name
            image_path = os.path.join(card_dir, "image.png")
            name_path = os.path.join(card_dir, "name.txt")

            if os.path.exists(image_path) and os.path.exists(name_path):
                card_image = Image.open(image_path)
                with open(name_path, "r") as f:
                    card_name = f.read().strip()

                # Center card layout
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="data:image/png;base64,{image_to_base64(image_path)}" alt="{card_name}" style="width: 300px; margin-bottom: 10px;" />
                        <p style="font-size: 16px; font-weight: bold;">{card_name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Expander for card details below the card
                with st.expander(f"View Details for {card_name}"):
                    cover_image_path = os.path.join(card_dir, "cover-image.png")
                    details_path = os.path.join(card_dir, "details.txt")

                    # Display larger cover image
                    if os.path.exists(cover_image_path):
                        cover_image = Image.open(cover_image_path)
                        st.image(cover_image, use_column_width=True, caption="Card Cover Image")  # Larger cover image

                    # Display card details
                    if os.path.exists(details_path):
                        with open(details_path, "r") as f:
                            details = f.read()
                        st.markdown(f"<p style='font-size:14px;'>{details}</p>", unsafe_allow_html=True)
    else:
        st.error("No cards found for this income range.")

import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")



# Initialize session state for UI toggle
if "show_cards" not in st.session_state:
    st.session_state.show_cards = False

# App title
st.markdown('<h1 class="title" style="text-align: center; color: #4CAF50;">Income Calculator</h1>', unsafe_allow_html=True)

# If the button has not been clicked, show the form
if not st.session_state.show_cards:
    # Income Details
    st.markdown("<h3 style='color:#4CAF50;'>Income Details</h3>", unsafe_allow_html=True)
    gross_income = st.number_input("Gross Income (Basic Salary + Fixed Allowance) (MYR)", min_value=0.0, value=0.0, step=0.01)
    other_income = st.number_input("Other Income (MYR)", min_value=0.0, value=0.0, step=0.01)
    total_income = gross_income + other_income
    st.markdown(f"<h4 style='color:#4CAF50;'>Total Income (MYR): {total_income:.2f}</h4>", unsafe_allow_html=True)

    # Divider line for better separation of sections
    st.markdown("---")

    # Input fields for deductions
    st.markdown("<h3 style='color:#F39C12;'>Deductions</h3>", unsafe_allow_html=True)
    epf = st.number_input("EPF (MYR)", min_value=0.0, value=0.0, step=0.01)
    socso = st.number_input("SOCSO (MYR)", min_value=0.0, value=0.0, step=0.01)
    monthly_deductions = st.number_input("Monthly Deductions (MYR)", min_value=0.0, value=0.0, step=0.01)
    other_deductions = st.number_input("Others (e.g., PTPTN, AEON CREDIT, COWAY) (MYR)", min_value=0.0, value=0.0, step=0.01)
    total_deduction = epf + socso + monthly_deductions + other_deductions
    st.markdown(f"<h4 style='color:#F39C12;'>Total Deductions (MYR): {total_deduction:.2f}</h4>", unsafe_allow_html=True)

    # Divider line for net income calculation
    st.markdown("---")

    # Net Income Calculation
    net_income = total_income - total_deduction
    st.markdown(f"<h4 style='color:#2ECC71;'>Net Income (MYR): {net_income:.2f}</h4>", unsafe_allow_html=True)

    # Button to show cards
    if st.button("Show Suitable Maybank Cards"):
        st.session_state.show_cards = True  # Update state to show the cards page
        st.session_state.net_income = net_income  # Store net income in session state
else:
    # Cards display page
    net_income = st.session_state.net_income
    folder_mapping = {
        (2000, 2900): "2000-2900",  # Folder for 2000-2900 range
        (3000, 4900): "3000-4900",  # Folder for 3000-4900 range
        '5000+': "5000+"           # Folder for 5000+ range
    }

    st.markdown("<h2 style='color:#4CAF50;'>Suitable Maybank Cards</h2>", unsafe_allow_html=True)
    display_cards(net_income, folder_mapping)

    # Back button to return to the form
    if st.button("Back to Calculator"):
        st.session_state.show_cards = False  # Reset the state to show the form again

