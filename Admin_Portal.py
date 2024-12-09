import streamlit as st
import pandas as pd
import mysql.connector

def create_connection():
    try:
        mydb = mysql.connector.connect(
            host="34.100.224.51",
            user="root",
            password="NETra@186",
            database="netrasarma"
        )
        if mydb.is_connected():
            return mydb
    except mysql.connector.Error as err:
        #st.error("Database not connected")
        #st.error(f"Error details: {err}")
        return None



#---------Pop-Up window after Login----------
@st.dialog("Success")
def login_success():
       st.success("Logged in successfully")
       proceed_btn=st.button("Proceed to Work")
       if proceed_btn:
           st.rerun()




# Initialize session state for login if not already set
if 'login' not in st.session_state:
    st.session_state['login'] = False
    
if not st.session_state['login']:
    c1, c2, c3 = st.columns([1,3,1])
    with c2:
        st.markdown("<h2 style='text-align: left;'>Sign in</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: left;'>to access Administrative Portal</h4>", unsafe_allow_html=True)
        a_id = st.text_input("Admin ID")
        a_pass = st.text_input("Password", type="password")
        btn2 = st.button("Login")

    if btn2:
        mydb = create_connection()
        if mydb:
            try:
                c = mydb.cursor()
                c.execute("SELECT * FROM admin WHERE admin_id=%s AND admin_pass=%s", (a_id, a_pass))
                result = c.fetchone()
                if result:
                    st.session_state['login'] = True
                    login_success()
                else:
                    with c2:
                        st.error("Login failed, please enter correct details")
            except Exception as e:
                st.error(f"An error occurred while verifying credentials: {e}")
        else:
            with c2:
                st.error("Unable to connect to the database. Please check Database connection.")




else:
    col1, col2=st.columns(2,gap="small",vertical_alignment="center")
    with col2:
        st.button("Logout", on_click=lambda: st.session_state.update({'login': False}))
    with col1:   
        st.success("Welcome! You are logged in as Admin.")
    st.write("\n")
    st.write("\n")
    col1, col2=st.columns(2,gap="small",vertical_alignment="center")
    with col1:
        choice1=st.selectbox("Select Task",("View All Employee Account","Create Employee Account","Delete Employee Acount","Update Employee Data","Messages from Employee" ),index=None)
    st.write("\n")
    st.write("\n")

## CODE TO CREATE NEW USER(INSIDE ADMIN)
    col1, col2=st.columns(2,gap="small",vertical_alignment="center")
    if choice1=="Create Employee Account":
        with col1:
            st.markdown("<h4 style='text-align:center;'>Employee Registration Form</h4>", unsafe_allow_html=True)
            u_type = st.selectbox("Department", ("HR", "Finance", "Marketing", "Sales", "IT", "Operations",
                            "Customer Service", "R&D", "Legal", "Procurement", "Administration", "PR"),index=None, placeholder="Choose Department")
            u_name=st.text_input("Full Name")
            u_id=st.text_input("User ID")
            u_pass=st.text_input("Password")
            
            c_btn=st.button("Submit")
            
            if c_btn:
                mydb=create_connection()
                c=mydb.cursor()
                query="INSERT INTO user(user_id,user_type,user_name,password) values (%s,%s,%s,%s)"
                c.execute(query,(u_id,u_type,u_name,u_pass))
                mydb.commit()
                st.success("Employee Account Created Successfully")
                c.close()
                

## CODE TO DELETE USER DATA (INSIDE ADMIN)         

    elif choice1=="Delete Employee Acount":
        col1, col2=st.columns(2,gap="small",vertical_alignment="center")
        with col1:
            user_id=st.text_input("Enter User Id")
            search_btn=st.button("Search Employee")
        

        if search_btn:
            mydb=create_connection()
            query = "SELECT * FROM user WHERE user_id = %s"
            df = pd.read_sql(query, mydb, params=(user_id,))
            st.table(df)
            mydb.close()
        with col1:
            delete_btn=st.button("Delete Account")
        if delete_btn:
            mydb=create_connection()
            c=mydb.cursor()
            c.execute("DELETE FROM user WHERE user_id=%s",(user_id,))
            mydb.commit()
            mydb.close()
            st.success("Account Deleted Successfully")

   
## CODE TO VIEW ALL USER DATA (INSIDE ADMIN)

    elif choice1=="View All Employee Account":
        st.markdown("<h4 style='text-align: center;'>Employee Details</h4>", unsafe_allow_html=True)
        mydb=create_connection()
        query="SELECT * FROM user"
        df=pd.read_sql(query,mydb)
        mydb.close()
            
        if df.empty:
            st.error("Data not found")
        else:
            st.table(df)
            
