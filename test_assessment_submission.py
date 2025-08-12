import pymysql
from db import get_db_connection

def test_assessment_submission():
    # Test parameters
    emp_id = 12  # Replace with a valid employee ID
    course_name = "Introduction to testing"  # Using a course that is assigned to the employee
    score = 8  # Test with a score of 8 (should pass if there are 10 questions)
    total_questions = 10
    percentage_score = (score / total_questions) * 100
    
    print(f"Testing assessment submission for Employee ID: {emp_id}, Course: {course_name}")
    print(f"Score: {score}/{total_questions} ({percentage_score}%)")
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # First, check if the course exists and is assigned to the employee
            cursor.execute("SELECT * FROM course_assigned WHERE emp_id = %s AND course_name = %s", 
                          (emp_id, course_name))
            assignment = cursor.fetchone()
            
            if not assignment:
                print(f"Error: Course '{course_name}' is not assigned to employee {emp_id}")
                return
            
            print(f"\nCurrent assignment status: {assignment['status']}, Progress: {assignment['progress']}%")
            
            # Insert the assessment mark
            cursor.execute("INSERT INTO assessment_marks (emp_id, course_name, marks_obtained) VALUES (%s, %s, %s)", 
                          (emp_id, course_name, score))
            
            # Update the course status based on percentage score
            if percentage_score >= 80:  # 80% threshold
                cursor.execute("UPDATE course_assigned SET status = 'Completed', progress = 100 WHERE emp_id = %s AND course_name = %s", 
                              (emp_id, course_name))
                
                # Check if already in completed courses before inserting
                cursor.execute("SELECT COUNT(*) as count FROM course_completed WHERE emp_id = %s AND course_name = %s", 
                              (emp_id, course_name))
                existing = cursor.fetchone()
                
                if existing['count'] == 0:
                    cursor.execute("INSERT INTO course_completed (emp_id, course_name) VALUES (%s, %s)", 
                                  (emp_id, course_name))
                    print("Added to course_completed table")
                else:
                    print("Already exists in course_completed table")
            else:
                cursor.execute("UPDATE course_assigned SET status = 'Not Started', progress = 0 WHERE emp_id = %s AND course_name = %s", 
                              (emp_id, course_name))
            
            conn.commit()
            
            # Verify the changes
            cursor.execute("SELECT * FROM course_assigned WHERE emp_id = %s AND course_name = %s", 
                          (emp_id, course_name))
            updated_assignment = cursor.fetchone()
            
            print(f"\nUpdated assignment status: {updated_assignment['status']}, Progress: {updated_assignment['progress']}%")
            
            # Check assessment marks
            cursor.execute("SELECT * FROM assessment_marks WHERE emp_id = %s AND course_name = %s ORDER BY attempt_date DESC", 
                          (emp_id, course_name))
            marks = cursor.fetchall()
            
            print("\nAssessment marks:")
            for mark in marks:
                print(f"  Marks: {mark['marks_obtained']}, Date: {mark['attempt_date']}")
            
            # Check course_completed
            cursor.execute("SELECT * FROM course_completed WHERE emp_id = %s AND course_name = %s", 
                          (emp_id, course_name))
            completed = cursor.fetchone()
            
            if completed:
                print(f"\nCourse completion record found. Date: {completed['completion_date']}")
            else:
                print("\nNo course completion record found.")
                
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_assessment_submission()