 
# 🎓 University Management System using Flask & MongoDB

This is a web application built using **Python (Flask)** and **MongoDB** that allows you to manage university data including **students, courses, and departments**.

It supports both a **web interface** and **RESTful APIs** for interacting with the data.
![Screenshot 2025-06-23 015257](https://github.com/user-attachments/assets/c1ff36ab-e104-49ac-8f0b-b0d8c00da742)

---

## Technologies Used

- Python 3.x
- Flask
- MongoDB (local)
- PyMongo (MongoDB driver)
- Jinja2 (HTML templating)
- Bootstrap (CSS styling)
- JavaScript (basic interactivity)

---

## Features

- Add, update, and delete students & courses
- View departments and assign students to courses
- API endpoints to query departments, courses, and students
- Aggregations to get:
  - Inactive / low-GPA students
  - Students grouped by department
  - Course-wise student counts
- GPA calculations and grade summarization
- Form validation & error handling with Flask Flash messages

---

## Folder Structure

```

/MongoDB-Project
│
├── app.py              # Main Flask app
├── mongo\_db.py         # MongoDB interaction class
├── templates/          # HTML templates (not detailed here)
├── static/             # CSS & JS files
├── requirements.txt    # Required packages
└── README.md           # Project description

````

---

🚀 How to Run Locally

1. Make sure you have Python and MongoDB installed** on your machine.

2. Start MongoDB server** (if not already running):

   ```bash
   mongod
````

3. Clone this repo and navigate to the project folder:**

   ```bash
   git clone https://github.com/salma-nour-eldeen6/MongoDB-Project.git
   cd MongoDB-Project
   ```

4. Install required Python packages:**

   ```bash
   pip install flask pymongo
   ```

5. Run the Flask app:**

   ```bash
   python app.py
   ```

6. Open your browser and go to:**

   ```
   http://localhost:5000
   ```

 
