import streamlit as st
import pandas as pd
import datetime
import random

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
    st.session_state['users'] = []
if 'activities' not in st.session_state:
    # Sample activities data
    st.session_state['activities'] = [
        {
            "id": 1,
            "party_name": "Sunday Football Fun",
            "activity_type": "Football",
            "date": datetime.date(2025, 3, 10),
            "start_time": datetime.time(18, 0),
            "location": "Central Park Fields",
            "max_participants": 10,
            "current_participants": 6,
            "creator_id": 1,
            "participants": [1, 2, 3, 4, 5, 6]
        },
        {
            "id": 2,
            "party_name": "Chess Masters",
            "activity_type": "Board Games",
            "date": datetime.date(2025, 3, 5),
            "start_time": datetime.time(19, 0),
            "location": "Gamesmith Cafe",
            "max_participants": 4,
            "current_participants": 3,
            "creator_id": 2,
            "participants": [2, 3, 4]
        },
        {
            "id": 3,
            "party_name": "Basketball Shootout",
            "activity_type": "Basketball",
            "date": datetime.date(2025, 3, 4),
            "start_time": datetime.time(17, 30),
            "location": "YMCA Court",
            "max_participants": 8,
            "current_participants": 5,
            "creator_id": 3,
            "participants": [3, 4, 5, 6, 7]
        },
        {
            "id": 4,
            "party_name": "Settlers of Catan Night",
            "activity_type": "Board Games",
            "date": datetime.date(2025, 3, 7),
            "start_time": datetime.time(20, 0),
            "location": "Board & Brew",
            "max_participants": 4,
            "current_participants": 2,
            "creator_id": 4,
            "participants": [4, 5]
        },
    ]

# Function to handle user registration
def register_user(user_data):
    # Check if username already exists
    if any(user['username'] == user_data['username'] for user in st.session_state['users']):
        return False
    st.session_state['users'].append(user_data)
    return True

# Function to handle login
def login(username, password):
    # For demo, simple login check
    user = next((user for user in st.session_state['users'] if user['username'] == username), None)
    if user and user['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = user
        return True
    return False

# Function to create a new activity
def create_activity(activity_data):
    activity_data["id"] = len(st.session_state['activities']) + 1
    st.session_state['activities'].append(activity_data)
    return activity_data["id"]

# Function to join an activity
def join_activity(activity_id, user_id):
    for activity in st.session_state['activities']:
        if activity['id'] == activity_id:
            if activity['current_participants'] < activity['max_participants'] and user_id not in activity['participants']:
                activity['participants'].append(user_id)
                activity['current_participants'] += 1
                return True
    return False

# Function to leave an activity
def leave_activity(activity_id, user_id):
    for activity in st.session_state['activities']:
        if activity['id'] == activity_id and user_id in activity['participants']:
            activity['participants'].remove(user_id)
            activity['current_participants'] -= 1
            return True
    return False

# Create sample users if none exist
if not st.session_state['users']:
    sample_users = [
        {
            "id": 1,
            "name": "John Doe",
            "age": 28,
            "phone": "123-456-7890",
            "gender": "Male",
            "username": "john",
            "password": "password",
            "preferred_activities": ["Football", "Basketball"],
            "location": "Downtown"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "age": 25,
            "phone": "123-456-7891",
            "gender": "Female",
            "username": "jane",
            "password": "password",
            "preferred_activities": ["Board Games", "Tennis"],
            "location": "Uptown"
        },
        {
            "id": 3,
            "name": "Bob Johnson",
            "age": 32,
            "phone": "123-456-7892",
            "gender": "Male",
            "username": "bob",
            "password": "password",
            "preferred_activities": ["Basketball", "Board Games"],
            "location": "Midtown"
        },
        {
            "id": 4,
            "name": "Alice Williams",
            "age": 27,
            "phone": "123-456-7893",
            "gender": "Female",
            "username": "alice",
            "password": "password",
            "preferred_activities": ["Board Games", "Volleyball"],
            "location": "Eastside"
        },
    ]
    st.session_state['users'].extend(sample_users)

# Main app layout
def main():
    # App title and header
    st.title("Joinzy! 🎮")
    st.markdown("### Find Your Perfect Activity Match")
    
    # Authentication section in sidebar
    with st.sidebar:
        st.header("Account")
        if st.session_state['logged_in']:
            st.success(f"Logged in as {st.session_state['current_user']['name']}")
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['current_user'] = None
                st.experimental_rerun()
            
            st.header("Navigation")
            page = st.radio("", ["Main Page", "My Activities", "Profile"])
        else:
            auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
            
            with auth_tab1:
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
            
            with auth_tab2:
                with st.form("registration_form"):
                    name = st.text_input("Full Name")
                    age = st.number_input("Age", min_value=16, max_value=100, value=25)
                    phone = st.text_input("Phone Number")
                    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    
                    activities_pref = st.multiselect(
                        "Preferred Activities", 
                        ["Football", "Basketball", "Tennis", "Board Games", "Volleyball", "Running", "Cycling"]
                    )
                    
                    location = st.text_input("Your Location (Area/District)")
                    
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
                                "preferred_activities": activities_pref,
                                "location": location
                            }
                            
                            if register_user(user_data):
                                st.success("Registration successful! Please log in.")
                            else:
                                st.error("Username already exists. Please choose another.")
            
            page = "Main Page"  # Default page for non-logged in users
    
    # Main page content
    if page == "Main Page":
        display_main_page()
    elif page == "My Activities":
        display_my_activities()
    elif page == "Profile":
        display_profile()

