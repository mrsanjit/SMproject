import streamlit as st

# Function to display the custom form
def render_input_form():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input('Age', min_value=0)
    
    with col2:
        sex = st.selectbox('Sex', ['Male', 'Female'])
    
    with col3:
        cp = st.selectbox('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'])
    
    # Add other fields here...
    
    return age, sex, cp
