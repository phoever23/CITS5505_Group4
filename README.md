
# CITS5505_Group

## Project Description

An budget application that can track expense (user upload) and put them into different categories, create dashboard or other charts to demonstrate the historical data, and predict future income/expense.

## Development Environment Setup

This section guides you through setting up your local machine to work on the project. We will use a virtual environment (`venv`) to manage project dependencies.

### Prerequisites

Before you start, make sure you have the following installed on your computer:

1.  **Python 3:** Download from [python.org](https://www.python.org/downloads/ "null"). Ensure you have Python 3.x.
    
    -   Check your version in your terminal/command prompt:
        
        ```bash
        python --version
        # or sometimes
        python3 --version        
        ```
        
2.  **Git:** Download from [git-scm.com](https://git-scm.com/downloads "null").
    
    -   Check your version:
        
        ```bash
        git --version        
        ```
        

### Setup Steps

Follow these steps in your terminal or command prompt:

1.  Clone the Repository:
    
    If you haven't already, clone the project repository.
    
    ```bash
    git clone git@github.com:phoever23/CITS5505_Group4.git    
    ```
    
2.  Navigate into the Project Directory:
    
    Change your current directory to the cloned repository folder.
    
    ```bash
    cd CITS5505_Group4    
    ```
    
3.  Create a .gitignore file:
    
    It's important to tell Git to ignore certain files and directories that are specific to your local environment or are generated automatically (like the virtual environment). This prevents them from being accidentally committed to the repository.
    
    Create a file named `.gitignore` in the root of your project directory. You can do this using a text editor like VScode
       
    Open the `.gitignore` file in a text editor and add the following line to ignore the virtual environment directory:
    
    ```bash
    venv/    
    ```
    
    Save the file. The crucial line here is `venv/`, which tells Git to ignore the virtual environment directory we will create in the next step.
    
4.  Create a Virtual Environment:
    
    Now, create a virtual environment named venv inside the project directory. Git will ignore this directory because of the .gitignore file you just created.
    
    ```bash
    python -m venv venv
    # or if the above doesn't work, try:
    python3 -m venv venv    
    ```
    
    This command creates the `venv` folder.
    
5.  Activate the Virtual Environment:
    
    This step activates the environment, ensuring you use the correct Python and pip.
    
    **For macOS and Linux:**
    
    ```bash
    source venv/bin/activate    
    ```
    
    **For Windows (Command Prompt or PowerShell):**
    
    ```
    .\venv\Scripts\activate
    ```
    
    After activation, you should see `(venv)` at the start of your terminal prompt.
    
6.  Install Dependencies:
    
    With the virtual environment activated, install project dependencies from requirements.txt.
    
    ```bash
    pip install -r requirements.txt    
    ```
    
    This installs libraries like Flask into your activated virtual environment.

### Running the Application
To run the Flask application, first make sure your virtual environment is activated (Step 5 in Development Environment Setup). Then, navigate to the root of the project directory in your terminal and execute one of the following commands:
```bash
python app.py
# or
python3 app.py
```
This will start the Flask development server. You should see output in your terminal indicating that the server is running, usually with a URL (like http://127.0.0.1:5000/) where you can access the application in your web browser.
    
### Deactivating the Virtual Environment

When you are done working on the project, exit the virtual environment:

```bash
deactivate
```

Your terminal prompt will return to its normal state. Remember to **activate** the environment (Step 5) each time you return to work on the project.

## Workflow

Once your development environment is set up (see above), follow this workflow for contributing:

1.  Synchronize with the Main Branch:
    
    Switch to the main branch and ensure your local copy is up-to-date with the latest changes from the remote repository.
    
    ```bash
    git checkout main
    git pull origin main    
    ```
    
2.  Create and Work on a New Local Branch:
    
    Create a new branch for your specific feature, bug fix, or task. Replace [new-branch-name] with a descriptive name (e.g., feature/add-dashboard-chart, fix/login-bug).
    
    ```bash
    git checkout -b [new-branch-name]    
    ```
    
    Make your code changes locally within this new branch.
    
3.  Commit Your Changes:
    
    Stage your changes and create meaningful commits.
    
    ```bash
    git add .
    git commit -m "Concise description of changes"    
    ```
    
    Commit frequently with clear messages.
    
4.  Push the local branch to GitHub:
    
    Push your new branch and its commits to the remote GitHub repository. The --set-upstream flag is usually only needed the first time you push a new branch.
    
    ```bash
    git push --set-upstream origin <new-branch-name>    
    ```
    
5.  Create a Pull Request (PR) on GitHub:
    
    Go to the GitHub repository page. GitHub will usually show a banner prompting you to create a pull request for your recently pushed branch. Create the PR, providing a clear title and description of your changes, linking it to relevant issues if applicable.
    
6.  Code Review:
    
    Your team members will review your pull request. Be prepared to discuss your changes and make modifications based on their feedback. If you make further changes locally (after receiving comments), commit them and push to the same branch on GitHub. The PR will automatically update.
    
7.  Merge the Branch:
    
    Once the pull request is approved by the required reviewers, it can be merged into the main branch on GitHub.
    
8.  Delete the Local Branch:
    
    After your branch has been successfully merged into main on GitHub, you can delete your local copy of the branch to keep your repository clean. First, switch back to main.
    
    ```bash
    git checkout main
    git branch -d [new-branch-name]    
    ```
    

## Issue Tracking

We use GitHub Issues to track tasks, bugs, and feature requests.

-   Before starting work on something new, check the existing issues to see if it's already listed or being worked on.
    
-   Create a new issue for any bugs you find, features you want to propose, or tasks you plan to work on. Assign yourself to issues you are working on.
    
-   Reference issues in your commit messages or pull request descriptions using `#issue-number` (e.g., `Fixes #123`, `Implements #45`).
