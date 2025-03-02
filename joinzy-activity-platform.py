import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Joinzy! - Activity Matching Platform",
    page_icon="🎮",
    layout="wide"
)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'users' not in st.session_state:
    st.session_state['users'] = [
        {
            "id": 1,
            "name": "John Doe",
            "age": 28,
            "phone": "555-123-4567",
            "gender": "Male",
            "username": "johnd",
            "password": "password",
            "activities_pref": ["Football", "Basketball"],
            "preferred_days": ["Weekends"],
            "preferred_times": ["Evening"],
            "location": "Downtown",
            "joined_date": datetime.datetime.now() - datetime.timedelta(days=30),
            "membership_status": "Premium"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "age": 24,
            "phone": "555-987-6543",
            "gender": "Female",
            "username": "janes",
            "password": "password",
            "activities_pref": ["Board Games", "Chess"],
            "preferred_days": ["Weekdays"],
            "preferred_times": ["Evening"],
            "location": "Uptown",
            "joined_date": datetime.datetime.now() - datetime.timedelta(days=15),
            "membership_status": "Basic"
        }
    ]
if 'parties' not in st.session_state:
    st.session_state['parties'] = [
        {
            "id": 1,
            "name": "Saturday Football Match",
            "activity_type": "Football",
            "date": datetime.date(2025, 3, 8),
            "start_time": datetime.time(16, 0),
            "end_time": datetime.time(18, 0),
            "location": "Central Park Field",
            "max_participants": 10,
            "current_participants": 7,
            "creator_id": 1,
            "participants": [1],
            "description": "Casual 5-a-side football match. All skill levels welcome!",
            "cost_per_person": 12.50,
            "venue_booked": True
        },
        {
            "id": 2,
            "name": "Chess Tournament",
            "activity_type": "Chess",
            "date": datetime.date(2025, 3, 5),
            "start_time": datetime.time(18, 0),
            "end_time": datetime.time(21, 0),
            "location": "Gamesmith Cafe",
            "max_participants": 8,
            "current_participants": 5,
            "creator_id": 2,
            "participants": [2],
            "description": "Weekly chess tournament. Prizes for the top three players!",
            "cost_per_person": 8.00,
            "venue_booked": True
        },
        {
            "id": 3,
            "name": "Catan Night",
            "activity_type": "Board Games",
            "date": datetime.date(2025, 3, 4),
            "start_time": datetime.time(19, 0),
            "end_time": datetime.time(22, 0),
            "location": "Dice & Drinks",
            "max_participants": 4,
            "current_participants": 3,
            "creator_id": 2,
            "participants": [2],
            "description": "Looking for players to join a game of Settlers of Catan. Experience preferred.",
            "cost_per_person": 10.00,
            "venue_booked": True
        }
    ]
if 'venues' not in st.session_state:
    st.session_state['venues'] = [
        {
            "id": 1,
            "name": "Central Park Field",
            "activity_types": ["Football", "Basketball", "Volleyball"],
            "cost_per_hour": 50.00,
            "max_capacity": 20,
            "address": "123 Park Ave, City Center",
            "available_hours": ["09:00-22:00"]
        },
        {
            "id": 2,
            "name": "Gamesmith Cafe",
            "activity_types": ["Board Games", "Chess", "Card Games"],
            "cost_per_hour": 20.00,
            "cost_per_person": 5.00,
            "max_capacity": 30,
            "address": "456 Game St, Uptown",
            "available_hours": ["12:00-00:00"]
        },
        {
            "id": 3,
            "name": "Dice & Drinks",
            "activity_types": ["Board Games", "Card Games"],
            "cost_per_hour": 0.00,
            "cost_per_person": 10.00,
            "max_capacity": 40,
            "address": "789 Dice Blvd, Downtown",
            "available_hours": ["16:00-02:00"]
        },
        {
            "id": 4,
            "name": "YMCA Court",
            "activity_types": ["Basketball", "Volleyball", "Badminton"],
            "cost_per_hour": 40.00,
            "max_capacity": 20,
            "address": "321 Sports Rd, City Center",
            "available_hours": ["08:00-21:00"]
        }
    ]
if 'activity_types' not in st.session_state:
    st.session_state['activity_types'] = [
        "Football", "Basketball", "Volleyball", "Tennis", "Badminton",
        "Board Games", "Chess", "Card Games", "Role-Playing Games"
    ]
