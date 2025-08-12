# F:\vscode\New folder\Samsaram athu Minsaram\admin_routes.py
from flask import Blueprint, request, jsonify, session, render_template, Response, redirect, url_for, send_file
from db import get_db_connection
# UPDATED: Import the correct remodeled agent for admin reports
from ai_agents import hr_agent_process_file, profile_agent
import csv
from io import StringIO
import os
import io
import pandas as pd
from werkzeug.utils import secure_filename
import random # NEW: Import for generating random metrics
import re

admin_bp = Blueprint('admin', __name__)

# ------------- PAGE ROUTES -------------

# UPDATED: This route now calls the new, correct profile_agent
@admin_bp.route('/admin/ai_report/<emp_code>')
def ai_report_page(emp_code):
    if session.get('role') != 'admin':
        return redirect('/')
    
    employee_id = int(emp_code)
    # Call the remodeled profile_agent to get the full analysis
    analysis_data = profile_agent(employee_id)

    if analysis_data.get('error'):
        return analysis_data['error'], 404

    # Fetch employee name separately for the page title
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT NAME FROM employee WHERE id = %s", (employee_id,))
            employee = cursor.fetchone()
            if not employee:
                return "Employee not found", 404
    finally:
        conn.close()

    return render_template(
        'admin_ai_report.html',
        employee=employee,
        analysis=analysis_data  # Pass the entire analysis dictionary
    )

# --- Other page routes ---

@admin_bp.route('/admin/hr_agent')
def hr_agent_page():
    if session.get('role') == 'admin':
        return render_template('admin_hr_agent.html')
    return redirect('/')

@admin_bp.route('/admin/courses_page')
def courses_page():
    if session.get('role') == 'admin':
        return render_template('admin_courses.html')
    return redirect('/')

@admin_bp.route('/admin/agent_metrics_page')
def agent_metrics_page():
    if session.get('role') == 'admin':
        return render_template('admin_agent_metrics.html')
    return redirect('/')

@admin_bp.route('/admin/generate_reports_page')
def generate_reports_page():
    if session.get('role') == 'admin':
        return render_template('admin_generate_reports.html')
    return redirect('/')

@admin_bp.route('/admin/add_employee_page')
def add_employee_page():
    if session.get('role') == 'admin':
        return render_template('admin_add_employee.html')
    return redirect('/')

# ...existing code...

@admin_bp.route('/admin/delete_employee_page')
def delete_employee_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('admin_delete_employee.html', agent_type='admin')

# ...existing code... 

@admin_bp.route('/admin/show_employees')
def show_employees_page():
    if session.get('role') == 'admin':
        return render_template('admin_show_employees.html')
    return redirect('/')

@admin_bp.route('/admin/search_filters')
def search_filters_page():
    if session.get('role') == 'admin':
        return render_template('admin_search_filters.html')
    return redirect('/')

# Removed AI course assignment page - AI now suggests courses directly to employees

@admin_bp.route('/admin/duplicate_cleanup')
def duplicate_cleanup_page():
    if session.get('role') == 'admin':
        return render_template('admin_duplicate_cleanup.html')
    return redirect('/')


