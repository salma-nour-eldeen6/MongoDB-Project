# University Management System using Flask & MongoDB

This is a web application built using **Python (Flask)** and **MongoDB** that allows you to manage university data including **students, courses, and departments**.

It supports both a web interface and RESTful APIs for interacting with the data.

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
/MongoDB-Project
│
├── app.py # Main Flask app
├── mongo_db.py # MongoDB interaction class
├── templates/ # HTML templates (not detailed here)
├── static/ # CSS & JS files
├── requirements.txt # Required packages (you can create this)
└── README.md # Project description


 

