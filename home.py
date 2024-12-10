import streamlit as st

st.set_page_config(
    page_title="Drowsiness Detection System",
    page_icon=""
    )

st.markdown("<h4 style='text-align: center;'>Welcome to</h4>",unsafe_allow_html=True) 
st.markdown("<h2 style='text-align: center;'>Drowsiness Detection System</h2>",unsafe_allow_html=True)
st.markdown('<style>div.block-container{padding-top:3rem}</style',unsafe_allow_html=True)
st.write("\n")
st.image("dds.jpg")

st.subheader("Purpose")
st.write("This system is designed to help prevent accidents caused by driver fatigue by detecting drowsiness in real-time.")

st.subheader("Key Features")
st.markdown("""
- **Real-time Detection**: Identify drowsiness using eye status (open or closed) effectively.
- **User-Friendly Interface**: Simple and intuitive design for easy use.
- **High Accuracy**: Powered by a robust Convolutional Neural Network (CNN) model trained on eye-state data.
""")

st.subheader("How It Works")
st.markdown("""
- Captures live video feed or images.
- Analyzes the state of the eyes (open or closed).
- Alerts users when signs of drowsiness are detected.
""")

st.subheader("Why Use This System?")
st.write("""
- Enhance road safety by reducing the risk of accidents.
- Easy integration with existing systems.
""")
