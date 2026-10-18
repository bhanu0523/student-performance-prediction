
import streamlit as st
import pandas as pd

from snowflake_inference import predict_exam_score, FEATURE_NAMES


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        color: #808080;
        margin-bottom: 2rem;
    }

    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.3);
        text-align: center;
        margin-top: 1rem;
    }

    .score {
        font-size: 2.8rem;
        font-weight: bold;
    }

    .small-text {
        color: #808080;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 Student Performance Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict a student’s expected exam score using a Machine Learning model '
    'deployed on Snowflake.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# Model Information
# --------------------------------------------------

with st.expander("About this project", expanded=False):
    st.write(
        """
        This application predicts a student's expected exam score based on
        academic, learning, and personal factors.

        - **Platform:** Snowflake ML
        - **Model:** STUDENT_PERFORMANCE_PREDICTOR
        - **Version:** V1
        - **Application:** Streamlit
        - **Prediction type:** Regression
        """
    )


# --------------------------------------------------
# Input Form
# --------------------------------------------------

st.subheader("Enter Student Details")

st.write(
    "Provide the following information to estimate the student's exam score."
)

with st.form("student_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        study_hours = st.number_input(
            "Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=3.0,
            step=0.5,
            help="Average hours spent studying per day."
        )

        attendance = st.slider(
            "Attendance (%)",
            min_value=0,
            max_value=100,
            value=80
        )

        resources = st.selectbox(
            "Access to Learning Resources",
            options=[0, 1, 2, 3, 4, 5],
            index=3,
            help="Use the same numerical encoding as the training dataset."
        )

        extracurricular = st.selectbox(
            "Extracurricular Activities",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        motivation = st.slider(
            "Motivation Level",
            min_value=1,
            max_value=5,
            value=3
        )

        internet = st.selectbox(
            "Internet Access",
            options=[0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        gender = st.selectbox(
            "Gender Code",
            options=[0, 1],
            help="Choose the numerical code used in the training dataset."
        )

    with col2:
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=20,
            step=1
        )

        learning_style = st.selectbox(
            "Learning Style Code",
            options=[0, 1, 2, 3],
            help="Use the numerical encoding from the training dataset."
        )

        online_courses = st.number_input(
            "Number of Online Courses",
            min_value=0,
            max_value=100,
            value=2,
            step=1
        )

        discussions = st.number_input(
            "Discussion Participation",
            min_value=0,
            max_value=100,
            value=3,
            step=1
        )

        assignment_completion = st.slider(
            "Assignment Completion (%)",
            min_value=0,
            max_value=100,
            value=80
        )

        edutech = st.selectbox(
            "Educational Technology Usage",
            options=[0, 1, 2, 3, 4, 5],
            help="Use the numerical encoding from the training dataset."
        )

        stress_level = st.slider(
            "Stress Level",
            min_value=1,
            max_value=5,
            value=3
        )

    submitted = st.form_submit_button(
        "Predict Exam Score",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if submitted:

    input_values = {
        "STUDYHOURS": study_hours,
        "ATTENDANCE": attendance,
        "RESOURCES": resources,
        "EXTRACURRICULAR": extracurricular,
        "MOTIVATION": motivation,
        "INTERNET": internet,
        "GENDER": gender,
        "AGE": age,
        "LEARNINGSTYLE": learning_style,
        "ONLINECOURSES": online_courses,
        "DISCUSSIONS": discussions,
        "ASSIGNMENTCOMPLETION": assignment_completion,
        "EDUTECH": edutech,
        "STRESSLEVEL": stress_level
    }

    # Confirm all model input features are present.
    if set(input_values.keys()) != set(FEATURE_NAMES):
        st.error(
            "Input features do not match the deployed model's expected features."
        )

    else:
        with st.spinner("Connecting to Snowflake and predicting exam score..."):

            try:
                predicted_score = predict_exam_score(input_values)

                # Keep the predicted value within the displayed score range.
                displayed_score = max(0.0, min(100.0, predicted_score))

                st.divider()
                st.subheader("Prediction Result")

                result_col1, result_col2 = st.columns(2)

                with result_col1:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="small-text">Predicted Exam Score</div>
                            <div class="score">{displayed_score:.2f}</div>
                            <div class="small-text">Out of 100</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with result_col2:
                    if displayed_score >= 75:
                        performance_band = "Excellent"
                    elif displayed_score >= 60:
                        performance_band = "Good"
                    elif displayed_score >= 40:
                        performance_band = "Average"
                    else:
                        performance_band = "Needs Improvement"

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="small-text">Performance Category</div>
                            <div class="score" style="font-size:2rem;">
                                {performance_band}
                            </div>
                            <div class="small-text">
                                Based on the predicted score
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.info(
                    "This is a machine learning estimate, not a guaranteed exam result."
                )

                with st.expander("View submitted student details"):
                    display_data = pd.DataFrame(
                        [input_values]
                    ).T.reset_index()

                    display_data.columns = ["Feature", "Value"]

                    st.dataframe(
                        display_data,
                        use_container_width=True,
                        hide_index=True
                    )

            except Exception as error:
                st.error("Unable to generate the prediction.")

                st.write(
                    "Please check your Snowflake service, authentication "
                    "token configuration, and network connection."
                )

                with st.expander("Technical error details"):
                    st.code(str(error))


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Student Performance Prediction | Streamlit + Snowflake ML"
)
