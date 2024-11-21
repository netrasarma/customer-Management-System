import streamlit as st

# ---------- PAGE SETUP -------------

home_page=st.Page(
    page="home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
employee=st.Page(
    page="Employee_Portal.py",
    title="Employee Portal",
    icon=":material/manage_accounts:",
)
admin=st.Page(
    page="Admin_Portal.py",
    title="Admin Portal",
    icon=":material/admin_panel_settings:",
)
contact=st.Page(
    page="contact.py",
    title="Contact",
    icon=":material/contact_phone:",
)
about=st.Page(
    page="About.py",
    title="About",
    icon=":material/groups:",
)

# ----------- Navigation------------

page=st.navigation(pages=[home_page,employee,admin,contact,about])
page.run()



#--------- Logo for all page------------
st.logo("CMS\icons\logom.png")




