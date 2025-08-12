from db import get_db_connection

def check_enrollments():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, check the table structure
    print('Checking course_assigned table structure:')
    cursor.execute("DESCRIBE course_assigned")
    columns = cursor.fetchall()
    
    for column in columns:
        print(f"- {column['Field']}: {column['Type']}")
    
    # Get all course enrollments with the correct columns
    print('\nFetching enrollments:')
    try:
        cursor.execute('SELECT emp_id, course_name, status, progress, assigned_date FROM course_assigned')
        enrollments = cursor.fetchall()
        
        print(f'Total enrollments found: {len(enrollments)}')
        
        if enrollments:
            print('\nEnrollment details:')
            for enrollment in enrollments:
                assigned = enrollment['assigned_date'].strftime('%Y-%m-%d %H:%M:%S') if enrollment['assigned_date'] else 'None'
                print(f"Employee: {enrollment['emp_id']}")
                print(f"  Course: {enrollment['course_name']}")
                print(f"  Status: {enrollment['status']}")
                print(f"  Progress: {enrollment['progress']}%")
                print(f"  Assigned: {assigned}")
                print("---")
        
        # Check for any issues with enrollments
        print('\nChecking for potential issues:')
        
        # Check for enrollments with invalid course names
        cursor.execute("""
            SELECT ca.emp_id, ca.course_name 
            FROM course_assigned ca 
            LEFT JOIN course c ON ca.course_name = c.CourseName 
            WHERE c.CourseName IS NULL
        """)
        invalid_courses = cursor.fetchall()
        
        if invalid_courses:
            print('\nEnrollments with invalid course names:')
            for invalid in invalid_courses:
                print(f"- Employee {invalid['emp_id']} enrolled in non-existent course: '{invalid['course_name']}'")
        else:
            print('No enrollments with invalid course names found.')
            
    except Exception as e:
        print(f"Error fetching enrollments: {e}")
    
    conn.close()

if __name__ == '__main__':
    check_enrollments()