def display_main_page():
    # Main Page Features as specified
    st.header("Find or Create Activities")
    
    # Activity Type Dropdown
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        activity_types = ["All Types", "Football", "Basketball", "Tennis", "Board Games", "Volleyball", "Running", "Cycling"]
        selected_type = st.selectbox("Activity Type", activity_types)
    
    # Create/Search Party Buttons
    with col2:
        st.write("")  # For spacing
        st.write("")  # For spacing
        create_col, search_col = st.columns(2)
        with create_col:
            create_button = st.button("Create Party")
        with search_col:
            search_button = st.button("Search")
    
    # Filter activities based on selection
    filtered_activities = st.session_state['activities']
    if selected_type != "All Types":
        filtered_activities = [act for act in filtered_activities if act['activity_type'] == selected_type]
    
    # Create Party Form (shown when Create Party button is clicked)
    if create_button:
        if not st.session_state['logged_in']:
            st.warning("Please log in to create a party")
        else:
            st.subheader("Create a New Activity Party")
            with st.form("create_party_form"):
                party_name = st.text_input("Party Name")
                activity_type = st.selectbox("Activity Type", activity_types[1:])  # Exclude "All Types"
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("Date", min_value=datetime.date.today())
                with col2:
                    time = st.time_input("Start Time", value=datetime.time(18, 0))
                
                location = st.text_input("Location/Venue")
                max_participants = st.number_input("Maximum Participants", min_value=2, max_value=50, value=8)
                
                submit_button = st.form_submit_button("Create Party")
                
                if submit_button:
                    if not party_name or not location:
                        st.error("Please fill in all required fields!")
                    else:
                        activity_data = {
                            "party_name": party_name,
                            "activity_type": activity_type,
                            "date": date,
                            "start_time": time,
                            "location": location,
                            "max_participants": max_participants,
                            "current_participants": 1,  # Creator is the first participant
                            "creator_id": st.session_state['current_user']['id'],
                            "participants": [st.session_state['current_user']['id']]
                        }
                        
                        activity_id = create_activity(activity_data)
                        st.success(f"Activity '{party_name}' created successfully!")
                        st.experimental_rerun()
    
    # Activity Summary Table
    st.subheader("Available Activities")
    
    if not filtered_activities:
        st.info("No activities found for the selected type. Try creating a new one!")
    else:
        # Create a DataFrame for display
        table_data = []
        for activity in filtered_activities:
            # Format date and time
            formatted_date = activity['date'].strftime('%d/%m/%Y')
            formatted_time = activity['start_time'].strftime('%H:%M')
            
            # Format participants
            participants_str = f"{activity['current_participants']}/{activity['max_participants']}"
            
            # Check if current user is a participant
            is_participant = False
            if st.session_state['logged_in']:
                is_participant = st.session_state['current_user']['id'] in activity['participants']
            
            table_data.append({
                "ID": activity['id'],
                "Party Name": activity['party_name'],
                "Activity Type": activity['activity_type'],
                "Date": formatted_date,
                "Start Time": formatted_time,
                "Location": activity['location'],
                "Participants": participants_str,
                "Is Participant": is_participant
            })
        
        df = pd.DataFrame(table_data)
        
        # Display table with custom formatting
        st.dataframe(
            df[["Party Name", "Activity Type", "Date", "Start Time", "Location", "Participants"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Activity details and join/leave buttons
        st.subheader("Activity Details")
        
        # Let user select an activity to view details
        selected_activity_id = st.selectbox(
            "Select an activity to view details",
            options=[a["ID"] for a in table_data],
            format_func=lambda x: next((a["Party Name"] for a in table_data if a["ID"] == x), ""),
        )
        
        if selected_activity_id:
            selected_activity = next((a for a in filtered_activities if a['id'] == selected_activity_id), None)
            
            if selected_activity:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {selected_activity['party_name']}")
                    st.markdown(f"**Activity Type:** {selected_activity['activity_type']}")
                    st.markdown(f"**Date & Time:** {selected_activity['date'].strftime('%d/%m/%Y')} at {selected_activity['start_time'].strftime('%H:%M')}")
                    st.markdown(f"**Location:** {selected_activity['location']}")
                    st.markdown(f"**Participants:** {selected_activity['current_participants']}/{selected_activity['max_participants']}")
                    
                    # Show creator
                    creator = next((user for user in st.session_state['users'] if user['id'] == selected_activity['creator_id']), None)
                    if creator:
                        st.markdown(f"**Created by:** {creator['name']}")
                    
                    # Show participants
                    st.markdown("**Participants List:**")
                    for participant_id in selected_activity['participants']:
                        participant = next((user for user in st.session_state['users'] if user['id'] == participant_id), None)
                        if participant:
                            st.markdown(f"- {participant['name']}")
                
                with col2:
                    st.write("")  # For spacing
                    st.write("")  # For spacing
                    
                    if not st.session_state['logged_in']:
                        st.warning("Please log in to join activities")
                    else:
                        user_id = st.session_state['current_user']['id']
                        is_participant = user_id in selected_activity['participants']
                        is_full = selected_activity['current_participants'] >= selected_activity['max_participants']
                        
                        if is_participant:
                            # Allow leaving the activity
                            if st.button("Leave Activity", key=f"leave_{selected_activity_id}"):
                                if leave_activity(selected_activity_id, user_id):
                                    st.success("You have left the activity")
                                    st.experimental_rerun()
                                else:
                                    st.error("Error leaving the activity")
                        else:
                            # Allow joining the activity if not full
                            if is_full:
                                st.error("This activity is full")
                            else:
                                if st.button("Join Activity", key=f"join_{selected_activity_id}"):
                                    if join_activity(selected_activity_id, user_id):
                                        st.success("You have joined the activity!")
                                        st.experimental_rerun()
                                    else:
                                        st.error("Error joining the activity")

def display_my_activities():
    if not st.session_state['logged_in']:
        st.warning("Please log in to view your activities")
        return
    
    st.header("My Activities")
    
    # Tabs for Created vs Joined activities
    tab1, tab2 = st.tabs(["Activities I Created", "Activities I Joined"])
    
    user_id = st.session_state['current_user']['id']
    
    with tab1:
        # Activities created by the user
        created_activities = [act for act in st.session_state['activities'] if act['creator_id'] == user_id]
        
        if not created_activities:
            st.info("You haven't created any activities yet. Go to the Main Page to create one!")
        else:
            for activity in created_activities:
                with st.expander(f"{activity['party_name']} - {activity['date'].strftime('%d/%m/%Y')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Activity Type:** {activity['activity_type']}")
                        st.markdown(f"**Date & Time:** {activity['date'].strftime('%d/%m/%Y')} at {activity['start_time'].strftime('%H:%M')}")
                        st.markdown(f"**Location:** {activity['location']}")
                        st.markdown(f"**Participants:** {activity['current_participants']}/{activity['max_participants']}")
                        
                        # List participants
                        st.markdown("**Participants:**")
                        for participant_id in activity['participants']:
                            participant = next((user for user in st.session_state['users'] if user['id'] == participant_id), None)
                            if participant:
                                st.markdown(f"- {participant['name']}")
                    
                    with col2:
                        if st.button("Edit", key=f"edit_{activity['id']}"):
                            st.session_state['edit_activity'] = activity['id']
                        
                        if st.button("Cancel Activity", key=f"cancel_{activity['id']}"):
                            st.warning("This would cancel the activity in a real application")
    
    with tab2:
        # Activities joined by the user (excluding ones created by them)
        joined_activities = [act for act in st.session_state['activities'] 
                           if user_id in act['participants'] and act['creator_id'] != user_id]
        
        if not joined_activities:
            st.info("You haven't joined any activities created by others. Go to the Main Page to find activities!")
        else:
            for activity in joined_activities:
                with st.expander(f"{activity['party_name']} - {activity['date'].strftime('%d/%m/%Y')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Activity Type:** {activity['activity_type']}")
                        st.markdown(f"**Date & Time:** {activity['date'].strftime('%d/%m/%Y')} at {activity['start_time'].strftime('%H:%M')}")
                        st.markdown(f"**Location:** {activity['location']}")
                        st.markdown(f"**Participants:** {activity['current_participants']}/{activity['max_participants']}")
                        
                        # Show creator
                        creator = next((user for user in st.session_state['users'] if user['id'] == activity['creator_id']), None)
                        if creator:
                            st.markdown(f"**Created by:** {creator['name']}")
                    
                    with col2:
                        if st.button("Leave Activity", key=f"leave_joined_{activity['id']}"):
                            if leave_activity(activity['id'], user_id):
                                st.success("You have left the activity")
                                st.experimental_rerun()
                            else:
                                st.error("Error leaving the activity")

def display_profile():
    if not st.session_state['logged_in']:
        st.warning("Please log in to view your profile")
        return
    
    st.header("My Profile")
    
    user = st.session_state['current_user']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile picture placeholder
        st.image("https://via.placeholder.com/150", caption=user['name'])
    
    with col2:
        st.markdown(f"**Name:** {user['name']}")
        st.markdown(f"**Age:** {user['age']}")
        st.markdown(f"**Gender:** {user['gender']}")
        st.markdown(f"**Phone:** {user['phone']}")
        st.markdown(f"**Location:** {user['location']}")
        st.markdown(f"**Preferred Activities:** {', '.join(user['preferred_activities'])}")
    
    st.subheader("Edit Profile")
    
    with st.form("edit_profile_form"):
        name = st.text_input("Full Name", value=user['name'])
        phone = st.text_input("Phone Number", value=user['phone'])
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=16, max_value=100, value=user['age'])
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"], index=["Male", "Female", "Non-binary", "Prefer not to say"].index(user['gender']))
        
        preferred_activities = st.multiselect(
            "Preferred Activities", 
            ["Football", "Basketball", "Tennis", "Board Games", "Volleyball", "Running", "Cycling"],
            default=user['preferred_activities']
        )
        
        location = st.text_input("Your Location", value=user['location'])
        
        st.markdown("**Change Password**")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submit_button = st.form_submit_button("Update Profile")
        
        if submit_button:
            if new_password and current_password != user['password']:
                st.error("Current password is incorrect")
            elif new_password and new_password != confirm_password:
                st.error("New passwords do not match")
            else:
                # Update user info
                updated_user = user.copy()
                updated_user.update({
                    "name": name,
                    "age": age,
                    "phone": phone,
                    "gender": gender,
                    "preferred_activities": preferred_activities,
                    "location": location
                })
                
                if new_password:
                    updated_user["password"] = new_password
                
                # Update in session state
                for i, u in enumerate(st.session_state['users']):
                    if u['id'] == user['id']:
                        st.session_state['users'][i] = updated_user
                        break
                
                st.session_state['current_user'] = updated_user
                st.success("Profile updated successfully!")

# Run the app
if __name__ == "__main__":
    main()
