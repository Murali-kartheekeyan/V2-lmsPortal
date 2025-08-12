import requests
import json
import time

# Base URL for the Flask application
base_url = 'http://127.0.0.1:5000'

# Login credentials
login_data = {
    'username': 'emp12',  # Replace with a valid employee username
    'password': 'password'  # Replace with the correct password
}

# Function to login and get a session cookie
def login():
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    response = session.post(f'{base_url}/login', headers=headers, json=login_data)
    if response.status_code == 200:
        print("Login successful")
        return session
    else:
        print(f"Login failed: {response.status_code}")
        if response.text:
            print(response.text[:200])  # Print first 200 chars of response
        return None

# Function to get the assessment page for a course
def get_assessment(session, course_name):
    response = session.get(f'{base_url}/employee/start_assessment/{course_name}')
    if response.status_code == 200:
        print(f"Got assessment for {course_name}")
        return True
    else:
        print(f"Failed to get assessment: {response.text}")
        return False

# Function to submit assessment answers
def submit_assessment(session, answers):
    headers = {'Content-Type': 'application/json'}
    response = session.post(
        f'{base_url}/employee/submit_assessment_answers',
        headers=headers,
        data=json.dumps({'answers': answers})
    )
    if response.status_code == 200:
        result = response.json()
        print(f"Assessment submission result: {result}")
        return result
    else:
        print(f"Failed to submit assessment: {response.text}")
        return None

# Function to check the assessment result page
def check_result(session, redirect_url):
    response = session.get(f'{base_url}{redirect_url}')
    if response.status_code == 200:
        print("Successfully accessed assessment result page")
        # Check if the page contains the expected content
        if "Congratulations" in response.text:
            print("Assessment passed message found")
        elif "Try Again" in response.text:
            print("Assessment failed message found")
        else:
            print("Could not determine assessment result from page content")
        return True
    else:
        print(f"Failed to access assessment result: {response.text}")
        return False

# Function to check course status after assessment
def check_course_status(session, course_name):
    response = session.get(f'{base_url}/employee/my_courses')
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            courses = data.get('courses', [])
            for course in courses:
                if course.get('course_name') == course_name:
                    print(f"Course status: {course.get('status')}, Progress: {course.get('progress')}%")
                    return course
            print(f"Course {course_name} not found in my courses")
        else:
            print(f"Failed to get courses: {data.get('message')}")
    else:
        print(f"Failed to check course status: {response.text}")
    return None

# Main test function
def test_assessment_flow():
    # Login
    session = login()
    if not session:
        return
    
    # Course to test
    course_name = "Introduction to testing"
    
    # Check initial course status
    print("\nChecking initial course status...")
    initial_status = check_course_status(session, course_name)
    
    # Get assessment
    print("\nGetting assessment...")
    if not get_assessment(session, course_name):
        return
    
    # Create answers that will pass (assuming 10 questions with correct answer index 0)
    # In a real test, you would need to parse the assessment page to get the actual questions
    answers = {}
    for i in range(10):  # Assuming 10 questions
        answers[str(i)] = "0"  # Assuming correct answer is always option 0
    
    # Submit assessment
    print("\nSubmitting assessment...")
    result = submit_assessment(session, answers)
    if not result or not result.get('success'):
        return
    
    # Check result page
    print("\nChecking assessment result page...")
    redirect_url = result.get('redirect_url')
    if not check_result(session, redirect_url):
        return
    
    # Wait a moment for database updates
    time.sleep(1)
    
    # Check final course status
    print("\nChecking final course status...")
    final_status = check_course_status(session, course_name)
    
    # Verify status changed
    if initial_status and final_status:
        if initial_status.get('status') != final_status.get('status'):
            print(f"Status changed from {initial_status.get('status')} to {final_status.get('status')}")
        else:
            print("Status did not change")
        
        if initial_status.get('progress') != final_status.get('progress'):
            print(f"Progress changed from {initial_status.get('progress')}% to {final_status.get('progress')}%")
        else:
            print("Progress did not change")

if __name__ == "__main__":
    test_assessment_flow()