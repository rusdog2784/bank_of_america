# Bank of America Python Module
This repository contains a python module for getting Bank of America account information using selenium's chromedriver. 


## Getting Started
See below for everything you need to get started.


### Prerequisites
Create a file called `.env` and place it inside the parent directory (same directory as the `run.py`) so that your project structure looks like this:
```
> bank_of_america
.env
.gitignore
README.md
requirements.txt
run.py
```
Within the `.env` file, add the following details (any instructions inside <> characters are for details you need to fill in):
   ```
   [credentials]
   BANK_OF_AMERICA_USERNAME = <Your Online ID>
   BANK_OF_AMERICA_PASSWORD = <Your Password>

   [security_questions]
   <Security question #1, word for word> = <Security question #1's answer>
   <Security question #2, word for word> = <Security question #2's answer>
   <Security question #3, word for word> = <Security question #3's answer>
   ```
An example of a security question, word for word, and its subsequent answer would look like this:
```
What is the name of your first job? = McDonalds
```
NOTE: If you want to reset your security questions, you can do so by:
   1) Logging into your Bank of America portal.
   2) Hover over "Profile & Settings".
   3) Click on "Security Center".
   4) Find and click on the link that says "Change my challenge questions".


### Installing
All you have to install are the package dependencies and you can do so by running the command:
```
pip install -r requirements.txt
```


### Running the Program
To execute the base program, which connects to your Bank of America account and fetches your up-to-date checking account balance, simply run the command:
```
python run.py
```