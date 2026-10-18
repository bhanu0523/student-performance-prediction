
# Student Performance Prediction Using Snowflake ML

An end-to-end student exam score prediction system built using Snowflake ML, Snowpark Container Services, and Streamlit. The application accepts student details and predicts an estimated exam score.

## Project Overview

Student exam score prediction is a regression problem. The model predicts a numerical exam score using academic habits, attendance, learning preferences, and other student-related features.

A Random Forest Regressor was selected after comparing multiple regression algorithms. The trained model is registered in the Snowflake Model Registry and deployed through Snowpark Container Services for online predictions.

## Architecture

Student Performance Dataset
|
v
Snowflake table: ML_WORK.PUBLIC.STUDENT_PERFORMANCE
|
v
Data quality checks and duplicate removal
|
v
Feature preparation and group-based train/validation/test split
|
v
Regression model comparison and evaluation
|
v
Snowflake Model Registry: STUDENT_PERFORMANCE_PREDICTOR, version V1
|
v
Snowpark Container Service: STUDENT_PERFORMANCE_PREDICTION_SVC
|
v
Streamlit application

## Dataset

The dataset is stored in:

`ML_WORK.PUBLIC.STUDENT_PERFORMANCE`

The original dataset contains 14,003 rows and 16 columns.

The prediction target is `EXAMSCORE`. The `FINALGRADE` column is excluded from the model inputs to reduce the risk of target leakage.

The model uses these 14 input features:

| Column | Description |
|---|---|
| STUDYHOURS | Study hours |
| ATTENDANCE | Attendance |
| RESOURCES | Learning resource category |
| EXTRACURRICULAR | Extracurricular participation |
| MOTIVATION | Motivation category |
| INTERNET | Internet access |
| GENDER | Gender category |
| AGE | Student age |
| LEARNINGSTYLE | Learning style category |
| ONLINECOURSES | Number of online courses |
| DISCUSSIONS | Discussion participation |
| ASSIGNMENTCOMPLETION | Assignment completion |
| EDUTECH | Educational technology |
| STRESSLEVEL | Stress category |

## Data Preparation

The training workflow:

- Loads data from Snowflake.
- Checks missing values and invalid target values.
- Removes exact duplicate rows.
- Excludes `EXAMSCORE` and `FINALGRADE` from input features.
- Keeps identical feature combinations together during splitting.
- Creates training, validation, and testing datasets.

After duplicate removal, 12,469 rows remain. The split contains 7,481 training rows, 2,494 validation rows, and 2,494 testing rows.

## Model

Three regression algorithms are compared:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

The Random Forest Regressor is selected using validation RMSE. The final model is trained on the combined training and validation datasets.

## Evaluation Metrics

The held-out test results are:

| Metric | Value |
|---|---:|
| Mean Absolute Error (MAE) | 4.853 |
| Root Mean Squared Error (RMSE) | 7.817 |
| R-squared (R²) | 0.806 |

MAE measures the average absolute prediction error. RMSE gives greater weight to larger errors. R² measures performance relative to a mean-baseline predictor.

These metrics may change if the dataset or training process changes.

## Snowflake Model Registry

- Model: `STUDENT_PERFORMANCE_PREDICTOR`
- Version: `V1`
- Algorithm: Random Forest Regressor
- Target: `EXAMSCORE`

## Snowpark Container Services

The deployed service is:

`STUDENT_PERFORMANCE_PREDICTION_SVC`

The service exposes a prediction endpoint that accepts the 14 input features and returns an estimated exam score.

Authentication requires a valid Snowflake Personal Access Token (PAT) and appropriate Snowflake access policies.

## Repository Contents

| File | Purpose |
|---|---|
| `streamlit_app.py` | Collects student inputs and displays predictions |
| `snowflake_inference.py` | Sends requests to the deployed Snowflake endpoint |
| `requirements.txt` | Lists application dependencies |
| `.gitignore` | Excludes secrets and local development files |
| `README.md` | Project documentation |

## Prerequisites

- Python 3.9 or later
- A Snowflake account with the required ML and Snowpark Container Services access
- The registered model and deployed inference service
- A valid Snowflake PAT
- A GitHub account

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd student_performance_prediction
```

Create a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

For local development, create a `.env` file in the project directory:

```text
SNOWFLAKE_PAT=your_personal_access_token
```

Never commit `.env` or expose your token.

For Streamlit Community Cloud, configure `SNOWFLAKE_PAT` in the application's Secrets settings.

## Run the Application

Run the following command from the project directory:

```bash
streamlit run streamlit_app.py
```

The application sends the entered student details to the deployed Snowflake service and displays the estimated exam score.

## Deployment

The model is already registered in Snowflake and deployed through Snowpark Container Services.

To deploy the interface:

1. Push the application files to GitHub.
2. Create an application on Streamlit Community Cloud.
3. Select this GitHub repository.
4. Set `streamlit_app.py` as the main file.
5. Add `SNOWFLAKE_PAT` in the application's Secrets settings.
6. Deploy and test the prediction form.

The Snowflake service must remain available, and its authentication policies must allow authorized requests.

## Notes

- Predictions are estimates, not guaranteed exam results.
- `FINALGRADE` is excluded from the model inputs.
- Encoded categories should match the dataset's original encoding.
- Never upload credentials, virtual environments, or local model files.
