from flask import Flask, json, jsonify, render_template, request, redirect, url_for, flash
from mongo_db import MongoDB
from bson.objectid import ObjectId
from flask import jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
db = MongoDB()

 
with app.app_context():
    if db.students.count_documents({}) == 0:
        db.initialize_data()
        db.create_indexes()
        db.calculate_total_grades()

@app.route('/')
def index():
    students = list(db.students.find())
    courses = list(db.courses.find())
    return render_template('index.html', students=students, courses=courses)

 
 
 
def check_department_exists():
    department = request.form.get('department')
    if not department:
        flash('Department is required', 'danger')
        return False

 
    existing_department = db.get_department(department)
    if not existing_department:
        flash('Department does not exist', 'danger')
        return False

    return True


@app.route('/add_student', methods=['POST'])
def add_student():
    try:
       
        if not check_department_exists():
            return redirect(url_for('index'))

        student_data = {
            "name": request.form['name'],
            "age": int(request.form['age']),
            "gpa": float(request.form['gpa']),
            "department": request.form['department'], 
            "active": request.form.get('active') == 'on',
            "grades": [int(g) for g in request.form['grades'].split(',')],
            "address": {
                "city": request.form['city'],
                "country": request.form['country']
            }
        }

        db.insert_student(student_data)
        db.calculate_and_store_total_grades()   
        flash(f'Student added successfully', 'success')
        
    except ValueError as e:
        flash(f'Invalid data format: {str(e)}', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('index'))



from bson import ObjectId  

@app.route('/update_student/<id>', methods=['POST'])
def update_student(id):
    try:
        update_data = {
            "$set": {
                "name": request.form['name'],
                "age": int(request.form['age']),
                "gpa": float(request.form['gpa']),
                "department": request.form['department'],
                "active": request.form.get('active') == 'True',
                "address.city": request.form['city'],
                "address.country": request.form['country']
            }
        }

        db.students.update_one({"_id": ObjectId(id)}, update_data)
        db.calculate_and_store_total_grades()   

        flash('Student updated successfully', 'success')
    except Exception as e:
        flash(f'Update failed: {str(e)}', 'danger')
        app.logger.error(f"Update failed: {str(e)}")

    return redirect(url_for('index'))

 
@app.route('/delete_student/<id>', methods=['POST'])     ###
def delete_student(id):
    try:
        db.delete_student(id)
        flash('Student deleted successfully', 'success')
    except ValueError as e:
        flash(f'Validation error: {str(e)}', 'warning')
    except Exception as e:
        flash(f'Deletion failed: {str(e)}', 'danger')
        app.logger.error(f"Delete failed for student {id}: {str(e)}")
    return redirect(url_for('index'))

 
@app.route('/add_course', methods=['POST'])
def add_course():
    try:
        department = request.form['department']
        
        
        existing_department = db.departments.find_one({"name": department})
        if not existing_department:
            flash(f'Department "{department}" does not exist!', 'warning')
            return redirect(url_for('index'))

        course_data = {
            "title": request.form['title'],
            "credits": int(request.form['credits']),
            "department": department,
            "enrolled_students": request.form['enrolled_students'],
            "Doctor": request.form['doctor']
        }
        
        db.add_course(course_data)
        flash('Course added successfully!', 'success')

    except ValueError as e:
        flash(f'Invalid data: {str(e)}', 'warning')
    except Exception as e:
        flash(f'Course addition failed: {str(e)}', 'danger')

    return redirect(url_for('index'))




@app.route('/update_course/<id>', methods=['POST'])
def update_course(id):
    try:
        department_name = request.form['department']
        department = db.get_department(department_name)

        if not department:
            flash(f'Department "{department_name}" not found in the database.', 'warning')
            return redirect(url_for('index'))

        update_data = {
            "title": request.form['title'],
            "credits": int(request.form['credits']),
            "department": department_name,
            "enrolled_students": request.form['enrolled_students'],
            "Doctor": request.form['doctor']
        }

        db.update_course(id, update_data)
        flash(f'Course updated successfully', 'success')

    except ValueError as e:
        flash(f'Validation error: {str(e)}', 'warning')
    except Exception as e:
        flash(f'Update failed: {str(e)}', 'danger')
        app.logger.error(f"Course update failed for ID {id}: {str(e)}")

    return redirect(url_for('index'))


@app.route('/delete_course/<id>', methods=['POST'])   
def delete_course(id):
    try:
        db.delete_course(id)
        flash('course deleted successfully', 'success')
    except ValueError as e:
        flash(f'Validation error: {str(e)}', 'warning')
    except Exception as e:
        flash(f'Deletion failed: {str(e)}', 'danger')
        app.logger.error(f"Delete failed for course {id}: {str(e)}")
    return redirect(url_for('index'))





@app.route('/enroll_student', methods=['POST'])            ###
def enroll_student():
    try:
        course_title = request.form['course_title']
        student_name = request.form['student_name']
        
       
        db.add_student_to_course(course_title, student_name)
        
        flash('Student enrolled successfully', 'success')
    except ValueError as e:
        flash(f'Validation error: {str(e)}', 'warning')
    except Exception as e:
        flash(f'Enrollment failed: {str(e)}', 'danger')
    return redirect(url_for('index'))
 
    
@app.route('/api/departments')
def get_departments():
    try:
        departments = db.departments.find()   
        department_list = [{"name": dept["name"]} for dept in departments]
        return jsonify(department_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/courses')
def get_courses():
    department = request.args.get('department')
    if not department:
        return jsonify({"error": "Department is required"}), 400

    try:
        courses = db.courses.find({"department": department})  
        course_list = [{"title": course["title"]} for course in courses]
        return jsonify(course_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

 
@app.route('/students/by-department-and-course')
def students_by_department_and_course():
    department = request.args.get('department')
    course = request.args.get('course')
    
    students = db.find_students_by_department_and_course(department, course)
    
    student_list = []
    for student in students:
        student_data = {
            "name": student.get("name", "N/A"),
            "department": student.get("department", "N/A"),
            "gpa": student.get("gpa", 0.0),
            "active": student.get("active", False)
        }
        student_list.append(student_data)
    
    return jsonify(student_list)  


@app.route("/at_risk_students")
def at_risk_students():
    try:
        students = db.find_inactive_or_low_gpa_students()
        return jsonify(students)  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

  
@app.route('/update_total_grades', methods=['POST'])
def update_total_grades():
    try:
      
        updated_count = db.calculate_and_store_total_grades()
        flash(f"Total grades updated for {updated_count['updated']} students.", 'success')
        return redirect(url_for('index'))  
    except Exception as e:
        return str(e), 500

    
    
@app.route('/students/by-department', methods=['GET'])
def get_students_by_department():
    try:
         
        data = db.get_all_students_grouped_by_department()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
 

@app.route('/courses')
def show_courses():
    courses = db.students.distinct("courses")
    return render_template("courses.html", courses=courses)


@app.route('/course_student_counts', methods=['GET'])
def course_student_counts():
    try:
        result = db.get_course_student_counts()   
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
    
    
    