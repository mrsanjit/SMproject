import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from Frontend.home import *  # Importing show_message from home.py -----sanjit 
from Frontend.news import fetch_health_articles  # Importing the health news function
import numpy as np
import pyttsx3
import plotly.express as px
from Frontend.user_profile import save_profile, view_profile_history, admin_login





# Set page configuration
st.set_page_config(page_title="Prediction of Disease Outbreaks",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load models with exception handling
try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading diabetes model: {e}")

try:
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading heart disease model: {e}")

try:
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading Parkinson's disease model: {e}")


# Example for Heart Disease Prediction - display pie chart
def display_prediction_chart(heart_prediction):
    # Sample data for chart
    prediction = ["Heart Disease", "No Heart Disease"]
    values = [heart_prediction[0], 1 - heart_prediction[0]]

    fig = px.pie(values=values, names=prediction, title="Heart Disease Prediction")
    st.plotly_chart(fig)


# import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()



# Sidebar for navigation
with st.sidebar:
       selected = option_menu('Prediction of Disease Outbreaks System',
                           ['Home', 'Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'User Profile', 'Health News'],
                           menu_icon='hospital-fill',
                           icons=['house', 'person-heart', 'heart-pulse', 'person-lines-fill', 'person', 'newspaper'],
                           default_index=0)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# User Profile Page (Create/Update and View History)
if selected == 'User Profile':
    st.title("User Profile Management")

    # Sidebar for Profile Management (Create/Update or View Profile History)
    profile_option = st.sidebar.selectbox("Choose an option", ["Create/Update Profile", "View Profile History"])

    # Create/Update Profile Section
    if profile_option == "Create/Update Profile":
        st.header("Create or Update Your Profile")
        
        # Form inputs for profile data
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        disease = st.text_input("Disease")
        
        # Save Profile Button
        if st.button("Save Profile"):
            if name and disease:
                profile_data = {
                    "Name": name,
                    "Age": age,
                    "Disease": disease
                }
                save_profile(profile_data)
            else:
                st.error("Please fill in all the fields.")

    # View Profile History Section (Admin Login)
    elif profile_option == "View Profile History":
        st.header("Admin Login to View Profile History")
        admin_login()

        if st.session_state.logged_in:
            view_profile_history()
        else:
            st.error("You must log in as admin to view profile history.")

# Home page content
if selected == 'Home':
    st.title("Welcome to Disease Prediction System")
    st.markdown(
        """
        <p style='font-size:20px; background-color:red; color:white; padding:10px;'>This app helps predict various diseases based on the input data.</p>
        """, unsafe_allow_html=True)
        
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")    

# Health News Page
if selected == 'Health News':
    st.title("Health News Section")
    fetch_health_articles()  # Fetch and display health articles from news.py


# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    # Code for Prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

        # After prediction, show message and chart
        show_message()

    st.success(diab_diagnosis)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age', min_value=0)

    with col2:
        sex = st.selectbox('Sex', ['Male', 'Female'])

    with col3:
        cp = st.selectbox('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'])

    with col1:
        trestbps = st.number_input('Resting Blood Pressure', min_value=0)

    with col2:
        chol = st.number_input('Serum Cholestoral in mg/dl', min_value=0)

    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', [True, False])

    with col1:
        restecg = st.selectbox('Resting Electrocardiographic Results', ['Normal', 'Having ST-T wave abnormality', 'Showing probable or definite left ventricular hypertrophy'])

    with col2:
        thalach = st.number_input('Maximum Heart Rate achieved', min_value=0)

    with col3:
        exang = st.selectbox('Exercise Induced Angina', [True, False])

    with col1:
        oldpeak = st.number_input('ST depression induced by exercise', min_value=0.0)

    with col2:
        slope = st.selectbox('Slope of the Peak Exercise ST Segment', ['Upsloping', 'Flat', 'Downsloping'])

    with col3:
        ca = st.number_input('Major Vessels Colored by Flourosopy', min_value=0)

    with col1:
        thal = st.selectbox('Thal: 0 = Normal; 1 = Fixed defect; 2 = Reversable defect', [0, 1, 2])

    # Code for Prediction
    heart_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        # Modify input processing based on selectbox inputs (sex, cp)
        sex = 1 if sex == 'Male' else 0  # Convert to numeric if needed
        cp = ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'].index(cp)  # Convert to numeric if needed
        fbs = 1 if fbs else 0  # Convert boolean to numeric (1 for True, 0 for False)
        restecg = ['Normal', 'Having ST-T wave abnormality', 'Showing probable or definite left ventricular hypertrophy'].index(restecg)  # Convert to numeric if needed
        exang = 1 if exang else 0  # Convert boolean to numeric (1 for True, 0 for False)
        slope = ['Upsloping', 'Flat', 'Downsloping'].index(slope)  # Convert to numeric if needed
        thal = int(thal)  # Convert to numeric if needed

        # Prepare user_input
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        # Convert string values to numeric (if any)
        user_input = [float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x for x in user_input]

        # Prediction using the heart disease model
        heart_prediction = heart_disease_model.predict([user_input])

        # Display diagnosis
        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
            speak(heart_diagnosis)
        else:
            heart_diagnosis = 'The person does not have any heart disease'
            speak(heart_diagnosis)

        # After prediction, show message and chart
        show_message()

    st.success(heart_diagnosis)


# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":

    # Page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # Code for Prediction
    park_diagnosis = ''

    # Creating a button for Prediction
    if st.button("Parkinson's Test Result"):
        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        # Convert string inputs to float
        user_input = [float(x) for x in user_input]

        park_prediction = parkinsons_model.predict([user_input])

        if park_prediction[0] == 1:
            park_diagnosis = "The person has Parkinson's disease"
        else:
            park_diagnosis = "The person does not have Parkinson's disease"

        # After prediction, show message
        show_message()
        