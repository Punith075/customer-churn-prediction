# ChurnIQ AI – Customer Churn Prediction & Retention Analytics

An AI-powered customer analytics platform that predicts customer churn using Machine Learning and provides actionable insights to improve customer retention.

## Project Overview

Customer churn is a major challenge for subscription-based businesses. ChurnIQ AI analyzes customer information, identifies churn patterns, and predicts the probability of a customer leaving a service.

## Features

- Customer churn prediction using Machine Learning.
- Interactive business analytics dashboard.
- Customer churn distribution visualization.
- Contract-wise and tenure-wise churn analysis.
- Internet service and billing analysis.
- Retention strategy recommendations.
- Model performance and feature importance analysis.

## Machine Learning Models

- Logistic Regression
- Random Forest

**Selected Model:** Logistic Regression

### Model Performance

| Metric | Score |
|---|---:|
| Accuracy | 73.81% |
| Precision | 50.43% |
| Recall | 78.34% |
| F1-Score | 61.36% |
| ROC-AUC | 84.13% |

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Plotly
- Streamlit
- Joblib

## Dataset

IBM Telco Customer Churn Dataset

- 7,043 customer records
- 21 original columns
- Binary classification problem

## Run Locally

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Navigate to the project folder:

   `cd customer_churn_project`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Run the application:

   `streamlit run app.py`

## Project Structure

```text
customer_churn_project/
├── app.py
├── customer_churn_model.pkl
├── feature_importance.csv
├── model_comparison.csv
├── telco_churn_data.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Future Enhancements

- Customer segmentation.
- Explainable AI.
- Downloadable prediction reports.
- Customer lifetime value analysis.
- Live business data integration.

---

**Developed as a Data Science and Machine Learning project.**