import streamlit as st
import mysql.connector
import re

def create_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="customer"
        )
        if mydb.is_connected():
            return mydb
    except mysql.connector.Error as err:
        #st.error(f"Error: {err}")
        return None
    
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    return False

col1, col2=st.columns(2,gap="small",vertical_alignment="center")
with col1:
    st.image("CMS\icons\contact.png", width=220)
with col2:
    st.markdown("<h2 style='text-align: left;'>Contact Us</h2>", unsafe_allow_html=True)
    st.write(
            """
             The purpose of the contact form is to facilitate better communication between users and 
             the company. This feature allows users to easily send messages, ensuring that feedback, 
             inquiries, or any customer concerns are promptly addressed. This helps create a more responsive 
             and user-friendly experience for all.
            """
            )




@st.dialog("Contact Us")
def contact_form():
    name=st.text_input("Full Name")
    mobile=st.text_input("Mobile Number",max_chars=14)
    email=st.text_input("Email")
    if email:
        if validate_email(email):
            st.success("Valid email address")
        else:
            st.error("Invalid Email")

    country=st.text_input("Country")
    message=st.text_area("Enter Your Message")

    submit=st.button("Send")

    if submit:
        mydb=create_connection()
        if mydb:
            try:
                c=mydb.cursor()
                query="INSERT INTO message(full_name,mobile,email,country,message) values (%s,%s,%s,%s,%s)"
                c.execute(query,(name,mobile,email,country,message))
                mydb.commit()
                c.close()
                st.success("Message Sent")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while verifying credentials: {e}")
        else:
            st.error("Unable to connect to the database. Please check Database connection.")

col1, col2=st.columns(2,gap="small",vertical_alignment="center")
with col2:
    if st.button("✉️ Contact Us"):
        contact_form()
