import streamlit as st
import pandas as pd
import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="Activity Matcher",
    page_icon="🏆",
    layout="wide"
)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'users' not in st.session_state:
    st.session_state['users'] = []
if 'activities' not in st.session_state:
    # Sample activities data
    st.session_state['activities'] = [
        {
            "id": 1,
            "name": "Football Match",
            "type": "Sports",
            "location": "Central Park Field",
            "cost": 15.00,
            "available_slots": 22,
            "booked_slots": 14,
            "datetime": datetime.datetime.now() + datetime.timedelta(days=2),
            "vendor": "City Sports League"
        },
        {
            "id": 2,
            "name": "Chess Tournament",
            "type": "Board Games",
            "location": "Community Center",
            "cost": 10.00,
            "available_slots": 16,
            "booked_slots": 7,
            "datetime": datetime.datetime.now() + datetime.timedelta(days=1),
            "vendor": "Mind Games Club"
        },
        {
            "id": 3,
            "name": "Basketball Pickup Game",
            "type": "Sports",
            "location": "YMCA Court",
            "cost": 8.00,
            "available_slots": 10,
            "booked_slots": 6,
            "datetime": datetime.datetime.now() + datetime.timedelta(hours=12),
            "vendor": "Local YMCA"
        },
        {
            "id": 4,
            "name": "Settlers of Catan Night",
            "type": "Board Games",
            "location": "Board Game Cafe",
            "cost": 12.50,
            "available_slots": 12,
            "booked_slots": 8,
            "datetime": datetime.datetime.now() + datetime.timedelta(days=3),
            "vendor": "Dice & Drinks"
        },
    ]
if 'bookings' not in st.session_state:
    st.session_state['bookings'] = []
if 'coupons' not in st.session_state:
    st.session_state['coupons'] = {
        "NEWUSER": 0.15,  # 15% off
        "WEEKEND": 0.10,  # 10% off
        "MEMBER2024": 0.20  # 20% off
    }

