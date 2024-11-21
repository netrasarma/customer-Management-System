import streamlit as st


st.title("Customer Management System:")

st.subheader("Introduction:")
st.write("""
    The Customer Management System provides a strong base through which subscriber information and employee accounts can be managed efficiently 
    and internal communication carried out within an organization. To smoothen up the process of handling customer information, contact interactions, 
    and data insight gathering with maximum data integrity levels and user-friendliness levels, this project was proposed.
""")

st.subheader("Purpose and Objectives:")
st.write("""
    The main function of the CMS will be to provide a whole solution addressing complexity in data management and analysis. The system was developed based on the following objectives:
""")
st.markdown("""
- **Centralized Subscriber and Employee Data Management**: This can ensure that access is easy, and storage is reliable.
- **Improved Communication**: Direct messaging among employees and the administration to help facilitate better interaction.
- **Data-Driven Decision-Making**: Powerful tools are offered for the analysis of revenue and subscriber metrics for strategic planning and growth initiatives.
""")

st.subheader("Key Features:")
st.write("""
    The Customer Management System includes the following key features for both Admin and Employee Portals:
""")

st.markdown("""
1. **Admin Portal**:
    - **User Authentication**: Secure login system for admin access.
    - **Employee Account Management**: Create, view, update, and delete employee accounts.
    - **Message Management**: View and respond to employee-submitted messages, with status tracking capabilities.

2. **Employee Portal**:
    - **Direct Communication with Admins**: Send messages to report issues or request data updates.
    - **Subscriber Data Management**:
        - **View Subscriber Details**: Access comprehensive subscriber information.
        - **Add Subscriber Data**: Upload and integrate CSV files for bulk data entry.
        - **Delete Subscriber Data**: Options to delete all data, data by range, or single records by ID.
    - **Revenue and Subscriber Analysis**:
        - **Revenue Analysis**: Visualize trends with charts like monthly revenue, revenue by type, country, and more.
        - **Subscriber Analysis**: Break down subscriber data by demographics, device usage, and plan types.
""")

st.subheader("Technology Used:")
st.write("""
    - **Frontend**: Streamlit, HTML
    - **Backend**: Python, MySQL
    - **Security**: Email validation
""")

st.subheader("Conclusion:")
st.write("""
    The CMS is an effective platform that provides powerful data management as well as informative analysis. It has empowered employees to keep current 
    subscriber records, make administrative tasks less complicated, and provide them with the tools needed for meaningful analysis of revenue and subscriber data. 
    In this regard, organizations may use it in order to enhance their efficiency in operations and data-driven decision-making processes.
""")