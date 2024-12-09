import streamlit as st
import pandas as pd 
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from time import sleep
from datetime import datetime

#DATABASE CONNECTION
def create_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NETra@186",
            database="customer"
        )
        if mydb.is_connected():
            return mydb
    except mysql.connector.Error as err:
        #st.error("Database not connected")
        #st.error(f"Error details: {err}")
        return None

#SUBSCRIBER DATA DELETE SECTION
    #----------DELETE ALL DATA---------
def delete_all_data():
    mydb=create_connection()
    c=mydb.cursor()
    c.execute("DELETE FROM customer")
    mydb.commit()
    c.close()
    mydb.close()
    st.success("All Subsciber data deleted successfully from database")

    #------------DELETE BY RANGE-----------
def delete_data_by_range(start_id,end_id):
    mydb=create_connection()
    c=mydb.cursor()
    delete_query=("DELETE FROM customer WHERE  `User ID` BETWEEN %s and %s")
    c.execute(delete_query,(start_id,end_id))
    mydb.commit()
    c.close()
    mydb.close()
    st.success("Subscriber data deleted successfully from database for the given range")

    #--------------DELETE SINGLE DATA---------
def delete_single_data(id_delete):
    mydb=create_connection()
    c=mydb.cursor()
    delete_query=("DELETE FROM customer WHERE `User ID`=%s")
    c.execute(delete_query,(id_delete,))
    mydb.commit()
    c.close()
    mydb.close()
    st.success("Subscriber data deleted successfully from database for the given ID")


#------------UPLOAD FILE INTO SUBSCRIBER DATA-------
def insert_data_from_csv(file, mydb):

    data = pd.read_csv(file)
    
    c = mydb.cursor()
    
    progress = st.progress(0)
    total_rows = len(data)
    
    for i, row in data.iterrows():
        c.execute(
            "INSERT INTO customer (`Subscription Type`, `Monthly Revenue`, `Join Date`, `Last Payment Date`, `Country`, `Age`, `Gender`, `Device`, `Plan Duration`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            tuple(row)
        )
        progress.progress(int((i + 1) / total_rows * 100))
        sleep(0.1) 
    
    mydb.commit()
    c.close()



#-----------Message to Admin-------------
#-----------Previous Message-----------



@st.dialog("Message to Admin")
def contact_form():
    id=st.text_input("Enter Your User ID")
    message=st.text_area("Enter Your Message")
        
        
    submit=st.button("Send")

    previous=st.button("Check Previous Messages")
    if previous:
        st.markdown("<h3 style='text-align: center;'>🕐Previous Mesages</h3>", unsafe_allow_html=True)
        u_id = id
        if u_id:
            mydb = create_connection()
            query = "SELECT * FROM message_from_employee WHERE emp_id = %s"
            df = pd.read_sql(query, mydb, params=(u_id,))

            if df.empty:
                st.warning("No messages found for the given Employee ID.")
            else:
                st.markdown(f"<h4 style='text-align: center;'>Messages Sent by Employee ID: {u_id}</h4>", unsafe_allow_html=True)
                st.table(df)

            mydb.close()
        else:
            st.warning("Please enter your id first to view your messages.")
        


    if submit:
        mydb=create_connection()
        c=mydb.cursor()
        query="INSERT INTO message_from_employee(emp_id,message) values (%s,%s)"
        c.execute(query,(id,message))
        mydb.commit()
        c.close()
        st.success("Message Sent")
        st.rerun()

#-------------------end-------------------------

 #-------------LOGIN SUCCESS DIALOG BOX------  
@st.dialog("Success")
def login_success():
       st.success("Sign in successfully")
       proceed_btn=st.button("Proceed to Work")
       if proceed_btn:
           st.rerun()

#-------------LOGIN EMPLOYEE---------
   
c1, c2, c3 = st.columns([1,3,1])
    
if 'signin' not in st.session_state:
    st.session_state['signin'] = False
    
if not st.session_state['signin']:
    with c2:
        st.markdown("<h2 style='text-align: left;'>Sign in</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: left;'>to access CMS portal</h4>", unsafe_allow_html=True)
        u_type = st.selectbox("Department", ("HR", "Finance", "Marketing", "Sales", "IT", "Operations",
                            "Customer Service", "R&D", "Legal", "Procurement", "Administration", "PR"))
        u_id = st.text_input("User ID")
        u_pass = st.text_input("Password", type="password")
        btn = st.button("Sign in")

    if btn:
        mydb = create_connection()
        if mydb:  # Proceed only if the database connection is successful
            try:
                c = mydb.cursor()
                c.execute("SELECT * FROM user WHERE user_type=%s AND user_id=%s AND password=%s", (u_type, u_id, u_pass))
                result = c.fetchone()
                c.close()
                mydb.close()

                if result:
                    st.session_state['signin'] = True
                    login_success()                    
                else:
                    with c2:
                        st.error("Sign in failed, Please enter correct details")
            except Exception as e:
                st.error(f"An error occurred while verifying credentials: {e}")
        else:
            with c2:
                st.error("Unable to connect to the database. Please check Database connection.")
        
            
