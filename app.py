import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date
import json
from pathlib import Path

# Initialize session state for bookings if it doesn't exist
if 'bookings' not in st.session_state:
    # Try to load existing bookings from file
    booking_file = Path('bookings.json')
    if booking_file.exists():
        with open(booking_file, 'r') as f:
            st.session_state.bookings = json.load(f)
    else:
        st.session_state.bookings = {}

def save_bookings():
    """Save bookings to a JSON file"""
    with open('bookings.json', 'w') as f:
        json.dump(st.session_state.bookings, f)

# Set page configuration
st.set_page_config(page_title="Desk Booking System", layout="wide")
st.title("Desk Booking System")

# Define desk list
DESKS = ['8.1', '8.2', '8.3', '7.1', '7.2', '7.3', 
         '6.1', '6.2', '6.3', '5.1', '5.2', '5.3', 
         '9.1', '9.2']

# Create month selector
months = list(calendar.month_name)[1:]
selected_month = st.selectbox("Select Month", months)
selected_month_num = months.index(selected_month) + 1

# Get number of days in selected month for 2025
num_days = calendar.monthrange(2025, selected_month_num)[1]

# Create the booking interface
st.subheader(f"Desk Bookings for {selected_month} 2025")

# Create a DataFrame for the booking grid
days = list(range(1, num_days + 1))
data = {desk: [None] * num_days for desk in DESKS}
df = pd.DataFrame(data, index=days)

# Update DataFrame with existing bookings
for booking_key in st.session_state.bookings:
    month, day, desk = booking_key.split('_')
    if int(month) == selected_month_num:
        df.at[int(day), desk] = st.session_state.bookings[booking_key]

# Display booking form
col1, col2 = st.columns(2)
with col1:
    selected_day = st.selectbox("Select Day", days)
with col2:
    available_desks = [desk for desk in DESKS 
                      if df.at[selected_day, desk] is None]
    selected_desk = st.selectbox(
        "Select Desk", 
        available_desks if available_desks else ["No desks available"]
    )

# Add booking button
user_name = st.text_input("Your Name")
if st.button("Book Desk"):
    if not user_name:
        st.error("Please enter your name")
    elif selected_desk == "No desks available":
        st.error("No desks available for selected day")
    else:
        # Create booking key
        booking_key = f"{selected_month_num}_{selected_day}_{selected_desk}"
        st.session_state.bookings[booking_key] = user_name
        save_bookings()
        st.success(f"Desk {selected_desk} booked for {selected_month} {selected_day}, 2025")
        st.rerun()

# Display booking grid
st.subheader("Current Bookings")

# Style the DataFrame
def color_occupied(val):
    return 'background-color: #ffcccb' if pd.notnull(val) else ''

# Display styled DataFrame
st.dataframe(
    df.style.applymap(color_occupied),
    height=400
)

# Add legend
st.markdown("""
**Legend:**
- Empty cells: Available
- Red cells: Booked (shows booker's name)
""")
