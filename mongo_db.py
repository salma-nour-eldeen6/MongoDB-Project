from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import ObjectId

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["universityDB"]
        self.students = self.db["students"]
        self.courses = self.db["courses"]   
        self.departments = self.db["departments"]
        
 
        self.create_indexes()
    
 
    def initialize_data(self):
        
        # Insert students
        self.students.insert_many([
            {
                "name": "Salma",
                "age": 21,
                "gpa":3.8,
                "department": "General",
                "active": True,
                "grades": [85, 90, 88],
                "address": {
                    "city": "Giza",
                    "country": "Egypt"
                }
            },
            {
                "name": "Sama",
                "age": 22,
                "gpa": 3.2,
                "department": "is",
                "active": False,
                "grades": [75, 80, 82],
                "address": {
                    "city": "Cairo",
                    "country": "Egypt"
                }
            },
            {
                "name": "Omar",
                "age": 24,
                "gpa": 2.5,
                "department": "General",
                "active": False,
                "grades": [85, 80, 82],
                "address": {
                    "city": "Cairo",
                    "country": "Egypt"
                }
            }
        ])
        
        # Insert courses
        self.courses.insert_many([
            {
                "title": "Math101",
                "credits": 4,
                "department": "General",
                "enrolled_students": ["salma", "sama"],
                "Doctor":"Amany"
 
            },
            {
                "title": "MIS201",
                "credits": 3,
                "department": "is",
                "enrolled_students": ["salma", "sama"],
                "Doctor":"Ahmed Elsyed"
 
            },
            {
                "title": "IA101",
                "credits": 3,
                "department": "is",
                "enrolled_students": ["salma"],
                "Doctor":["Hanan","Wael"]
 
            }
        ])
        self.departments.insert_many([
            {
                "name": "General",
                "head": "Dr. Ahmed"
            },
            {
                "name": "is",
                "head": "Dr. Hanan"
            },
            {
                "name": "CS",
                "head": "Dr. Wael"
            },
                        {
                "name": "it",
                "head": "Dr. shamardan"
            },
            {
                "name": "ai",
                "head": "Dr. amr"
            }
        ])
        
    def insert_student(self, student_data):
        try:
            result = self.students.insert_one(student_data)
            return str(result.inserted_id)  
        except Exception as e:
            raise Exception(f"Database insertion error: {str(e)}")
        
    
    def get_department(self, department_name):
            department = self.departments.find_one({"name": department_name})
            return department
        
    def update_student(self, student_id, update_data):
   
        try:
           
            if not ObjectId.is_valid(student_id):
                raise ValueError("Invalid student ID format")
            
            if not update_data or not isinstance(update_data, dict):
                raise ValueError("No valid update data provided")
            
            gpa_increment = update_data.pop('gpa_increment', None)
            
            update_ops = {}
            
            if update_data:
                update_ops['$set'] = update_data
                
            if gpa_increment is not None:
                
                update_ops['$inc'] = {'gpa': gpa_increment}
            
            if not update_ops:
                raise ValueError("No valid update operations specified")
         
            result = self.students.update_one(
                {"_id": ObjectId(student_id)},
                update_ops
            )
            
            if result.modified_count == 0:
                raise Exception("No documents were updated - student may not exist")
                
            return result.modified_count
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Database update failed: {str(e)}")
 
   
    def delete_student(self, student_id):
 
        try:
            if not ObjectId.is_valid(student_id):
                raise ValueError("Invalid student ID format")
            
            result = self.students.delete_one({"_id": ObjectId(student_id)})
            
            if result.deleted_count == 0:
                raise Exception("No student found with this ID")
                
            return True
            
        except Exception as e:
            raise Exception(f"Deletion failed: {str(e)}")

  
    def add_course(self, course_data):
       
        try:
            required_fields = ['title', 'credits', 'department']
            for field in required_fields:
                if field not in course_data:
                    raise ValueError(f"Missing required field: {field}")
            
            if not isinstance(course_data['credits'], int) or course_data['credits'] <= 0:
                raise ValueError("Credits must be a positive integer")
            
            
            if 'enrolled_students' in course_data:
                if isinstance(course_data['enrolled_students'], str):
                    course_data['enrolled_students'] = [s.strip() for s in course_data['enrolled_students'].split(',')]
            
         
            result = self.courses.insert_one(course_data)
            return str(result.inserted_id)
            
        except Exception as e:
            raise Exception(f"Course insertion failed: {str(e)}")
        
        
        
 

    def update_course(self, course_id, update_data):
         
        try:
           
            if not ObjectId.is_valid(course_id):
                raise ValueError("Invalid course ID format")

             
            if not update_data or not isinstance(update_data, dict):
                raise ValueError("No valid update data provided")
 
            if 'enrolled_students' in update_data:
                if isinstance(update_data['enrolled_students'], str):
                    update_data['enrolled_students'] = [
                        s.strip() for s in update_data['enrolled_students'].split(',')
                    ]

            if 'Doctor' in update_data:
                if isinstance(update_data['Doctor'], str) and ',' in update_data['Doctor']:
                    update_data['Doctor'] = [d.strip() for d in update_data['Doctor'].split(',')]
 
            if 'credits' in update_data and (not isinstance(update_data['credits'], int) or update_data['credits'] <= 0):
                raise ValueError("Credits must be a positive integer")

            result = self.courses.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": update_data}
            )

            if result.modified_count == 0:
                raise Exception("No courses were updated - course may not exist")

            return result.modified_count

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Course update failed: {str(e)}")
        
        
        
    def delete_course(self, course_id):
   
        try:
            
            if not ObjectId.is_valid(course_id):
                raise ValueError("Invalid course ID format")
            
           
            result = self.courses.delete_one({"_id": ObjectId(course_id)})
            
            
            if result.deleted_count == 0:
                raise Exception("Course not found")
            
            return True
            
        except Exception as e:
         
            raise Exception(f"Deletion error: {str(e)}")

 
  
    def add_student_to_course(self, course_title, student_name):
    
        try:
            
            if not course_title or not isinstance(course_title, str):
                raise ValueError("Invalid course title")
            
            if not student_name or not isinstance(student_name, str):
                raise ValueError("Invalid student name")

      
            result = self.courses.update_one(
                {"title": course_title},
                {"$push": {"enrolled_students": student_name}},
                upsert=False   
            )

            if result.modified_count == 0:
                raise Exception("Course not found or student already enrolled")
                
            return True

        except Exception as e:
            
            raise Exception(f"Enrollment error: {str(e)}")
    
    
    
         
    def find_students_by_department_and_course(self, department, course_title):
        try:
            print(f"Searching for course: {course_title} in department: {department}")   

            course = self.courses.find_one({
                "$and": [
                    {"department": department},
                    {"title": course_title}
                ]
            })
            if not course:
                print(f"No course found for {course_title} in department {department}")  
                return []

            enrolled_names = course.get("enrolled_students", [])
            print(f"Enrolled students: {enrolled_names}")  

            students = list(self.students.find({
                "$and": [
                    {"name": {"$in": enrolled_names}},
                    {"department": department}
                ]
            }))
            print(f"Found students: {students}")  

            return students
        except Exception as e:
            print(f"Query error: {str(e)}")  
            raise Exception(f"Query error: {str(e)}")

    from bson import ObjectId

    def find_inactive_or_low_gpa_students(self):
        try:

            students = list(self.students.find({
                "$or": [
                    {"active": False},       
                    {"gpa": {"$lt": 2}}        
                ]
            }))
             
            for student in students:
                student["_id"] = str(student["_id"])

            print(f"Found {len(students)} students matching the criteria.")
            return students

        except Exception as e:
            print(f"Error during query: {str(e)}")
            raise Exception(f"Query error: {str(e)}" )


 
    def calculate_and_store_total_grades(self):
        try:
            students = self.students.find({"grades": {"$exists": True, "$type": "array"}})
            updated_count = 0

            for student in students:
                grades = student.get("grades", [])
                if grades:
                    total = sum(grades)
                    
                    result = self.students.update_one(
                        {"_id": student["_id"]},
                        {"$set": {"totalGrade": total}}  
                    )
                    if result.modified_count > 0:
                        updated_count += 1

            return {"updated": updated_count}
        except Exception as e:
            print(f"Error during grade calculation: {str(e)}")
            raise Exception(f"Grade calculation error: {str(e)}")

   
    def create_indexes(self):
        # Single-field index
        self.students.create_index("name")
        
        # Compound index
        self.students.create_index([("age", 1), ("active", 1)])
        
        # Unique index
        self.courses.create_index("title", unique=True)


    def get_all_students_grouped_by_department(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$department",
                    "students": {
                        "$push": {
                            "name": "$name",
                            "age": "$age",
                            "gpa": "$gpa",
                            "grades": "$grades",
                            "active": "$active"
                        }
                    }
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
        result = list(self.students.aggregate(pipeline))
        return result
    
    def get_course_student_counts(self):
       
        courses = self.courses.find({})  

        result = []

        
        for course in courses:
            count = len(course['enrolled_students'])   
            result.append({
                "course": course['title'],
                "student_count": count
            })

        return result

 
if __name__ == "__main__":
    db = MongoDB()
    db.initialize_data()
      