if 'coupons' not in st.session_state:
    st.session_state['coupons'] = {
        "WELCOME": 0.15,  # 15% off
        "WEEKEND": 0.10,  # 10% off
        "PREMIUM": 0.20   # 20% off for premium members
    }
if 'activity_images' not in st.session_state:
    # In a real app, these would be proper image paths
    st.session_state['activity_images'] = {
        "Football": "/api/placeholder/100/100?text=Football",
        "Basketball": "/api/placeholder/100/100?text=Basketball",
        "Volleyball": "/api/placeholder/100/100?text=Volleyball",
        "Tennis": "/api/placeholder/100/100?text=Tennis",
        "Badminton": "/api/placeholder/100/100?text=Badminton",
        "Board Games": "/api/placeholder/100/100?text=Board+Games",
        "Chess": "/api/placeholder/100/100?text=Chess",
        "Card Games": "/api/placeholder/100/100?text=Card+Games",
        "Role-Playing Games": "/api/placeholder/100/100?text=RPGs"
    }

# Function to handle login
def login(username, password):
    user = next((user for user in st.session_state['users'] if user['username'] == username), None)
    if user and user['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = user
        return True
    return False

# Function to handle registration
def register_user(user_data):
    if any(user['username'] == user_data['username'] for user in st.session_state['users']):
        return False
    st.session_state['users'].append(user_data)
    return True

# Function to create a new party
def create_party(party_data):
    st.session_state['parties'].append(party_data)
    return True

# Function to join a party
def join_party(party_id, user_id):
    for party in st.session_state['parties']:
        if party['id'] == party_id:
            if party['current_participants'] < party['max_participants']:
                if user_id not in party['participants']:
                    party['participants'].append(user_id)
                    party['current_participants'] += 1
                    return True, "Successfully joined the party!"
                else:
                    return False, "You are already in this party."
            else:
                return False, "Party is already full."
    return False, "Party not found."

# Function to leave a party
def leave_party(party_id, user_id):
    for party in st.session_state['parties']:
        if party['id'] == party_id:
            if user_id in party['participants']:
                party['participants'].remove(user_id)
                party['current_participants'] -= 1
                return True, "Successfully left the party."
            else:
                return False, "You are not in this party."
    return False, "Party not found."

# Function to calculate party cost
def calculate_party_cost(party_id, apply_coupon=None):
    party = next((p for p in st.session_state['parties'] if p['id'] == party_id), None)
    if not party:
        return None
    
    base_cost = party['cost_per_person']
    discount = 0
    
    # Apply coupon if valid
    if apply_coupon and apply_coupon in st.session_state['coupons']:
        discount = base_cost * st.session_state['coupons'][apply_coupon]
    
    # Apply premium member discount
    if st.session_state['logged_in'] and st.session_state['current_user']['membership_status'] == "Premium":
        premium_discount = base_cost * 0.10  # 10% discount for premium members
        discount = max(discount, premium_discount)  # Take the higher discount
    
    final_cost = base_cost - discount
    return {
        "base_cost": base_cost,
        "discount": discount,
        "final_cost": final_cost
    }

# Main app layout
def main():
    # Sidebar navigation
    st.sidebar.title("Joinzy! 🎮")
    st.sidebar.markdown("*Connect, Play, Enjoy*")
    
    nav_options = ["Home"]
    if not st.session_state['logged_in']:
        nav_options.extend(["Login", "Register"])
    else:
        nav_options.extend(["My Profile", "My Parties", "Create Party"])
    
    page = st.sidebar.radio("Navigation", nav_options)
    
    # Display user info in sidebar if logged in
    if st.session_state['logged_in']:
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"Welcome, {st.session_state['current_user']['name']}!")
        membership = st.session_state['current_user']['membership_status']
        if membership == "Premium":
            st.sidebar.markdown("✨ **Premium Member** ✨")
        else:
            st.sidebar.markdown("Basic Member")
            st.sidebar.markdown("[Upgrade to Premium]()")
        
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = None
            st.experimental_rerun()
    
    # Home page
    if page == "Home":
        st.title("Joinzy! - Activity Matching Platform")
        st.markdown("### Find your perfect activity partner!")
        
        # Main features as described
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Activity type filter
            selected_activity = st.selectbox(
                "Activity Type", 
                ["All"] + st.session_state['activity_types']
            )
            
            # Create/Search buttons
            if st.session_state['logged_in']:
                if st.button("Create New Party", key="home_create"):
                    st.session_state['page'] = "Create Party"
                    st.experimental_rerun()
            else:
                st.info("Please login to create parties")
            
            st.button("Search Parties", key="home_search")
            
            # Quick filters
            st.markdown("### Quick Filters")
            st.checkbox("Today only")
            st.checkbox("Near me")
            st.checkbox("Available slots")
            
            # Information box
            st.markdown("---")
            st.info("""
            **How It Works**
            1. Browse activities
            2. Join an existing party or create your own
            3. Meet new people and enjoy your activity!
            """)
        
        with col2:
            # Activity Summary Table
            st.markdown("### Available Activities")
            
            # Filter parties based on selected activity
            filtered_parties = st.session_state['parties']
            if selected_activity != "All":
                filtered_parties = [p for p in filtered_parties if p['activity_type'] == selected_activity]
            
            if not filtered_parties:
                st.info(f"No {selected_activity} activities available at the moment.")
                st.markdown("Why not create one?")
            else:
                # Create columns for the table
                for party in filtered_parties:
                    col_img, col_details, col_actions = st.columns([1, 3, 1])
                    
                    with col_img:
                        # Display activity image
                        img_path = st.session_state['activity_images'].get(party['activity_type'], "/api/placeholder/100/100?text=Activity")
                        st.image(img_path, width=100)
                    
                    with col_details:
                        st.subheader(party['name'])
                        
                        # Activity details
                        details_col1, details_col2 = st.columns(2)
                        
                        with details_col1:
                            st.markdown(f"**Activity:** {party['activity_type']}")
                            st.markdown(f"**Date:** {party['date'].strftime('%d/%m/%Y')}")
                            st.markdown(f"**Time:** {party['start_time'].strftime('%H:%M')} - {party['end_time'].strftime('%H:%M')}")
                        
                        with details_col2:
                            st.markdown(f"**Location:** {party['location']}")
                            st.markdown(f"**Participants:** {party['current_participants']}/{party['max_participants']}")
                            st.markdown(f"**Cost:** ${party['cost_per_person']:.2f} per person")
                        
                        # Progress bar for participants
                        progress = party['current_participants'] / party['max_participants']
                        st.progress(progress)
                    
                    with col_actions:
                        if st.session_state['logged_in']:
                            user_id = st.session_state['current_user']['id']
                            if user_id in party['participants']:
                                if st.button("Leave", key=f"leave_{party['id']}"):
                                    success, message = leave_party(party['id'], user_id)
                                    if success:
                                        st.success(message)
                                    else:
                                        st.error(message)
                            else:
                                if st.button("Join", key=f"join_{party['id']}"):
                                    success, message = join_party(party['id'], user_id)
                                    if success:
                                        st.success(message)
                                    else:
                                        st.error(message)
                        else:
                            st.info("Login to join")
                    
                    st.markdown("---")
    
    # Login page
    elif page == "Login":
        st.title("Login")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
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
            
            st.markdown("Don't have an account? Register now!")
        
        with col2:
            st.image("/api/placeholder/300/300?text=Joinzy+Login", caption="Find your activity partners")
    
    # Register page
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
                location = st.text_input("Your Location")
            
            st.subheader("Activity Preferences")
            activities_pref = st.multiselect(
                "Select activities you enjoy", 
                st.session_state['activity_types']
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
                        # Automatically redirect to login
                        login(username, password)
                        st.experimental_rerun()
                    else:
                        st.error("Username already exists. Please choose another.")
    
    # My Profile page (only accessible when logged in)
    elif page == "My Profile" and st.session_state['logged_in']:
        user = st.session_state['current_user']
        
        st.title("My Profile")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("/api/placeholder/200/200?text=Profile", width=200)
            st.markdown(f"**Member since:** {user['joined_date'].strftime('%B %d, %Y')}")
            st.markdown(f"**Membership:** {user['membership_status']}")
            
            if user['membership_status'] != "Premium":
                st.button("Upgrade to Premium")
        
        with col2:
            with st.expander("Personal Information", expanded=True):
                st.markdown(f"**Name:** {user['name']}")
                st.markdown(f"**Age:** {user['age']}")
                st.markdown(f"**Gender:** {user['gender']}")
                st.markdown(f"**Phone:** {user['phone']}")
                st.markdown(f"**Location:** {user['location']}")
            
            with st.expander("Activity Preferences", expanded=True):
                st.markdown("**Favorite Activities:**")
                for activity in user['activities_pref']:
                    st.markdown(f"- {activity}")
                
                st.markdown("**Availability:**")
                st.markdown(f"- Days: {', '.join(user['preferred_days'])}")
                st.markdown(f"- Times: {', '.join(user['preferred_times'])}")
            
            with st.expander("Edit Profile", expanded=False):
                st.markdown("Update your profile information:")
                
                name = st.text_input("Name", value=user['name'])
                phone = st.text_input("Phone", value=user['phone'])
                location = st.text_input("Location", value=user['location'])
                
                activities_pref = st.multiselect(
                    "Select activities you enjoy", 
                    st.session_state['activity_types'],
                    default=user['activities_pref']
                )
                
                if st.button("Update Profile"):
                    user['name'] = name
                    user['phone'] = phone
                    user['location'] = location
                    user['activities_pref'] = activities_pref
                    st.success("Profile updated successfully!")
    
    # My Parties page (only accessible when logged in)
    elif page == "My Parties" and st.session_state['logged_in']:
        st.title("My Parties")
        
        user_id = st.session_state['current_user']['id']
        
        # Find parties where the user is a participant or creator
        user_parties = [p for p in st.session_state['parties'] if user_id in p['participants']]
        created_parties = [p for p in st.session_state['parties'] if p['creator_id'] == user_id]
        
        tabs = st.tabs(["Joined Parties", "Created Parties", "Past Parties"])
        
        with tabs[0]:
            if not user_parties:
                st.info("You haven't joined any parties yet.")
                if st.button("Browse Activities"):
                    st.session_state['page'] = "Home"
                    st.experimental_rerun()
            else:
                for party in user_parties:
                    with st.expander(f"{party['name']} - {party['date'].strftime('%d/%m/%Y')}"):
                        col1, col2, col3 = st.columns([1, 2, 1])
                        
                        with col1:
                            img_path = st.session_state['activity_images'].get(party['activity_type'], "/api/placeholder/100/100?text=Activity")
                            st.image(img_path, width=150)
                        
                        with col2:
                            st.markdown(f"**Activity:** {party['activity_type']}")
                            st.markdown(f"**Date:** {party['date'].strftime('%d/%m/%Y')}")
                            st.markdown(f"**Time:** {party['start_time'].strftime('%H:%M')} - {party['end_time'].strftime('%H:%M')}")
                            st.markdown(f"**Location:** {party['location']}")
                            st.markdown(f"**Participants:** {party['current_participants']}/{party['max_participants']}")
                            st.markdown(f"**Description:** {party['description']}")
                            
                            # Calculate cost with potential discounts
                            cost_info = calculate_party_cost(party['id'])
                            st.markdown(f"**Cost:** ${cost_info['final_cost']:.2f} per person")
                            if cost_info['discount'] > 0:
                                st.markdown(f"*You save: ${cost_info['discount']:.2f}*")
                        
                        with col3:
                            if st.button("Leave Party", key=f"myleave_{party['id']}"):
                                success, message = leave_party(party['id'], user_id)
                                if success:
                                    st.success(message)
                                    st.experimental_rerun()
                                else:
                                    st.error(message)
                            
                            st.markdown("---")
                            st.markdown("**Need to know**")
                            st.markdown("Contact organizer:")
                            creator = next((u for u in st.session_state['users'] if u['id'] == party['creator_id']), None)
                            if creator:
                                st.markdown(f"{creator['name']}: {creator['phone']}")
        
        with tabs[1]:
            if not created_parties:
                st.info("You haven't created any parties yet.")
                if st.button("Create a Party"):
                    st.session_state['page'] = "Create Party"
                    st.experimental_rerun()
            else:
                for party in created_parties:
                    with st.expander(f"{party['name']} - {party['date'].strftime('%d/%m/%Y')}"):
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            img_path = st.session_state['activity_images'].get(party['activity_type'], "/api/placeholder/100/100?text=Activity")
                            st.image(img_path, width=150)
                        
                        with col2:
                            st.markdown(f"**Activity:** {party['activity_type']}")
                            st.markdown(f"**Date:** {party['date'].strftime('%d/%m/%Y')}")
                            st.markdown(f"**Time:** {party['start_time'].strftime('%H:%M')} - {party['end_time'].strftime('%H:%M')}")
                            st.markdown(f"**Location:** {party['location']}")
                            st.markdown(f"**Participants:** {party['current_participants']}/{party['max_participants']}")
                            st.markdown(f"**Cost:** ${party['cost_per_person']:.2f} per person")
                            st.markdown(f"**Description:** {party['description']}")
                            
                            if st.button("Edit Party", key=f"edit_{party['id']}"):
                                st.info("Edit functionality would be implemented here")
                            
                            if st.button("Cancel Party", key=f"cancel_{party['id']}"):
                                st.warning("This would cancel the party and notify all participants")
                            
                            st.markdown("---")
                            st.markdown("### Participants")
                            
                            # Show participants list
                            participant_names = []
                            for p_id in party['participants']:
                                participant = next((u for u in st.session_state['users'] if u['id'] == p_id), None)
                                if participant:
                                    participant_names.append(participant['name'])
                            
                            for name in participant_names:
                                st.markdown(f"- {name}")
        
        with tabs[2]:
            st.info("Past parties would be displayed here")
            st.markdown("This would show a history of activities you've participated in")
    
    # Create Party page (only accessible when logged in)
    elif page == "Create Party" and st.session_state['logged_in']:
        st.title("Create a New Party")
        
        with st.form("create_party_form"):
            st.subheader("Party Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                party_name = st.text_input("Party Name")
                activity_type = st.selectbox("Activity Type", st.session_state['activity_types'])
                party_date = st.date_input("Date", value=datetime.datetime.now().date() + datetime.timedelta(days=1))
            
            with col2:
                start_time = st.time_input("Start Time", value=datetime.time(18, 0))
                end_time = st.time_input("End Time", value=datetime.time(20, 0))
                max_participants = st.number_input("Maximum Participants", min_value=2, max_value=50, value=10)
            
            # Filter venues based on selected activity type
            suitable_venues = [v for v in st.session_state['venues'] if activity_type in v['activity_types']]
            venue_options = [(v['id'], v['name']) for v in suitable_venues]
            
            if not venue_options:
                st.warning(f"No suitable venues found for {activity_type}")
                location = st.text_input("Custom Location")
                venue_cost = 0
            else:
                selected_venue = st.selectbox(
                    "Select Venue",
                    venue_options,
                    format_func=lambda x: x[1]
                )
                
                # Get venue details
                venue = next((v for v in st.session_state['venues'] if v['id'] == selected_venue[0]), None)
                location = venue['name']
                
                if 'cost_per_hour' in venue and venue['cost_per_hour'] > 0:
                    hours = (datetime.datetime.combine(datetime.date.today(), end_time) - 
                            datetime.datetime.combine(datetime.date.today(), start_time)).seconds / 3600
                    venue_cost = venue['cost_per_hour'] * hours
                    st.markdown(f"Venue cost: ${venue_cost:.2f} total (${venue['cost_per_hour']:.2f} per hour)")
                
                if 'cost_per_person' in venue and venue['cost_per_person'] > 0:
                    st.markdown(f"Additional cost: ${venue['cost_per_person']:.2f} per person")
                    person_cost = venue['cost_per_person']
                else:
                    person_cost = 0
            
            st.subheader("Additional Information")
            description = st.text_area("Description", placeholder="Tell others about your party...")
            
            # Calculate cost per person
            if 'venue_cost' in locals():
                cost_per_person = person_cost + (venue_cost / max_participants)
            else:
                cost_per_person = st.number_input("Cost per Person ($)", min_value=0.0, value=10.0, step=0.5)
            
            st.markdown(f"**Estimated cost per person:** ${cost_per_person:.2f}")
            
            submit_button = st.form_submit_button("Create Party")
            
            if submit_button:
                if not party_name or not activity_type or not location:
                    st.error("Please fill in all required fields!")
                else:
                    new_party = {
                        "id": len(st.session_state['parties']) + 1,
                        "name": party_name,
                        "activity_type": activity_type,
                        "date": party_date,
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": location,
                        "max_participants": max_participants,
                        "current_participants": 1,  # Creator is the first participant
                        "creator_id": st.session_state['current_user']['id'],
                        "participants": [st.session_state['current_user']['id']],
                        "description": description,
                        "cost_per_person": cost_per_person,
                        "venue_booked": True if 'venue_cost' in