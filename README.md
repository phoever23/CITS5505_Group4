# CITS5505_Group4

## Project Description

A budget-tracking web application that allows users to record and manage their expenses, categorize them, visualize spending patterns, and share data with others.

The main features include:

1. Upload and Record Expenses

   Users can manually input or upload expense records (e.g. CSV files) to keep track of their daily spending.

2. Category Management

   The system will record the expenditure by 5 categories, including Housing, Food, Shopping, Education, and Others.

3. Data Visualization

   Various types of charts are displayed through the dashboard, such as expenditure trend charts, category percentage charts, Top 5 highest expenses, etc.

4. Historical Export

   Users can export their dashboard as a PDF or PNG file to keep a visual record of their spending.

5. Data Sharing

   Users can select a custom time range and share their expense data with other users on the platform — such as a partner or roommate — to improve transparency and collaborative budgeting.

6. Future Feature: Expense Prediction

   Planned functionality to predict future expenses based on past trends and notify users to adjust their budgets accordingly.

## Group Members

| UWA ID   | Name                            | GitHub Username | Main Contribution                                                       |
| -------- | ------------------------------- | --------------- | ----------------------------------------------------------------------- |
| 24177876 | Ming Gao                        | phoever23       | Share data view, database setup, user authentication, github management |
| 24350939 | Jianing Wang                    | zhazha-1004     | Homepage design, project description                                    |
| 24297797 | Gayathri Kasunthika Kanakaratne | GayaKasun2401   | Dashboard view, unit tests                                              |
| 24345651 | Niranjan Vasudevan              | niranjan-v2     | Upload view, selenium tests, bugs and issues                            |

Note: Commit `5477df1` on May 6, 2025, which appears under Ming’s name, was actually authored by Gayathri. Due to time constraints, Gayathri was unable to push the commit to GitHub herself, so Ming pushed it on her behalf. The work in this commit should be credited to Gayathri.

## Launch the Application

Follow these steps to set up and run the application:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/phoever23/CITS5505_Group4.git
   cd CITS5505_Group4
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   # or
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

   - **Windows:**

     ```bash
     .\venv\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations**

   After installing the dependencies, apply the latest database schema with

   ```bash
   flask db upgrade
   ```

6. **Run the Application**

   ```bash
   python app.py
   # or
   python3 app.py
   ```

Visit `http://127.0.0.1:5000/` in your browser to access the app.

## Run the Tests

### Unit Tests

To run the unit tests:

1. Make sure your virtual environment is activated.
2. From the root directory of the project, run:

   ```bash
   python -m unittest tests.test_app
   ```

This will execute 13 unit tests covering key components of the application.

### Selenium Tests

To run the end-to-end Selenium tests:

1. Navigate to the `tests/selenium` directory:

   ```bash
   cd tests/selenium
   ```

2. Then run:

   ```bash
   python test_suite/signup_test.py
   python test_suite/login_test.py
   python test_suite/logout_test.py
   python test_suite/manualUpload_test.py
   python test_suite/share_test.py
   ```

These tests cover core user flows such as sign up, login, logout, manual expense upload, and sharing functionality.
