from flask import Blueprint, request, jsonify, session
from db import get_db_connection
from ai_agents import assign_domain_with_ai  # <-- IMPORT the new AI function

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Clear any existing session data to ensure a clean login.
    session.clear() 
    
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"success": False, "message": "Missing credentials"}, 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Query the credentials table to find the user
            cursor.execute(
                "SELECT emp_id, password, is_admin FROM credentials WHERE username = %s LIMIT 1",
                (username,)
            )
            user = cursor.fetchone()

            if user and user['password'] == password:
                # Set session variables for both admin and employee
                session['emp_code'] = user['emp_id']
                
                if user['is_admin']:
                    session['role'] = 'admin'
                else:
                    session['role'] = 'employee'
                    
                    # --- NEW DOMAIN ASSIGNMENT LOGIC ---
                    # Check if the employee has a domain assigned
                    cursor.execute("SELECT domain FROM employee WHERE id = %s", (user['emp_id'],))
                    employee_data = cursor.fetchone()
                    
                    assigned_domain = employee_data.get('domain') if employee_data else None

                    # If no domain is set, call the AI agent to assign one
                    if not assigned_domain:
                        print(f"No domain for employee {user['emp_id']}. Calling AI agent.")
                        assigned_domain = assign_domain_with_ai(user['emp_id'])
                        
                    # Store the domain in the session for easy access
                    session['domain'] = assigned_domain

                return {"success": True}, 200
            else:
                # No match found or password incorrect
                return {"success": False, "message": "Invalid credentials"}, 401

    except Exception as e:
        print(f"An error occurred during login: {e}")
        return {"success": False, "message": "An internal error occurred."}, 500
    finally:
        conn.close()
