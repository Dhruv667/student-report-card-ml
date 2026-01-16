import streamlit as st
import joblib
import numpy as np
import pandas as pd

@st.cache_resource
def load_model():
    return joblib.load("student_report_model.pkl")

model = load_model()

st.title("🎓 Student Report Card & Pass/Fail Prediction System")

name = st.text_input("Enter Student Name")
roll_no = st.text_input("Enter Roll Number")
division = st.selectbox("Enter Division", ["A", "B", "C"])
standard = st.selectbox("Select Standard", ["10th", "12th"])

st.subheader("📚 Enter Subject Marks (out of 100)")

if standard == "10th":
    english = st.number_input("English", 0, 100)
    hindi = st.number_input("Hindi", 0, 100)
    marathi = st.number_input("Marathi", 0, 100)
    maths = st.number_input("Mathematics", 0, 100)
    science = st.number_input("Science", 0, 100)

    subjects = [english, hindi, marathi, maths, science]
    subject_names = ["English", "Hindi", "Marathi", "Mathematics", "Science"]

elif standard == "12th":
    physics = st.number_input("Physics", 0, 100)
    chemistry = st.number_input("Chemistry", 0, 100)
    maths = st.number_input("Mathematics", 0, 100)
    biology = st.number_input("Biology", 0, 100)
    english = st.number_input("English", 0, 100)

    subjects = [physics, chemistry, maths, biology, english]
    subject_names = ["Physics", "Chemistry", "Mathematics", "Biology", "English"]

if st.button("Generate Report Card"):

    total_marks = sum(subjects)
    percentage = (total_marks / 500) * 100
    average_marks = total_marks / 5

    if percentage > 90:
        grade = "A"
    elif percentage >= 71:
        grade = "B"
    elif percentage >= 51:
        grade = "C"
    elif percentage >= 35:
        grade = "D"
    else:
        grade = "F"

    input_data = np.array([[average_marks, percentage]])
    prediction = model.predict(input_data)

    if any(mark < 35 for mark in subjects):
        result = "FAIL"
    else:
        if prediction[0] == 1:
            result = "PASS"
        else:
            result = "FAIL"

    st.subheader("📄 Report Card")

    student_info = pd.DataFrame({
        "Field": ["Name", "Roll Number", "Division", "Standard"],
        "Value": [name, roll_no, division, standard]
    })

    st.subheader("📝 Student Details")
    st.table(student_info)

    marks_table = pd.DataFrame({
        "Subject": subject_names,
        "Marks Obtained": subjects,
        "Max Marks": [100, 100, 100, 100, 100]
    })

    st.subheader("📚 Subject-wise Marks")
    st.table(marks_table)

    summary_table = pd.DataFrame({
        "Metric": ["Total Marks", "Percentage", "Grade", "Result"],
        "Value": [
            f"{total_marks} / 500",
            f"{round(percentage, 2)} %",
            grade,
            result
        ]
    })

    st.subheader("📊 Result Summary")
    st.table(summary_table)

    if result == "PASS":
        st.success("✅ Result: PASS")
    else:
        st.error("❌ Result: FAIL")
