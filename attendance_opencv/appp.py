import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import os
import random

CSV_FILE = "attendance.csv"
CAPTURE_FOLDER = "captures"
QUOTES = [
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Do something today that your future self will thank you for.",
    "Small steps every day lead to big results.",
    "Your only limit is your mind."
]

os.makedirs(CAPTURE_FOLDER, exist_ok=True)

st.title("📸 Face Attendance System")
st.write("Enter your Name and Roll Number, click Capture, and your attendance will be marked!")

name = st.text_input("Enter Name")
roll_no = st.text_input("Enter Roll Number")

# Use Streamlit camera input instead of OpenCV
img_file_buffer = st.camera_input("Take your photo")

if st.button("Capture Attendance"):
    if name.strip() == "" or roll_no.strip() == "":
        st.error("Please enter both Name and Roll Number!")
    elif img_file_buffer is None:
        st.error("Please take a photo!")
    else:
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"{CAPTURE_FOLDER}/{name}_{roll_no}_{timestamp}.png"
        img = Image.open(img_file_buffer)
        img.save(img_filename)

        # Save to CSV
        if not os.path.exists(CSV_FILE):
            df = pd.DataFrame(columns=["Name", "Roll No", "Time", "Image"])
        else:
            df = pd.read_csv(CSV_FILE)

        df = pd.concat([df, pd.DataFrame([{
            "Name": name,
            "Roll No": roll_no,
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Image": img_filename
        }])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        st.success(f"Attendance marked for {name} at {datetime.now().strftime('%H:%M:%S')}!")
        st.image(img, width=400)
        st.info(random.choice(QUOTES))

# Show attendance records
st.markdown("### 📋 Attendance Records")
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        for index, row in df.iterrows():
            img_path = row.get("Image", "")
            if isinstance(img_path, str) and os.path.exists(img_path):
                img = Image.open(img_path)
                st.image(img, width=200)
            st.write(f"**Name:** {row['Name']} | **Roll No:** {row['Roll No']} | **Time:** {row['Time']}")
    else:
        st.write("No attendance recorded yet.")
else:
    st.write("No attendance recorded yet.")
