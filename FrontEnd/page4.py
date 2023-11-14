import streamlit as st
from deepface import DeepFace
import os
from fpdf import FPDF
import base64
from mailjet_rest import Client
import mysql.connector

def analyze_image_and_send_report(uploaded_image, user_email):
    # Create a temporary directory to save the uploaded image
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    image_path = os.path.join(temp_dir, uploaded_image.name)

    # Save the uploaded image to the temporary directory
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())
    
    try:
        objs = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race', 'emotion'])
    except Exception:
        #st.error(f"Error in analyzing the image: {e}")
        return
    
    # Analyze the uploaded image using DeepFace
    objs = DeepFace.analyze(img_path=image_path, actions=['age', 'gender','race','emotion'])

    # Display the uploaded image
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Display the analysis results
    st.write("Analysis Results:")
    st.write(f"Age: {objs[0]['age']}")  # Access age value correctly
    st.write(f"Gender: {objs[0]['dominant_gender']}")
    st.write(f"Race: {objs[0]['dominant_race']}")  
    st.write(f"Emotion: {objs[0]['dominant_emotion']}")

    pdf = FPDF(format='letter')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

# Set font and size
    pdf.set_font("Arial", size=12)

# Add a title with a border
    pdf.multi_cell(0, 10, f"EpicVison Final Report", border=1, align='C')
    pdf.ln(10)

# Load the image with proper dimensions and add a border
    pdf.image(image_path, x=10, w=50)
    pdf.ln(10)

# Access the values from objs[0] correctly
    age = objs[0]['age']
    gender = objs[0]['dominant_gender']
    race = objs[0]['dominant_race']
    emotion = objs[0]['dominant_emotion']

    # Create formatted text with borders and alignment
    pdf.multi_cell(0, 10, f"Age: {objs[0]['age']}")  # Access age value correctly
    pdf.multi_cell(0, 10, f"Gender: {objs[0]['dominant_gender']}")  # Access gender value correctly
    pdf.multi_cell(0, 10, f"Race: {objs[0]['dominant_race']}")
    pdf.multi_cell(0, 10, f"Emotion: {objs[0]['dominant_emotion']}")


    # Save the PDF report with proper file structure
    report_directory = "reports"
    os.makedirs(report_directory, exist_ok=True)
    report_path = os.path.join(report_directory, "analysis_report.pdf")

    # Save the PDF report
    pdf.output(report_path)
    
    store_results_in_database(image_path, age, gender, race, emotion)

    with open(report_path, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        st.markdown(f'<a href="data:application/pdf;base64,{pdf_base64}" download="analysis_report.pdf">Click here to download the PDF report</a>', unsafe_allow_html=True)

    if user_email:
        # Define your Mailjet API credentials
        api_key = API_KEY
        api_secret = SECRET_KEY
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Create the email message
        message = {
            'Messages': [
                {
                    'From': {
                        'Email': 'studyaccrakshika@gmail.com',
                        'Name': 'EpicVision',
                    },
                    'To': [
                        {
                            'Email': user_email,
                            'Name': 'Recipient Name',
                        },
                    ],
                    'Subject': 'Criminal Suspect Report',
                    'TextPart': 'Attached is the Criminal Suspect Report.',
                    'Attachments': [
                        {
                            'ContentType': 'application/pdf',
                            'Filename': 'analysis_report.pdf',
                            'Base64Content': pdf_base64,
                        },
                    ],
                },
            ]
        }

        # Send the email using Mailjet
        response = mailjet.send.create(data=message)
        if response.status_code == 200:
            st.write(f"Report sent to {user_email}")
        else:
            st.error("Failed to send the email. Please check your Mailjet API credentials.")


def store_results_in_database(image_path, age, gender, race, emotion):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            database="predictions",
            autocommit=True
        )
        cursor = connection.cursor()

        insert_query = "INSERT INTO analysis_results (image_path, predicted_age, predicted_gender, predicted_race, predicted_emotion) VALUES (%s, %s, %s, %s, %s)"
        data = (image_path, age, gender, race, emotion)
        cursor.execute(insert_query, data)

        connection.commit()
        st.write("Analysis results stored in the database.")

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def main():
    st.title("Suspect feature prediction")

    # Create a Streamlit file uploader widget to allow users to upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    
    user_email = st.text_input("Enter your email address")
    if st.button("Send Report via Email"):
        analyze_image_and_send_report(uploaded_image, user_email)
        
    if uploaded_image is not None:
        analyze_image_and_send_report(uploaded_image, user_email)
    else:
        st.write("Please upload an image.")
    
    

if __name__ == '__main__':
    main()
