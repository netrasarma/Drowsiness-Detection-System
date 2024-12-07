
import streamlit as st

# ---------- PAGE SETUP -------------

home_page=st.Page(
    page="home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
dds=st.Page(
    page="drowsiness.py",
    title="Drowsiness Detection System",
    icon=":material/sentiment_content:",
)
about=st.Page(
    page="about.py",
    title="About",
    icon=":material/groups:",
)

# ----------- Navigation------------

page=st.navigation(pages=[home_page,dds,about])
page.run()



#--------- Logo for all page------------
#st.logo("CMS\icons\logom.png")
