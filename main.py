import streamlit as st

# ---------- PAGE SETUP -------------

home_page=st.Page(
    page="Pages/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
employee=st.Page(
    page="Pages/Employee_Portal.py",
    title="Employee Portal",
    icon=":material/manage_accounts:",
)
admin=st.Page(
    page="Pages/Admin_Portal.py",
    title="Admin Portal",
    icon=":material/admin_panel_settings:",
)
contact=st.Page(
    page="Pages/contact.py",
    title="Contact",
    icon=":material/contact_phone:",
)
about=st.Page(
    page="Pages/About.py",
    title="About",
    icon=":material/groups:",
)

# ----------- Navigation------------

page=st.navigation(pages=[home_page,employee,admin,contact,about])
page.run()



#--------- Logo for all page------------
st.logo("CMS\icons\logom.png")