else:
    col1, col2=st.columns(2,gap="small",vertical_alignment="center")
    with col2:
        st.button("Logout", on_click=lambda: st.session_state.update({'signin': False}))
    with col1:   
        st.success("Welcome! You are logged_in as Employee.")
    
    # -------------------------------****** EMPLOYEE LOGIN END HERE ******----------------------------------------------
    
    
    #------------MESSAGE TO ADMIN-----------------
    if st.sidebar.button("✉️ Message to Admin"):
        contact_form()



#FEATURES INSIDE EMPLOYEE PORTAL      
    st.write("\n")
    st.write("\n")
    col1, col2=st.columns(2,gap="small",vertical_alignment="center")
    with col1:
        task=st.selectbox("Select Task",("View All Subscriber","Revenue and Subscriber Analysis","View Messages","Upload Subscriber Data","Delete Subscriber Data"),index=None,placeholder="Choose Your Task")

    st.write("\n")
# ALL SUBSCRIBER TABLE
    
    if task=="View All Subscriber":
        mydb=create_connection()
        query="SELECT * FROM customer"
        df=pd.read_sql(query,mydb)
            
        if df.empty:
            st.error("Data not found")
        else:
            st.markdown("<h4 style='text-align: center;'>All Subscriber Details</h4>", unsafe_allow_html=True)
            from st_aggrid import AgGrid, GridOptionsBuilder

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True) 
            gb.configure_side_bar()  
            gb.configure_default_column(editable=True, groupable=True) 
            grid_options = gb.build()

            AgGrid(
                df,
                gridOptions=grid_options,
                height=600,
                width='100%',
                theme='streamlit', 
                enable_enterprise_modules=True,
                fit_columns_on_grid_load=True,
            )
            # -------------- END HERE -----------------
        st.write("\n")    
            
        
