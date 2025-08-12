from db import get_db_connection

def check_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all courses from the database
    cursor.execute('SELECT CourseName, CourseFile FROM course')
    courses = cursor.fetchall()
    
    print('Course Names and Files:')
    for course in courses:
        print(f'- {course["CourseName"]} -> {course["CourseFile"]}')
    
    # Check if course files exist
    import os
    print('\nChecking if course files exist:')
    for course in courses:
        file_path = os.path.join('static', 'courses', course['CourseFile'])
        exists = os.path.exists(file_path)
        print(f'- {course["CourseFile"]}: {"Exists" if exists else "MISSING"}')
    
    conn.close()

if __name__ == '__main__':
    check_courses()