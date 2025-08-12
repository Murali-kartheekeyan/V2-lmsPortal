import pymysql
from db import get_db_connection

def check_assessment_marks():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check the structure of the assessment_marks table
            cursor.execute("DESCRIBE assessment_marks")
            columns = cursor.fetchall()
            print("\nAssessment Marks Table Structure:")
            for col in columns:
                print(f"  {col['Field']} - {col['Type']} - {col.get('Key', '')}")
            
            # Check the content of the assessment_marks table
            cursor.execute("SELECT * FROM assessment_marks ORDER BY emp_id, course_name")
            marks = cursor.fetchall()
            print("\nAssessment Marks Records:")
            if not marks:
                print("  No records found in assessment_marks table")
            else:
                for mark in marks:
                    print(f"  Employee ID: {mark['emp_id']}, Course: {mark['course_name']}, Marks: {mark['marks_obtained']}")
            
            # Check the course_completed table
            cursor.execute("DESCRIBE course_completed")
            columns = cursor.fetchall()
            print("\nCourse Completed Table Structure:")
            for col in columns:
                print(f"  {col['Field']} - {col['Type']} - {col.get('Key', '')}")
            
            # Check the content of the course_completed table
            cursor.execute("SELECT * FROM course_completed ORDER BY emp_id, course_name")
            completed = cursor.fetchall()
            print("\nCourse Completed Records:")
            if not completed:
                print("  No records found in course_completed table")
            else:
                for course in completed:
                    print(f"  Employee ID: {course['emp_id']}, Course: {course['course_name']}")
            
            # Check the course_assigned table for courses with status 'Completed'
            cursor.execute("SELECT * FROM course_assigned WHERE status = 'Completed' ORDER BY emp_id, course_name")
            assigned = cursor.fetchall()
            print("\nCourse Assigned Records with 'Completed' status:")
            if not assigned:
                print("  No records found with 'Completed' status in course_assigned table")
            else:
                for course in assigned:
                    print(f"  Employee ID: {course['emp_id']}, Course: {course['course_name']}, Status: {course['status']}, Progress: {course['progress']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_assessment_marks()