# Function to handle login
def login(username, password):
    # For demo, simple login check
    user = next((user for user in st.session_state['users'] if user['username'] == username), None)
    if user and user['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = user
        return True
    return False

# Function to handle registration
def register_user(user_data):
    # Check if username already exists
    if any(user['username'] == user_data['username'] for user in st.session_state['users']):
        return False
    st.session_state['users'].append(user_data)
    return True

# Function to book an activity
def book_activity(activity_id, user_id, coupon_code=None):
    activity = next((act for act in st.session_state['activities'] if act['id'] == activity_id), None)
    if not activity or activity['available_slots'] <= activity['booked_slots']:
        return False, "Activity not found or fully booked."
    
    cost = activity['cost']
    discount = 0
    
    if coupon_code and coupon_code in st.session_state['coupons']:
        discount = cost * st.session_state['coupons'][coupon_code]
        cost -= discount
    
    booking = {
        "id": len(st.session_state['bookings']) + 1,
        "activity_id": activity_id,
        "user_id": user_id,
        "booking_time": datetime.datetime.now(),
        "original_cost": activity['cost'],
        "discount": discount,
        "final_cost": cost,
        "coupon_applied": coupon_code if coupon_code else "None"
    }
    
    st.session_state['bookings'].append(booking)
    
    # Update booked slots
    for act in st.session_state['activities']:
        if act['id'] == activity_id:
            act['booked_slots'] += 1
            break
    
    return True, booking

# Main app layout
def main():
    st.sidebar.title("Activity Matcher 🏆")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Home", "Register", "Login", "Browse Activities", "My Bookings", "Vendor Dashboard"])
    
    # Home page
    if page == "Home":
        st.title("Welcome to Activity Matcher!")
        st.header("Connect, Play, Enjoy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Find Your Next Activity")
            st.write("""
            Whether you're looking to join a football match, play board games, 
            or try something new, Activity Matcher connects you with events in your area.
            """)
            
            # Featured activities
            st.subheader("Featured Activities")
            for i, activity in enumerate(st.session_state['activities'][:2]):
                with st.expander(f"{activity['name']} - {activity['datetime'].strftime('%b %d, %Y')}"):
                    st.write(f"**Type:** {activity['type']}")
                    st.write(f"**Location:** {activity['location']}")
                    st.write(f"**Cost:** ${activity['cost']:.2f}")
                    st.write(f"**Available:** {activity['available_slots'] - activity['booked_slots']} slots")
                    
                    if st.session_state['logged_in']:
                        if st.button(f"Book Now", key=f"book_featured_{i}"):
                            success, result = book_activity(activity['id'], st.session_state['current_user']['id'])
                            if success:
                                st.success("Activity booked successfully!")
                            else:
                                st.error(result)
                    else:
                        st.info("Please login to book activities")
        
        with col2:
            st.image("https://via.placeholder.com/400x300?text=Activity+Image", caption="Join the fun!")
            
            # How it works
            st.subheader("How it works")
            st.markdown("""
            1. **Register** - Create your profile with your interests
            2. **Browse** - Find activities that match your preferences
            3. **Book** - Secure your spot with our easy booking system
            4. **Play** - Enjoy your activity with new friends
            """)
    
    # Registration page
    elif page == "Register":
        st.title("Create Your Account")
        
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=16, max_value=100, value=25)
                phone = st.text_input("Phone Number")
                gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
            
            with col2:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
            st.subheader("Activity Preferences")
            activities_pref = st.multiselect(
                "Select activities you enjoy", 
                ["Football", "Basketball", "Tennis", "Chess", "Board Games", "Card Games", "Volleyball", "Badminton"]
            )
            
            st.subheader("Availability")
            col3, col4 = st.columns(2)
            with col3:
                preferred_days = st.multiselect(
                    "Preferred days", 
                    ["Weekdays", "Weekends", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                )
            with col4:
                preferred_times = st.multiselect(
                    "Preferred times",
                    ["Morning", "Afternoon", "Evening", "Night"]
                )
            
            location = st.text_input("Your Location (City/Area)")
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif not name or not username or not password:
                    st.error("Please fill in all required fields!")
                else:
                    user_data = {
                        "id": len(st.session_state['users']) + 1,
                        "name": name,
                        "age": age,
                        "phone": phone,
                        "gender": gender,
                        "username": username,
                        "password": password,
                        "activities_pref": activities_pref,
                        "preferred_days": preferred_days,
                        "preferred_times": preferred_times,
                        "location": location,
                        "joined_date": datetime.datetime.now(),
                        "membership_status": "Basic"
                    }
                    
                    if register_user(user_data):
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("Username already exists. Please choose another.")
    
    # Login page
    elif page == "Login":
        if st.session_state['logged_in']:
            st.success(f"You are already logged in as {st.session_state['current_user']['name']}!")
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['current_user'] = None
                st.experimental_rerun()
        else:
            st.title("Login to Your Account")
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    if login(username, password):
                        st.success("Login successful!")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")
            
            st.info("Don't have an account? Go to the Register page to create one!")
    
    # Browse Activities page
    elif page == "Browse Activities":
        st.title("Browse Activities")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            activity_type = st.selectbox("Activity Type", ["All"] + list(set(act['type'] for act in st.session_state['activities'])))
        with col2:
            time_filter = st.selectbox("Time Frame", ["All", "Today", "This Week", "This Month"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Date", "Cost: Low to High", "Cost: High to Low", "Availability"])
        
        # Filter activities
        filtered_activities = st.session_state['activities']
        if activity_type != "All":
            filtered_activities = [act for act in filtered_activities if act['type'] == activity_type]
        
        if time_filter == "Today":
            today = datetime.datetime.now().date()
            filtered_activities = [act for act in filtered_activities if act['datetime'].date() == today]
        elif time_filter == "This Week":
            today = datetime.datetime.now().date()
            end_of_week = today + datetime.timedelta(days=(6-today.weekday()))
            filtered_activities = [act for act in filtered_activities if today <= act['datetime'].date() <= end_of_week]
        
        # Sort activities
        if sort_by == "Date":
            filtered_activities.sort(key=lambda x: x['datetime'])
        elif sort_by == "Cost: Low to High":
            filtered_activities.sort(key=lambda x: x['cost'])
        elif sort_by == "Cost: High to Low":
            filtered_activities.sort(key=lambda x: x['cost'], reverse=True)
        elif sort_by == "Availability":
            filtered_activities.sort(key=lambda x: x['available_slots'] - x['booked_slots'], reverse=True)
        
        # Display activities
        if not filtered_activities:
            st.info("No activities match your criteria")
        else:
            for activity in filtered_activities:
                with st.expander(f"{activity['name']} - {activity['datetime'].strftime('%b %d, %Y at %I:%M %p')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(activity['name'])
                        st.write(f"**Type:** {activity['type']}")
                        st.write(f"**Location:** {activity['location']}")
                        st.write(f"**Vendor:** {activity['vendor']}")
                        st.write(f"**Date & Time:** {activity['datetime'].strftime('%b %d, %Y at %I:%M %p')}")
                        st.write(f"**Cost:** ${activity['cost']:.2f}")
                        
                        # Show availability
                        available = activity['available_slots'] - activity['booked_slots']
                        st.write(f"**Availability:** {available} slots out of {activity['available_slots']}")
                        st.progress(activity['booked_slots'] / activity['available_slots'])
                    
                    with col2:
                        st.image(f"https://via.placeholder.com/200x150?text={activity['type']}", caption=activity['type'])
                        
                        if st.session_state['logged_in']:
                            coupon_code = st.text_input("Coupon Code (if any)", key=f"coupon_{activity['id']}")
                            
                            if st.button("Book Now", key=f"book_{activity['id']}"):
                                success, result = book_activity(
                                    activity['id'], 
                                    st.session_state['current_user']['id'],
                                    coupon_code
                                )
                                if success:
                                    st.success("Activity booked successfully!")
                                    if coupon_code and coupon_code in st.session_state['coupons']:
                                        discount_percent = st.session_state['coupons'][coupon_code] * 100
                                        st.info(f"Coupon applied: {discount_percent:.0f}% discount")
                                else:
                                    st.error(result)
                        else:
                            st.info("Please login to book activities")
    
    # My Bookings page
    elif page == "My Bookings":
        st.title("My Bookings")
        
        if not st.session_state['logged_in']:
            st.warning("Please login to view your bookings")
        else:
            user_id = st.session_state['current_user']['id']
            user_bookings = [b for b in st.session_state['bookings'] if b['user_id'] == user_id]
            
            if not user_bookings:
                st.info("You haven't made any bookings yet.")
                st.write("Go to the Browse Activities page to find and book activities.")
            else:
                # Tab Navigation
                tabs = st.tabs(["Upcoming", "Past"])
                
                with tabs[0]:
                    st.subheader("Upcoming Bookings")
                    upcoming_bookings = []
                    
                    for booking in user_bookings:
                        activity = next((a for a in st.session_state['activities'] if a['id'] == booking['activity_id']), None)
                        if activity and activity['datetime'] > datetime.datetime.now():
                            upcoming_bookings.append((booking, activity))
                    
                    if not upcoming_bookings:
                        st.info("No upcoming bookings")
                    else:
                        for booking, activity in upcoming_bookings:
                            with st.expander(f"{activity['name']} - {activity['datetime'].strftime('%b %d, %Y')}"):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**Activity:** {activity['name']}")
                                    st.write(f"**Location:** {activity['location']}")
                                    st.write(f"**Date & Time:** {activity['datetime'].strftime('%b %d, %Y at %I:%M %p')}")
                                    st.write(f"**Original Cost:** ${booking['original_cost']:.2f}")
                                    if booking['discount'] > 0:
                                        st.write(f"**Discount Applied:** ${booking['discount']:.2f} ({booking['coupon_applied']})")
                                    st.write(f"**Final Cost:** ${booking['final_cost']:.2f}")
                                
                                with col2:
                                    st.write(f"**Booking ID:** {booking['id']}")
                                    st.write(f"**Booked on:** {booking['booking_time'].strftime('%b %d, %Y')}")
                                    if st.button("Cancel Booking", key=f"cancel_{booking['id']}"):
                                        st.warning("This is a mock cancellation. In a real application, this would cancel your booking.")
                
                with tabs[1]:
                    st.subheader("Past Bookings")
                    past_bookings = []
                    
                    for booking in user_bookings:
                        activity = next((a for a in st.session_state['activities'] if a['id'] == booking['activity_id']), None)
                        if activity and activity['datetime'] <= datetime.datetime.now():
                            past_bookings.append((booking, activity))
                    
                    if not past_bookings:
                        st.info("No past bookings")
                    else:
                        for booking, activity in past_bookings:
                            with st.expander(f"{activity['name']} - {activity['datetime'].strftime('%b %d, %Y')}"):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**Activity:** {activity['name']}")
                                    st.write(f"**Location:** {activity['location']}")
                                    st.write(f"**Date & Time:** {activity['datetime'].strftime('%b %d, %Y at %I:%M %p')}")
                                    st.write(f"**Cost:** ${booking['final_cost']:.2f}")
                                
                                with col2:
                                    st.write(f"**Booking ID:** {booking['id']}")
                                    st.write(f"**Booked on:** {booking['booking_time'].strftime('%b %d, %Y')}")
                                    if st.button("Rate Activity", key=f"rate_{booking['id']}"):
                                        st.write("Rating functionality would go here")
    
    # Vendor Dashboard
    elif page == "Vendor Dashboard":
        st.title("Vendor Dashboard")
        
        st.info("This is a mockup of the vendor interface. In a real application, vendors would have their own login.")
        
        tabs = st.tabs(["My Activities", "Manage Bookings", "Add New Activity"])
        
        with tabs[0]:
            st.subheader("My Activities")
            
            vendor_name = st.selectbox("Select Vendor", list(set(act['vendor'] for act in st.session_state['activities'])))
            vendor_activities = [act for act in st.session_state['activities'] if act['vendor'] == vendor_name]
            
            for activity in vendor_activities:
                with st.expander(f"{activity['name']} - {activity['datetime'].strftime('%b %d, %Y')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Activity Type:** {activity['type']}")
                        st.write(f"**Location:** {activity['location']}")
                        st.write(f"**Date & Time:** {activity['datetime'].strftime('%b %d, %Y at %I:%M %p')}")
                        st.write(f"**Cost per Person:** ${activity['cost']:.2f}")
                        
                        bookings = len([b for b in st.session_state['bookings'] if b['activity_id'] == activity['id']])
                        st.write(f"**Bookings:** {bookings}")
                        st.write(f"**Capacity:** {activity['booked_slots']}/{activity['available_slots']} slots filled")
                        st.progress(activity['booked_slots'] / activity['available_slots'])
                    
                    with col2:
                        st.write(f"**Activity ID:** {activity['id']}")
                        if st.button("Edit Activity", key=f"edit_{activity['id']}"):
                            st.write("Edit functionality would go here")
                        if st.button("Cancel Activity", key=f"cancel_act_{activity['id']}"):
                            st.warning("This would cancel the activity and notify all participants")
        
        with tabs[1]:
            st.subheader("Manage Bookings")
            
            vendor_name = st.selectbox("Select Vendor", list(set(act['vendor'] for act in st.session_state['activities'])), key="vendor_bookings")
            vendor_activities = [act for act in st.session_state['activities'] if act['vendor'] == vendor_name]
            
            activity_id = st.selectbox(
                "Select Activity", 
                [(act['id'], f"{act['name']} - {act['datetime'].strftime('%b %d, %Y')}") for act in vendor_activities],
                format_func=lambda x: x[1]
            )
            
            if activity_id:
                activity_id = activity_id[0]
                activity_bookings = [b for b in st.session_state['bookings'] if b['activity_id'] == activity_id]
                
                if not activity_bookings:
                    st.info("No bookings for this activity yet")
                else:
                    st.write(f"Total Bookings: {len(activity_bookings)}")
                    
                    booking_data = []
                    for booking in activity_bookings:
                        user = next((u for u in st.session_state['users'] if u['id'] == booking['user_id']), {"name": "Unknown", "phone": "Unknown"})
                        booking_data.append({
                            "Booking ID": booking['id'],
                            "User Name": user['name'],
                            "Phone": user['phone'],
                            "Booking Date": booking['booking_time'].strftime('%b %d, %Y'),
                            "Amount Paid": f"${booking['final_cost']:.2f}"
                        })
                    
                    st.dataframe(pd.DataFrame(booking_data))
        
        with tabs[2]:
            st.subheader("Add New Activity")
            
            with st.form("add_activity_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    activity_name = st.text_input("Activity Name")
                    activity_type = st.selectbox(
                        "Activity Type", 
                        ["Sports", "Board Games", "Card Games", "Outdoor Adventure", "Other"]
                    )
                    location = st.text_input("Location")
                    vendor_name = st.selectbox("Vendor Name", list(set(act['vendor'] for act in st.session_state['activities'])))
                
                with col2:
                    activity_date = st.date_input("Date", value=datetime.datetime.now().date() + datetime.timedelta(days=1))
                    activity_time = st.time_input("Time", value=datetime.time(18, 0))
                    cost = st.number_input("Cost per Person ($)", min_value=0.0, value=15.0, step=0.5)
                    capacity = st.number_input("Capacity (slots)", min_value=1, value=20)
                
                submit_button = st.form_submit_button("Add Activity")
                
                if submit_button:
                    if not activity_name or not location:
                        st.error("Please fill in all required fields!")
                    else:
                        activity_datetime = datetime.datetime.combine(activity_date, activity_time)
                        new_activity = {
                            "id": len(st.session_state['activities']) + 1,
                            "name": activity_name,
                            "type": activity_type,
                            "location": location,
                            "cost": cost,
                            "available_slots": capacity,
                            "booked_slots": 0,
                            "datetime": activity_datetime,
                            "vendor": vendor_name
                        }
                        
                        st.session_state['activities'].append(new_activity)
                        st.success("Activity added successfully!")

# Run the app
if __name__ == "__main__":
    main()
