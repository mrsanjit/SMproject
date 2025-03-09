import pandas as pd
import streamlit as st

# Admin login function
def admin_login():
    username = st.text_input("Enter admin username", key="admin_username")
    password = st.text_input("Enter admin password", type="password", key="admin_password")
    
    # Define the admin credentials (You can enhance this later with more security)
    admin_username = "admin"
    admin_password = "admin123"  # You can change this password
    
    if st.button("Login"):
        if username == admin_username and password == admin_password:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.session_state.logged_in = False
            st.error("Invalid username or password.")

# Function to create user profile
def create_user_profile():
    st.header("Create or Update Your Profile")
    
    # Get user inputs
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=0)
    weight = st.number_input("Weight (kg)", min_value=0)
    medical_history = st.text_area("Medical History (e.g., Diabetes, Heart Disease)")

    # Create the profile dictionary
    user_profile = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Height (cm)": height,
        "Weight (kg)": weight,
        "Medical History": medical_history
    }
    
    # Button to save profile
    if st.button("Save Profile"):
        save_profile(user_profile)

# Function to save the profile data
def save_profile(profile_data):
    try:
        # Load existing profiles if they exist
        try:
            profiles_df = pd.read_csv("user_profiles.csv")
        except FileNotFoundError:
            profiles_df = pd.DataFrame()

        # Convert the new profile data to a DataFrame
        new_profile_df = pd.DataFrame([profile_data])

        # Append the new profile data to the existing ones using pd.concat
        profiles_df = pd.concat([profiles_df, new_profile_df], ignore_index=True)

        # Save to CSV
        profiles_df.to_csv("user_profiles.csv", index=False)
        st.success("Profile saved successfully!")

    except Exception as e:
        st.error(f"An error occurred while saving the profile: {e}")

# Function to display profile history (for admin only)
def view_profile_history():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        try:
            # Read the profiles data
            profiles_df = pd.read_csv("user_profiles.csv")

            if profiles_df.empty:
                st.info("No profiles found.")
            else:
                st.write(profiles_df)

        except FileNotFoundError:
            st.error("No profile history available.")
    else:
        st.error("You must log in as admin to view the profile history.")
