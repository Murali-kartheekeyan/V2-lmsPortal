from db import get_db_connection

def check_credentials():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Query the credentials table to find employee users
            cursor.execute(
                "SELECT c.emp_id, c.username, c.password, c.is_admin, e.NAME FROM credentials c JOIN employee e ON c.emp_id = e.id WHERE c.is_admin = 0"
            )
            employees = cursor.fetchall()
            
            print("\nEmployee Credentials:")
            for emp in employees:
                print(f"  Employee ID: {emp['emp_id']}")
                print(f"  Name: {emp['NAME']}")
                print(f"  Username: {emp['username']}")
                print(f"  Password: {emp['password']}")
                print(f"  Is Admin: {emp['is_admin']}")
                print("---")
            
            # Check course assignments for employee with ID 12
            cursor.execute(
                "SELECT * FROM course_assigned WHERE emp_id = 12"
            )
            courses = cursor.fetchall()
            
            print("\nCourses assigned to Employee ID 12:")
            for course in courses:
                print(f"  Course: {course['course_name']}")
                print(f"  Status: {course['status']}")
                print(f"  Progress: {course['progress']}%")
                print("---")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_credentials()