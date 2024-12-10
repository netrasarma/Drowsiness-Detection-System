import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
from pygame import mixer

#Sound
try:
    mixer.init()
    sound = mixer.Sound('alarm.wav')
    audio_supported = True
except Exception as e:
    st.warning(f"Audio support is unavailable: {e}")
    audio_supported = False

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(r'face.xml')
leye_cascade = cv2.CascadeClassifier(r'lefteye.xml')
reye_cascade = cv2.CascadeClassifier(r'righteye.xml')

# Load the trained model
model = load_model('drowsy.h5')


# Initialize session state
if "detection_running" not in st.session_state:
    st.session_state.detection_running = False

def drowsiness_detection(video_source, model, face_cascade, leye_cascade, reye_cascade):
    cap = cv2.VideoCapture(video_source)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    score = 0
    thicc = 2
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    FRAME_WINDOW = st.image([])

    while st.session_state.detection_running:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to access the video source. Check your settings.")
            break

        # Process frame
        small_frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        gray_enhanced = clahe.apply(gray)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray_enhanced, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))

        for (x, y, w, h) in faces:
            cv2.rectangle(small_frame, (x, y), (x + w, y + h), (100, 100, 100), 1)
            roi_gray = gray_enhanced[y:y + h // 2, x:x + w]
            left_eye = leye_cascade.detectMultiScale(roi_gray)
            right_eye = reye_cascade.detectMultiScale(roi_gray)

            lpred = rpred = 1  # Default predictions to open eyes

            # Predict on left eye
            if len(left_eye) > 0:
                (lex, ley, lew, leh) = left_eye[0]
                l_eye = roi_gray[ley:ley + leh, lex:lex + lew]
                l_eye_resized = cv2.resize(l_eye, (64, 64))
                l_eye_colored = cv2.cvtColor(l_eye_resized, cv2.COLOR_GRAY2RGB)
                l_eye_normalized = l_eye_colored / 255
                l_eye_reshaped = l_eye_normalized.reshape(1, 64, 64, 3)
                lpred = np.argmax(model.predict(l_eye_reshaped), axis=1)[0]

            # Predict on right eye
            if len(right_eye) > 0:
                (rex, rey, rew, reh) = right_eye[0]
                r_eye = roi_gray[rey:rey + reh, rex:rex + rew]
                r_eye_resized = cv2.resize(r_eye, (64, 64))
                r_eye_colored = cv2.cvtColor(r_eye_resized, cv2.COLOR_GRAY2RGB)
                r_eye_normalized = r_eye_colored / 255
                r_eye_reshaped = r_eye_normalized.reshape(1, 64, 64, 3)
                rpred = np.argmax(model.predict(r_eye_reshaped), axis=1)[0]

            # Update score based on predictions
            if rpred == 0 and lpred == 0:
                score = max(0, score - 1)
                
                cv2.putText(small_frame, "Eyes Open", (10, 60), font, 1, (0, 255, 0), 2)
            else:
                score += 1
                cv2.putText(small_frame, "Eyes closed", (10, 60), font, 1, (0, 0, 255), 2)

            cv2.putText(small_frame, f'Score: {score}', (10, 30), font, 1, (0, 0, 255), 2)
            
            # Trigger alarm for drowsiness
            if score > 12:
                try:
                    #sound.play()
                    cv2.putText(small_frame, "Please Wake Up", (220, 450), font, 1, (0, 0, 255), 2)
                except:
                    pass
                thicc = min(thicc + 2, 16)
                cv2.rectangle(small_frame, (0, 0), (small_frame.shape[1], small_frame.shape[0]), (0, 0, 255), thicc)

        # Display the frame
        frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame_rgb)

    cap.release()

st.markdown("<h1 style='text-align:center;'>Drowsiness Detection System</h1>", unsafe_allow_html=True)

st.write("\n")
st.write("\n")
st.write("\n")

st.sidebar.title("Select Camera Option")

choice=st.sidebar.selectbox("Video Source",["📷 Camera","🔗 URL","🎥 Video"],index=None,placeholder="Choose an Option")



if choice=="📷 Camera":

    st.sidebar.title("Camera Settings")
    camera_choice = st.sidebar.selectbox("Select Camera Type", ["Primary", "Secondary", "IP Camera"], index=None,placeholder="Choose an Camera Option")
    if camera_choice == "Primary":

        if st.sidebar.button("Start Detection"):

            stop_detect=st.sidebar.button("Stop Detection")

            if stop_detect:  
                st.session_state.detection_running = False

            st.session_state.detection_running = True
            camera_id = 0
            drowsiness_detection(camera_id, model, face_cascade, leye_cascade, reye_cascade)
                

    elif camera_choice == "Secondary":

        if st.sidebar.button("Start Detection"):

            stop_detect=st.sidebar.button("Stop Detection")
            if stop_detect:  
                st.session_state.detection_running = False
            st.session_state.detection_running = True
            camera_id = 1
            drowsiness_detection(camera_id, model, face_cascade, leye_cascade, reye_cascade)

            


    elif camera_choice == "IP Camera":
            camera_id = st.text_input("Enter IP Camera URL")
            st.info("Example: http://192.0.0.4:8080/video")
            c1,c2,c3=st.columns(3)
            with c1:
                detect=st.button("Start Detection")
            if detect:
                with c2:
                    stop_detect=st.button("Stop Detection")
                if stop_detect:  
                    st.session_state.detection_running = False

                st.session_state.detection_running = True
                drowsiness_detection(camera_id, model, face_cascade, leye_cascade, reye_cascade)

    
        
elif choice=="🔗 URL":
    url=st.text_input("Enter Your URL")
    st.info('Please upload a video file to start detection.')
    c1,c2,c3=st.columns(3)
    with c1:
        detect=st.button("Start Detection")
    if detect:
        with c2:
            stop_detect=st.button("Stop Detection")
        if stop_detect:  
            st.session_state.detection_running = False

        st.session_state.detection_running = True

        drowsiness_detection(
            url, model, face_cascade, leye_cascade, reye_cascade
        )


elif choice=="🎥 Video": 
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
        
        st.success("Video uploaded successfully.")
        
        c1,c2,c3=st.columns(3)
        with c1:
            detect=st.button("Start Detection")
        if detect:
            with c2:
                stop_detect=st.button("Stop Detection")
            if stop_detect:  
                st.session_state.detection_running = False

            st.session_state.detection_running = True

            drowsiness_detection(
                "temp_video.mp4", model, face_cascade, leye_cascade, reye_cascade
            )
    else:
        st.info("Please upload a video file to start detection.")
import os
if os.path.exists("temp_video.mp4"):
    os.remove("temp_video.mp4")

     