# ------------- API ROUTES -------------

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/admin/hr_agent/upload_employees', methods=['POST'])
def upload_employees_by_agent():
    if session.get('role') != 'admin': return jsonify({"success": False, "message": "Unauthorized"}), 401
    if 'file' not in request.files: return jsonify({"success": False, "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"success": False, "message": "Invalid or no selected file"}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.csv': df = pd.read_csv(filepath)
        elif ext == '.xlsx': df = pd.read_excel(filepath)
        elif ext == '.json': df = pd.read_json(filepath)
        else: raise ValueError("Unsupported file format")
    except Exception as e:
        os.remove(filepath)
        return jsonify({"success": False, "message": f"Error reading file: {e}"}), 500
    employees_added, error = hr_agent_process_file(df)
    os.remove(filepath)
    if error: return jsonify({"success": False, "message": f"Error processing data: {error}"}), 500
    return jsonify({"success": True, "message": f"AI HR Agent successfully onboarded {employees_added} new employees."}), 200

@admin_bp.route('/admin/list_employees', methods=['GET'])
def list_employees():
    if session.get('role') != 'admin': return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    # Get filter parameters
    emp_id = request.args.get('emp_id')
    dept = request.args.get('dept')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Build query based on filters
            query = "SELECT id, NAME, domain FROM employee"
            params = []
            where_clauses = []
            
            if emp_id:
                where_clauses.append("id LIKE %s")
                params.append(f"%{emp_id}%")
            
            if dept:
                where_clauses.append("domain LIKE %s")
                params.append(f"%{dept}%")
            
            # Add WHERE clause if any filters are applied
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(query, tuple(params))
            employees = cursor.fetchall()
        return jsonify({"success": True, "employees": employees})
    finally: conn.close()

def _slugify_username_from_name(name: str) -> str:
    """Create a simple slug base from a name (letters and numbers only, lowercase)."""
    base = re.sub(r"[^a-zA-Z0-9]", "", (name or "user")).lower()
    return base or "user"

@admin_bp.route('/admin/add_employee', methods=['POST'])
def add_employee():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.json or {}
    name = data.get('Name')
    password = data.get('Password')

    if not name or not password:
        return jsonify({"success": False, "error": "Name and Password are required"}), 400

    # Gather proficiency fields with safe defaults
    fields = ['HTML', 'CSS', 'JAVASCRIPT', 'PYTHON', 'C', 'CPP', 'JAVA', 'SQL_TESTING', 'TOOLS_COURSE']
    prof = {f: int(data.get(f, 0) or 0) for f in fields}

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Insert into employee
            cursor.execute(
                """
                INSERT INTO employee (NAME, HTML, CSS, JAVASCRIPT, PYTHON, C, CPP, JAVA, SQL_TESTING, TOOLS_COURSE, domain)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
                """,
                (
                    name,
                    prof['HTML'], prof['CSS'], prof['JAVASCRIPT'], prof['PYTHON'],
                    prof['C'], prof['CPP'], prof['JAVA'], prof['SQL_TESTING'], prof['TOOLS_COURSE']
                )
            )
            new_emp_id = cursor.lastrowid

            # Create a unique username based on name + id
            base = _slugify_username_from_name(name)
            username = f"{base}{new_emp_id}"

            # Insert credentials (non-admin by default)
            cursor.execute(
                """
                INSERT INTO credentials (emp_id, username, password, email, is_admin)
                VALUES (%s, %s, %s, NULL, 0)
                """,
                (new_emp_id, username, password)
            )

            conn.commit()

        return jsonify({
            "success": True,
            "message": "Employee added successfully",
            "employee": {"id": new_emp_id, "name": name, "username": username}
        })
    except Exception as e:
        if conn and conn.open:
            conn.rollback()
        return jsonify({"success": False, "error": f"Failed to add employee: {str(e)}"}), 500
    finally:
        if conn and conn.open:
            conn.close()

@admin_bp.route('/admin/delete_employee', methods=['POST'])
def delete_employee():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.json or {}
    emp_id = data.get('emp_id') or data.get('id') or data.get('emp_code')

    try:
        emp_id = int(emp_id)
    except Exception:
        return jsonify({"success": False, "error": "A valid emp_id is required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Ensure employee exists
            cursor.execute("SELECT id, NAME FROM employee WHERE id = %s", (emp_id,))
            employee = cursor.fetchone()
            if not employee:
                return jsonify({"success": False, "error": "Employee not found"}), 404

            # Prevent deleting admin accounts
            cursor.execute("SELECT is_admin FROM credentials WHERE emp_id = %s", (emp_id,))
            cred = cursor.fetchone()
            if cred and cred.get('is_admin'):
                return jsonify({"success": False, "error": "Cannot delete an admin account"}), 400

            # Delete from employee (cascades will clean dependent rows where configured)
            cursor.execute("DELETE FROM employee WHERE id = %s", (emp_id,))
            conn.commit()

        return jsonify({"success": True, "message": f"Employee {employee['NAME']} (ID {emp_id}) deleted"})
    except Exception as e:
        if conn and conn.open:
            conn.rollback()
        return jsonify({"success": False, "error": f"Failed to delete employee: {str(e)}"}), 500
    finally:
        if conn and conn.open:
            conn.close()

@admin_bp.route('/admin/course_analytics', methods=['GET'])
def get_course_analytics():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT 
                    c.CourseName,
                    c.Domain,
                    COUNT(ca.emp_id) AS total_enrolled,
                    SUM(CASE WHEN ca.status = 'Completed' THEN 1 ELSE 0 END) AS total_completed,
                    SUM(CASE WHEN ca.status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress
                FROM 
                    course c
                LEFT JOIN 
                    course_assigned ca ON TRIM(LOWER(c.CourseName)) = TRIM(LOWER(ca.course_name))
                GROUP BY 
                    c.CourseName, c.Domain
                ORDER BY
                    total_enrolled DESC, c.CourseName;
            """
            cursor.execute(sql)
            courses = cursor.fetchall()

            for course in courses:
                if course['total_enrolled'] > 0:
                    course['completion_rate'] = round((course['total_completed'] / course['total_enrolled']) * 100)
                else:
                    course['completion_rate'] = 0
            
        return jsonify({"success": True, "courses": courses})
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# NEW: API endpoint for live agent metrics
@admin_bp.route('/admin/agent_metrics', methods=['GET'])
def get_agent_metrics():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    # Simulate live data for demonstration
    metrics = {
        "Profile_Agent": {
            "queue": random.randint(0, 5),
            "latency_ms": random.randint(250, 400),
            "error_rate": f"{random.uniform(0.1, 1.5):.2f}%"
        },
        "Assessment_Agent": {
            "queue": random.randint(0, 10),
            "latency_ms": random.randint(150, 250),
            "error_rate": f"{random.uniform(0.0, 0.5):.2f}%"
        },
        "Recommender_Agent": {
            "queue": random.randint(0, 3),
            "latency_ms": random.randint(500, 800),
            "error_rate": f"{random.uniform(0.5, 2.0):.2f}%"
        },
        "Tracker_Agent": {
            "queue": random.randint(0, 15),
            "latency_ms": random.randint(100, 200),
            "error_rate": f"{random.uniform(0.0, 0.2):.2f}%"
        }
    }
    return jsonify({"success": True, "metrics": metrics})

# NEW: Dashboard stats endpoint
@admin_bp.route('/admin/dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get total employees
            cursor.execute("SELECT COUNT(*) as total FROM employee")
            total_employees = cursor.fetchone()['total']
            
            # Get total courses
            cursor.execute("SELECT COUNT(*) as total FROM course")
            total_courses = cursor.fetchone()['total']
            
            # Get average completion rate
            cursor.execute("""
                SELECT 
                    AVG(CASE WHEN status = 'Completed' THEN 100 ELSE 0 END) as avg_completion
                FROM course_assigned
            """)
            avg_completion_result = cursor.fetchone()
            avg_completion = round(avg_completion_result['avg_completion'] or 0)
            
            # Get employees by department for chart data
            cursor.execute("""
                SELECT domain, COUNT(*) as count 
                FROM employee 
                GROUP BY domain
            """)
            dept_data = cursor.fetchall()
            
            # Format data for chart
            chart_labels = [row['domain'] for row in dept_data]
            chart_data = [row['count'] for row in dept_data]
            
            stats = {
                "total_employees": total_employees,
                "total_courses": total_courses,
                "avg_completion": avg_completion,
                "overdue_tasks": 0,  # Placeholder for now
                "learning_progress_chart": {
                    "labels": chart_labels,
                    "data": chart_data
                }
            }
            
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# NEW: Assessment report endpoint
@admin_bp.route('/admin/assessment_report', methods=['GET'])
def get_assessment_report():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    e.id as emp_id,
                    e.NAME,
                    cc.course_name,
                    am.marks_obtained
                FROM employee e
                JOIN course_completed cc ON e.id = cc.emp_id
                JOIN (
                    SELECT emp_id, course_name, MAX(marks_obtained) as marks_obtained
                    FROM assessment_marks
                    GROUP BY emp_id, course_name
                ) am ON e.id = am.emp_id AND cc.course_name = am.course_name
                ORDER BY e.NAME, cc.course_name
            """)
            report = cursor.fetchall()
            
        return jsonify({"success": True, "report": report})
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# NEW: Get domain statistics
@admin_bp.route('/admin/get_domain_stats', methods=['GET'])
def get_domain_stats():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get domain statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_employees,
                    COUNT(domain) as with_domain,
                    COUNT(*) - COUNT(domain) as without_domain,
                    domain,
                    COUNT(*) as domain_count
                FROM employee 
                GROUP BY domain
                ORDER BY domain_count DESC
            """)
            domain_stats = cursor.fetchall()
            
            # Calculate totals
            total_employees = sum(stat['domain_count'] for stat in domain_stats)
            with_domain = sum(stat['domain_count'] for stat in domain_stats if stat['domain'])
            without_domain = sum(stat['domain_count'] for stat in domain_stats if not stat['domain'])
            
        return jsonify({
            "success": True,
            "stats": {
                "total_employees": total_employees,
                "with_domain": with_domain,
                "without_domain": without_domain,
                "domain_breakdown": domain_stats
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# Removed bulk employee assignment - AI now suggests courses directly to employees

# NEW: Assign domains to employees who don't have them
@admin_bp.route('/admin/assign_missing_domains', methods=['POST'])
def assign_missing_domains():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json or {}
    specific_employee_ids = data.get('employee_ids', [])

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if specific_employee_ids:
                # Assign domains to specific employees
                cursor.execute("SELECT id, NAME FROM employee WHERE id IN %s AND domain IS NULL", (tuple(specific_employee_ids),))
                employees_to_process = cursor.fetchall()
            else:
                # Get all employees without domains
                cursor.execute("SELECT id, NAME FROM employee WHERE domain IS NULL")
                employees_to_process = cursor.fetchall()

            if not employees_to_process:
                return jsonify({"success": True, "message": "All selected employees already have domains assigned"})

            results = []
            for employee in employees_to_process:
                try:
                    from ai_agents import assign_domain_with_ai
                    assigned_domain = assign_domain_with_ai(employee['id'])
                    if assigned_domain:
                        results.append({
                            "emp_id": employee['id'],
                            "name": employee['NAME'],
                            "success": True,
                            "domain": assigned_domain,
                            "message": f"Assigned domain '{assigned_domain}' to {employee['NAME']}"
                        })
                    else:
                        results.append({
                            "emp_id": employee['id'],
                            "name": employee['NAME'],
                            "success": False,
                            "message": f"Failed to assign domain to {employee['NAME']}"
                        })
                except Exception as e:
                    results.append({
                        "emp_id": employee['id'],
                        "name": employee['NAME'],
                        "success": False,
                        "message": f"Error assigning domain to {employee['NAME']}: {str(e)}"
                    })
            # Count successful assignments
            successful = len([r for r in results if r['success']])
            failed = len(results) - successful
            return jsonify({
                "success": True,
                "message": f"Domain assignment completed. {successful} successful, {failed} failed.",
                "results": results,
                "summary": {
                    "total": len(results),
                    "successful": successful,
                    "failed": failed
                }
            })
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# Removed bulk assignment routes - AI now suggests courses directly to employees

# NEW: Clean up duplicate course assignments
@admin_bp.route('/admin/cleanup_duplicates', methods=['POST'])
def cleanup_duplicate_assignments():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Find and remove duplicate assignments, keeping only the first one
            cursor.execute("""
                DELETE ca1 FROM course_assigned ca1
                INNER JOIN course_assigned ca2 
                WHERE ca1.assignment_id > ca2.assignment_id 
                AND ca1.emp_id = ca2.emp_id 
                AND ca1.course_name = ca2.course_name
            """)
            
            deleted_count = cursor.rowcount
            conn.commit()
            
        return jsonify({
            "success": True, 
            "message": f"Cleaned up {deleted_count} duplicate course assignments"
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# NEW: Get duplicate assignments report
@admin_bp.route('/admin/duplicate_report', methods=['GET'])
def get_duplicate_report():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Find duplicate assignments
            cursor.execute("""
                SELECT 
                    ca.emp_id,
                    e.NAME as employee_name,
                    ca.course_name,
                    COUNT(*) as assignment_count
                FROM course_assigned ca
                JOIN employee e ON ca.emp_id = e.id
                GROUP BY ca.emp_id, ca.course_name
                HAVING COUNT(*) > 1
                ORDER BY e.NAME, ca.course_name
            """)
            duplicates = cursor.fetchall()
            
        return jsonify({
            "success": True, 
            "duplicates": duplicates
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    finally:
        conn.close()

# --- Report Download Route ---
@admin_bp.route('/admin/generate_report')
def generate_report():
    if session.get('role') != 'admin':
        return redirect('/')


    # Department mapping: numeric code to domain string
    department_map = {
        '1': 'Frontend Developer',
        '2': 'Backend Developer',
        '3': 'Database Engineer',
        # Add more as needed
    }

    report_type = request.args.get('type')
    target = request.args.get('target', '')


    # Determine department filter from either ?department=... or ?type=department&target=...
    department_code = request.args.get('department')
    if not department_code and report_type == 'department' and target:
        department_code = target
    department_domain = department_map.get(department_code)

    # If type=individual, filter by employee ID
    individual_emp_id = None
    if report_type == 'individual' and target:
        try:
            individual_emp_id = int(target)
        except Exception:
            individual_emp_id = target  # fallback if emp_id is string

    # Generate a CSV report of all employees from the database
    conn = get_db_connection()
    output = io.StringIO()
    writer = csv.writer(output)
    try:
        with conn.cursor() as cursor:

            # Fetch all employees, optionally filter by department or individual
            if individual_emp_id:
                cursor.execute("SELECT id, NAME, domain FROM employee WHERE id = %s", (individual_emp_id,))
            elif department_domain:
                cursor.execute("SELECT id, NAME, domain FROM employee WHERE domain = %s", (department_domain,))
            else:
                cursor.execute("SELECT id, NAME, domain FROM employee")
            employees = cursor.fetchall()


            # Fetch all course assignments, optionally filter by department employees
            if department_domain:
                emp_ids = [emp['id'] for emp in employees]
                if emp_ids:
                    format_strings = ','.join(['%s'] * len(emp_ids))
                    cursor.execute(f"SELECT emp_id, course_name, status, progress FROM course_assigned WHERE emp_id IN ({format_strings})", tuple(emp_ids))
                    course_assignments = cursor.fetchall()
                else:
                    course_assignments = []
            else:
                cursor.execute("SELECT emp_id, course_name, status, progress FROM course_assigned")
                course_assignments = cursor.fetchall()

            # Build a mapping from emp_id to courses by status
            from collections import defaultdict
            inprogress_map = defaultdict(list)
            completed_map = defaultdict(list)
            for ca in course_assignments:
                if ca['status'] == 'In Progress':
                    inprogress_map[ca['emp_id']].append(ca['course_name'])
                elif ca['status'] == 'Completed':
                    completed_map[ca['emp_id']].append(ca['course_name'])

            # Write header
            writer.writerow(['ID', 'Name', 'Domain', 'Course', 'Status', 'Completion %'])
            # Build a mapping from (emp_id, course_name) to progress
            progress_map = {}
            for ca in course_assignments:
                progress_map[(ca['emp_id'], ca['course_name'])] = ca.get('progress', 'null')

            # For each employee, write one row per course assignment (in progress or completed)
            for emp in employees:
                emp_id = emp.get('id')
                name = emp.get('NAME', 'null') if emp.get('NAME') is not None else 'null'
                domain = emp.get('domain', 'null') if emp.get('domain') is not None else 'null'
                # Gather all in-progress and completed courses for this employee
                course_rows = []
                for course in inprogress_map[emp_id]:
                    course_rows.append((course, 'In Progress'))
                for course in completed_map[emp_id]:
                    course_rows.append((course, 'Completed'))
                # If no courses, show null
                if not course_rows:
                    writer.writerow([
                        emp_id if emp_id is not None else 'null',
                        name,
                        domain,
                        'null',
                        'null',
                        'null'
                    ])
                else:
                    for course_name, status in course_rows:
                        percent = progress_map.get((emp_id, course_name), 'null')
                        writer.writerow([
                            emp_id if emp_id is not None else 'null',
                            name,
                            domain,
                            course_name,
                            status,
                            percent
                        ])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='employee_report.csv'
        )
    finally:
        conn.close()