## CODE TO UPDATE USER DATA (INSIDE ADMIN)

    elif choice1 == "Update Employee Data":
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = ""

        if not st.session_state['logged_in']:
            
            col1, col2=st.columns(2,gap="small",vertical_alignment="center")
            with col1:
                st.markdown("<h4 style='text-align: center;'>Update Account Details</h4>", unsafe_allow_html=True)
                user_id = st.text_input("User ID")
            if st.button("Search"):
                mydb = create_connection()
                c = mydb.cursor()
                c.execute("SELECT user_name FROM user WHERE user_id = %s", (user_id,))
                user = c.fetchone()
                c.close()
                mydb.close()

                if user:
                    st.session_state.update({'logged_in': True, 'user_name': user[0], 'user_id': user_id})
                    st.success(f"Account Details Found with name: {st.session_state['user_name']}!")
                    st.session_state['show_form'] = True
                    st.button("Click Here to Update")
                else:
                    st.error("Account not found with the given ID.")
        else:
            if 'show_form' in st.session_state:
                mydb = create_connection()
                c = mydb.cursor()
                c.execute("SELECT user_type, user_name, password FROM user WHERE user_id = %s", (st.session_state['user_id'],))
                user_details = c.fetchone()
                c.close()
                mydb.close()

                if user_details:
                    with st.form("update_form"):
                        options = [
                            "HR", "Finance", "Marketing", "Sales", "IT", "Operations",
                            "Customer Service", "R&D", "Legal", "Procurement", "Administration", "PR"
                        ]
                        user_type = st.selectbox("Department", options,
                                                index=options.index(user_details[0]) if user_details[0] in options else 0)
                        user_name = st.text_input("New Name", value=user_details[1])
                        password = st.text_input("New Password", value=user_details[2], type="password")

                        if st.form_submit_button("Update Data"):
                            mydb = create_connection()
                            c = mydb.cursor()
                            c.execute("UPDATE user SET user_type = %s, user_name = %s, password = %s WHERE user_id = %s",
                                    (user_type, user_name, password, st.session_state['user_id']))
                            mydb.commit()
                            c.close()
                            mydb.close()
                            st.success("Account Details updated successfully!")

                    if st.button("Update Another Data"):
                        st.session_state.update({'logged_in': False, 'user_name': ""})
                        st.rerun()

#-----------FUNCTION TO REPLY EMPLOYEE MESSAGES --------------
    def reply(emp_message_id):
        mydb = create_connection()
        query = "SELECT * FROM message_from_employee WHERE emp_message_id = %s"
        df = pd.read_sql(query, mydb, params=(emp_message_id,))
        
        if not df.empty:
            emp_data = df.iloc[0]
            mydb.close()
        else:
            st.warning("Message data not found.")
            return
        
        st.markdown(f"### Reply to Message ID: {emp_message_id}")
        col1, col2 = st.columns(2, gap="small")
        with col1:
            reply_text = st.text_area("Reply", value=emp_data.get('reply', ''))
            status_text = st.text_input("Status", value=emp_data.get('status', ''))
        
        send_btn = st.button("Send")
        
        if send_btn:
            if reply_text and status_text:
                mydb = create_connection()
                c = mydb.cursor()
                update_query = """
                UPDATE message_from_employee
                SET reply = %s, status = %s
                WHERE emp_message_id = %s
                """
                c.execute(update_query, (reply_text, status_text, emp_message_id))
                mydb.commit()
                st.success("Reply and status updated successfully.")
                c.close()
                mydb.close()
            else:
                st.warning("Please fill all the fields.")


#-------------MESSAGE FROM EMPLOYE AND REPLY FORM ---------------
    if choice1 == "Messages from Employee":
        st.markdown("<h4 style='text-align: center;'>Messages from employee</h4>", unsafe_allow_html=True)
        mydb = create_connection()
        query = "SELECT * FROM message_from_employee"
        df = pd.read_sql(query, mydb)
        
        if df.empty:
            st.error("Data not found")
        else:
            st.table(df)
            emp_message_id_selected = st.selectbox("Select a Message ID to reply:", df['emp_message_id'])

            if emp_message_id_selected:
                st.write("Details for the selected Message ID:")
                st.table(df[df['emp_message_id'] == emp_message_id_selected])
                reply(emp_message_id_selected) 



        

    
    


            

 





    