# ANALYSIS START HERE            
    
    elif task=="Revenue and Subscriber Analysis":
        st.markdown("<h3 style='text-align: left;'>📊 Revenue and Subscriber Analysis Dashboard</h3> ", unsafe_allow_html=True)
        mydb=create_connection()
        query="SELECT * FROM customer"
        df=pd.read_sql(query,mydb)
        col1, col2,col3=st.columns(3,gap="small",vertical_alignment="center")
        with col1:
            task1=st.selectbox("Choose Analysis",("Revenue Analysis","Subscriber Analysis"),index=None)
        
    #SUBSCRIBER ANALYSIS
        
        if task1=="Subscriber Analysis":
            col1, col2=st.columns(2,gap="small",vertical_alignment="center")
            with col1:
                task2=st.selectbox("Choose a Visualization:",(
            "Subscriber by Gender (Bar Chart)",
            "Subscriber by Age (Bar Chart)",
            "Subscriber by Device (Bar Chart)",
            "Subscriber by Country (Bar Chart)",
            "Subscriber by Plan (Pie Chart)"
            ),index=None,placeholder="Choose a visualization")
            
            st.sidebar.markdown("<h5>Apply Filters</h5>", unsafe_allow_html=True)
            
        # FILTER BY AGE
            age_filter = st.sidebar.slider("Select Age Range", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(int(df['Age'].min()), int(df['Age'].max())))
            filtered_df = df[(df['Age'] >= age_filter[0]) & (df['Age'] <= age_filter[1])]

        # FILTER BY GENDER
            gender_filter = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
            filtered_df = filtered_df[filtered_df['Gender'].isin(gender_filter)]

        # FILTER BY DEVICE
            device_filter = st.sidebar.multiselect("Select Device", options=df['Device'].unique(), default=df['Device'].unique())
            filtered_df = filtered_df[filtered_df['Device'].isin(device_filter)]

        # VISUALIZATION START HERE
        
            # GENDER WISE SUBSCRIBER
            if task2 == "Subscriber by Gender (Bar Chart)":
                device_counts = filtered_df['Gender'].value_counts().reset_index()
                device_counts.columns = ['Gender', 'Count']

                fig = px.bar(
                    device_counts, 
                    x='Gender', 
                    y='Count', 
                    title=' Subscriber by Gender',
                    text='Count',
                    color='Gender',
                    template='plotly_white'
                )

                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title='Gender',
                    yaxis_title='Number of Subscriber',
                    showlegend=False
                )
                st.plotly_chart(fig)
                
                
            # AGE WISE SUBSCRIBER
            
            elif task2 == "Subscriber by Age (Bar Chart)":
                device_counts = filtered_df['Age'].value_counts().reset_index()
                device_counts.columns = ['Age', 'Count']

                fig = px.bar(
                    device_counts, 
                    x='Age', 
                    y='Count', 
                    title='Subscriber by Age',
                    text='Count',
                    color='Age',
                    template='plotly_white'
                )

                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title='Age',
                    yaxis_title='Subscriber',
                    showlegend=False
                )

                st.plotly_chart(fig)
            
            # COUNTRY WISE SUBSCRIBER
            
            elif task2 == "Subscriber by Country (Bar Chart)":
                
                device_counts = filtered_df['Country'].value_counts().reset_index()
                device_counts.columns = ['Country', 'Count']


                fig = px.bar(
                    device_counts, 
                    x='Country', 
                    y='Count', 
                    title='Subscriber by Country',
                    text='Count',
                    color='Country',  # Optional: color code by Country
                    template='plotly_white'
                )


                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title='Country',
                    yaxis_title='Subscriber',
                    showlegend=False
                )

                st.plotly_chart(fig)
                
            # DEVICE WISE SUBSCRIBER
            
            elif task2 == "Subscriber by Device (Bar Chart)":
                device_counts = filtered_df['Device'].value_counts().reset_index()
                device_counts.columns = ['Device', 'Count']

                fig = px.bar(
                    device_counts, 
                    x='Device', 
                    y='Count', 
                    title='Subscriber by Device',
                    text='Count',
                    color='Device',  
                    template='plotly_white'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title='Device',
                    yaxis_title='Subscriber',
                    showlegend=False
                )

                st.plotly_chart(fig)

            # PLAN WISE SUBSCRIBER
            
            elif task2 == "Subscriber by Plan (Pie Chart)":        
                subscription_counts = filtered_df['Subscription Type'].value_counts().reset_index()
                subscription_counts.columns = ['Plan', 'Count']

                # Creating the pie chart using plotly express
                fig = px.pie(subscription_counts, 
                            names='Plan', 
                            values='Count', 
                            title='Subscriber by Plan')

                st.plotly_chart(fig)
                        
       
        #REVENUE ANALYSIS
        
        if task1=="Revenue Analysis":
            col1, col2=st.columns(2,gap="small",vertical_alignment="center")
            with col1:
                #st.markdown("<h4 style='text-align: center;'>Select Visualization Type</h4>", unsafe_allow_html=True)
                chart_type = st.selectbox("Choose a Visualization:", (
                "Monthly Revenue Trend (Line Chart)",
                "Revenue by Subscription Type (Bar Chart)",
                "Revenue by Country (Bar Chart)",
                "Gender-based Revenue Analysis (Pie Chart)",
                "Device-based Revenue Distribution (Bar Chart)",
                "Age Group Revenue Analysis (Bar Chart)"
            ),index=None,placeholder="Choose a Visualization")
            df['Join Date'] = pd.to_datetime(df['Join Date'], errors='coerce')
            df['Last Payment Date'] = pd.to_datetime(df['Last Payment Date'], errors='coerce')
            
            st.sidebar.markdown("<h5>Apply Filters</h5>", unsafe_allow_html=True)
            country_filter = st.sidebar.multiselect("Select Country:", options=df['Country'].unique(), default=df['Country'].unique())
            df = df[df['Country'].isin(country_filter)]
            
            # Subscription type filter
            subscription_filter = st.sidebar.multiselect("Select Subscription Type:", options=df['Subscription Type'].unique(), default=df['Subscription Type'].unique())
            df = df[df['Subscription Type'].isin(subscription_filter)]
            
            # Age range filter
            min_age, max_age = st.sidebar.slider("Select Age Range:", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(int(df['Age'].min()), int(df['Age'].max())))
            df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]
            
    
            if chart_type == "Monthly Revenue Trend (Line Chart)":
                df['Month'] = df['Last Payment Date'].dt.strftime('%B')
                monthly_revenue = df.groupby('Month')['Monthly Revenue'].sum().reindex(
                    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                )
                fig = px.line(monthly_revenue, x=monthly_revenue.index, y=monthly_revenue, title='Monthly Revenue Trend', markers=True, labels={'x': 'Month','y': 'Revenue'})
                st.plotly_chart(fig)
        
            elif chart_type == "Revenue by Subscription Type (Bar Chart)":
                revenue_by_subscription = df.groupby('Subscription Type')['Monthly Revenue'].sum().sort_values()
                fig = px.bar(revenue_by_subscription, x=revenue_by_subscription.index, y=revenue_by_subscription, title='Revenue by Subscription Type',labels={'x': 'Subscription Type', 'y': 'Revenue'})
                st.plotly_chart(fig)
                
            elif chart_type == "Revenue by Country (Bar Chart)":
                revenue_by_country = df.groupby('Country')['Monthly Revenue'].sum().sort_values()
                fig = px.bar(revenue_by_country, x=revenue_by_country.index, y=revenue_by_country, title='Revenue by Country', labels={'x': 'Country', 'y': 'Revenue'})
                st.plotly_chart(fig)
                
            elif chart_type == "Gender-based Revenue Analysis (Pie Chart)":
                revenue_by_gender = df.groupby('Gender')['Monthly Revenue'].sum()
                fig = px.pie(revenue_by_gender, names=revenue_by_gender.index, values=revenue_by_gender, title='Revenue by Gender')
                st.plotly_chart(fig)
            
            elif chart_type == "Device-based Revenue Distribution (Bar Chart)":
                revenue_by_device = df.groupby('Device')['Monthly Revenue'].sum().sort_values()
                fig = px.bar(revenue_by_device, x=revenue_by_device.index, y=revenue_by_device, title='Revenue by Device', labels={'x': 'Device', 'y': 'Revenue'})
                st.plotly_chart(fig)
                
            elif chart_type == "Age Group Revenue Analysis (Bar Chart)":
                bins = [20, 30, 40, 50, 60]
                labels = ['20-30', '31-40', '41-50', '51-60']
                df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
                revenue_by_age_group = df.groupby('Age Group')['Monthly Revenue'].sum()
                fig = px.bar(revenue_by_age_group, x=revenue_by_age_group.index, y=revenue_by_age_group, title='Revenue by Age Group', labels={'x': 'Age Group', 'y': 'Revenue'})
                st.plotly_chart(fig)




    if task=="View Messages":
        mydb=create_connection()
        query="SELECT * FROM message"
        df=pd.read_sql(query,mydb)
            
        if df.empty:
            st.error("Data not found")
        else:
            st.markdown("<h4 style='text-align: center;'>All Messages</h4>", unsafe_allow_html=True)
            from st_aggrid import AgGrid, GridOptionsBuilder

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True) 
            gb.configure_side_bar()  
            gb.configure_default_column(editable=True, groupable=True) 
            grid_options = gb.build()

            AgGrid(
                df,
                gridOptions=grid_options,
                height=200,
                width='100%',
                theme='streamlit', 
                enable_enterprise_modules=True,
                fit_columns_on_grid_load=True,
            )



    if task=="Upload Subscriber Data":
        st.markdown("<h4 style='text-align: center;'>Upload data to Subsciber Data</h4>", unsafe_allow_html=True)

    # File uploader to upload CSV
        uploaded_file = st.file_uploader(":file_folder: Choose a CSV file", type=["csv"])
        st.info("Ensure that the date format is in yyyy-mm-dd. And your CSV file columns are in the order: Subscription Type, Monthly Revenue, Join Date, Last Payment Date, Country, Age, Gender, Device, Plan Duration.")
        upload_btn=st.button("Upload")
        if uploaded_file is not None:
            if upload_btn:
            
                st.write("File uploaded successfully!")
                
                # Create MySQL connection
                try:
                    mydb = create_connection()
                    if mydb.is_connected():
                        st.success("Connected to MySQL database")
                        
                        # Insert data from CSV
                        insert_data_from_csv(uploaded_file, mydb)
                        st.success("Data inserted into MySQL successfully!")
                        
                except Error as e:
                    st.error(f"Error: {e}")
                
                finally:
                    if mydb.is_connected():
                        mydb.close()
                        st.write("MySQL connection is closed")

    if task=="Delete Subscriber Data":
        delete_option=st.selectbox("Choose Delete Option",["Delete All Data","Delete by Range","Delete Single Data"],index=None)

        if delete_option=="Delete All Data":
            st.info("Caution: This option deletes all the customer data available in the database, the this action cannot be reversed")
            if st.button("Delete All Data"):
                 delete_all_data()

        elif delete_option=="Delete by Range":
            start_id=st.number_input("Enter Start ID",min_value=1,step=1)
            end_id=st.number_input("Enter End ID",min_value=1,step=1)
            if st.button("Delete Data"):
                if start_id and end_id and start_id<=end_id:
                    delete_data_by_range(start_id,end_id)
                else:
                    st.error("Please enter Valid Range")
        elif delete_option=="Delete Single Data":
            id=st.number_input("Enter ID",min_value=1,step=1)
            if st.button("Delete Data"):
                if id:
                    delete_single_data(id)
                else:
                    st.error("Please enter Valid ID")









