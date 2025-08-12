# F:\vscode\New folder\Samsaram athu Minsaram\ai_agents.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
from db import get_db_connection
import json

# Use your Gemini API Key (set as environment variable)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key="AIzaSyC9i-w-UJxYINBWdveXDoRw8iZtRy4GnMo"
)


def call_ai(prompt: str):
    """Utility function to call the AI model and clean the response."""
    try:
        response = llm.invoke(prompt)
        # A more robust way to clean the response, removing markdown code blocks
        clean_text = response.content.strip().replace("```json", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- AGENT 0: Domain Assignment (Utility for Login) ---
def assign_domain_with_ai(emp_id: int):
    """
    Analyzes an employee's skills using an AI and assigns them a domain if one is not set.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT HTML, CSS, JAVASCRIPT, PYTHON, C, CPP, JAVA, SQL_TESTING, TOOLS_COURSE FROM employee WHERE id = %s", (emp_id,))
            skills = cursor.fetchone()
            if not skills: 
                print(f"Employee {emp_id} not found")
                return None
            
            # Check if employee already has a domain
            cursor.execute("SELECT domain FROM employee WHERE id = %s", (emp_id,))
            existing_domain = cursor.fetchone()
            if existing_domain and existing_domain.get('domain'):
                print(f"Employee {emp_id} already has domain: {existing_domain['domain']}")
                return existing_domain['domain']
        
        # Prepare skill scores for AI analysis
        skill_scores_text = ", ".join([f"{key}: {value}" for key, value in skills.items() if value is not None])
        
        # Create a more detailed prompt for better AI analysis
        prompt = f"""
        Analyze the following skill scores and assign the most appropriate domain:
        {skill_scores_text}
        
        Available domains:
        - Frontend Developer (for HTML, CSS, JavaScript skills)
        - Backend Developer (for Python, Java, C, C++ skills)
        - Database Engineer (for SQL Testing, Tools Course skills)
        
        Return only the domain name: Frontend Developer, Backend Developer, or Database Engineer.
        """
        
        assigned_domain = call_ai(prompt)
        valid_domains = ["Frontend Developer", "Backend Developer", "Database Engineer"]
        
        # Clean up AI response and validate
        assigned_domain = assigned_domain.strip() if assigned_domain else ""
        
        # Fallback logic if AI response is invalid
        if assigned_domain not in valid_domains:
            print(f"AI returned invalid domain '{assigned_domain}', using fallback logic")
            
            # Calculate average scores for each domain
            frontend_score = (skills.get('HTML', 0) + skills.get('CSS', 0) + skills.get('JAVASCRIPT', 0)) / 3
            backend_score = (skills.get('PYTHON', 0) + skills.get('JAVA', 0) + skills.get('C', 0) + skills.get('CPP', 0)) / 4
            database_score = (skills.get('SQL_TESTING', 0) + skills.get('TOOLS_COURSE', 0)) / 2
            
            # Assign domain based on highest average score
            if frontend_score >= backend_score and frontend_score >= database_score:
                assigned_domain = "Frontend Developer"
            elif backend_score >= frontend_score and backend_score >= database_score:
                assigned_domain = "Backend Developer"
            else:
                assigned_domain = "Database Engineer"
        
        # Update the database
        with conn.cursor() as cursor:
            cursor.execute("UPDATE employee SET domain = %s WHERE id = %s", (assigned_domain, emp_id))
            conn.commit()
        
        print(f"Assigned domain '{assigned_domain}' to employee {emp_id}")
        return assigned_domain
        
    except Exception as e:
        print(f"Error assigning domain to employee {emp_id}: {str(e)}")
        if conn and conn.open: 
            conn.rollback()
        return None
    finally:
        if conn and conn.open: 
            conn.close()


# --- REMODELED AGENT 1: Profile Agent ---
def profile_agent(emp_id: int):
    """
    Infers latent skill vectors by correlating skills, course history, and performance ratings.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employee WHERE id = %s", (emp_id,))
            employee = cursor.fetchone()
            if not employee: return {"error": "Employee not found."}
            
            # BUG FIX: Correctly query the course_completed table which has no 'status' column.
            cursor.execute("SELECT course_name, completion_date FROM course_completed WHERE emp_id = %s", (emp_id,))
            course_completions = cursor.fetchall()

            cursor.execute("SELECT course_name, marks_obtained FROM assessment_marks WHERE emp_id = %s", (emp_id,))
            performance_ratings = cursor.fetchall()

        skill_columns = ['HTML', 'CSS', 'JAVASCRIPT', 'PYTHON', 'C', 'CPP', 'JAVA', 'SQL_TESTING', 'TOOLS_COURSE']
        skills = {skill: employee.get(skill, 0) or 0 for skill in skill_columns}
        
        completions_text = "\n".join([f"- {c['course_name']} (Completed on {c['completion_date']:%Y-%m-%d})" for c in course_completions]) or "None"
        ratings_text = "\n".join([f"- {p['course_name']}: {p['marks_obtained']}/10" for p in performance_ratings]) or "None"

        prompt = f"""
        You are an expert AI HR Analyst. Your task is to analyze disparate data to create a comprehensive employee skill profile and infer latent skills.

        **Employee Input Data:**
        - **Domain:** {employee.get('domain')}
        - **Explicit Skill Scores (out of 100):** {skills}
        - **Past Course Completions:**
        {completions_text}
        - **Performance Ratings (Assessment Scores):**
        {ratings_text}

        **Task & Reasoning:**
        1.  **Correlate Data:** Analyze all inputs to find connections. For example, if an employee scored high in 'PYTHON' and also has a high assessment score in the 'Fundamentals of Java' course, infer a latent skill in 'Object-Oriented Programming'.
        2.  **Generate Output:** Produce a detailed "Employee Skill Vector & History Log".

        **Output Format (use Markdown):**
        **Overall Summary:** A brief, 2-sentence summary of the employee's profile.
        **Explicit Skills:** List the top 3 skills from the scores.
        **Inferred Latent Skills:** List 2-3 latent skills you have inferred from the data correlation.
        **Learning History Highlights:** Mention 1-2 key takeaways from their course and assessment history.
        """
        output = call_ai(prompt)
        return {
            "agent": "Profile Agent",
            "summary": "Your AI-Generated Skill Profile:",
            "details": [line.strip() for line in output.split('\n') if line.strip()]
        }
    except Exception as e:
        return {"error": f"An error occurred in the Profile Agent: {e}"}
    finally:
        if conn and conn.open: conn.close()

# --- REMODELED AGENT 2: Assessment Agent ---
def assessment_agent(emp_id: int):
    """
    Returns a summary, completed courses, and recent assessment results for the assessment agent dashboard.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Fetch completed courses
            cursor.execute("SELECT course_name FROM course_completed WHERE emp_id = %s", (emp_id,))
            completed_courses = [row['course_name'] for row in cursor.fetchall()]
            # Fetch recent assessment results (last 5)
            cursor.execute("SELECT course_name, marks_obtained FROM assessment_marks WHERE emp_id = %s ORDER BY assessment_id DESC LIMIT 5", (emp_id,))
            recent_assessments = cursor.fetchall()
            # Build summary
            summary = f"You have completed {len(completed_courses)} course(s). You can take assessments to test your knowledge." if completed_courses else "No completed courses yet. Complete a course to unlock assessments."
            details = [summary]
            return {
                "summary": summary,
                "details": details,
                "completed_courses": completed_courses,
                "recent_assessments": recent_assessments
            }
    except Exception as e:
        return {"error": f"An error occurred in the Assessment Agent: {e}"}
    finally:
        if conn and conn.open: conn.close()

def generate_completed_courses_quiz(emp_id: int, completed_courses):
    """
    Generate a quiz based on the courses an employee has completed.
    """
    try:
        # Extract course names from completed courses
        course_names = [course['course_name'] for course in completed_courses]
        
        if not course_names:
            return None
            
        # Create a prompt for the AI to generate a quiz
        prompt = f"""
        Generate a 5-question multiple-choice quiz to test knowledge across these completed courses:
        {', '.join(course_names)}
        
        The quiz should test the employee's retention of key concepts from these courses.
        Each question should relate to one of the completed courses.
        
        Provide the output as a valid JSON array of objects with keys: "question", "options" (array of 4), and "correctAnswerIndex" (int 0-3).
        Return only the raw JSON array.
        """
        
        response = llm.invoke(prompt)
        raw_response = response.content.strip()
        json_start = raw_response.find('[')
        json_end = raw_response.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON array in AI response.")
        
        json_str = raw_response[json_start:json_end]
        questions = json.loads(json_str)
        
        if isinstance(questions, list) and len(questions) > 0 and all(k in questions[0] for k in ["question", "options", "correctAnswerIndex"]):
            # Rename correctAnswerIndex to correct_answer for consistency with the template
            for question in questions:
                question["correct_answer"] = question.pop("correctAnswerIndex")
            return questions
        else:
            raise ValueError("Invalid JSON structure.")
            
    except Exception as e:
        print(f"Error generating quiz from completed courses: {e}")
        return None

# --- REMODELED AGENT 3: Recommender Agent ---
def recommender_agent(emp_id: int):
    """
    Crafts a ranked learning path with narrative explanations.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employee WHERE id = %s", (emp_id,)); employee = cursor.fetchone()
            if not employee: return {"error": "Employee not found."}
            cursor.execute("SELECT course_name, marks_obtained FROM assessment_marks WHERE emp_id = %s", (emp_id,)); assessment_scores = cursor.fetchall()
            cursor.execute("SELECT CourseName FROM course WHERE Domain = %s", (employee.get('domain'),)); available_courses = [row['CourseName'] for row in cursor.fetchall()]

        skill_columns = ['HTML', 'CSS', 'JAVASCRIPT', 'PYTHON', 'C', 'CPP', 'JAVA', 'SQL_TESTING', 'TOOLS_COURSE']
        skills = {skill: employee.get(skill, 0) or 0 for skill in skill_columns}
        scores_text = "\n".join([f"- {p['course_name']}: {p['marks_obtained']}/10" for p in assessment_scores]) or "None"

        prompt = f"""
        You are an expert AI Learning Path Designer. Create a personalized, ranked learning path.

        **Employee Profile & Assessment Scores:**
        - **Domain:** {employee.get('domain')}
        - **Skill Scores:** {skills}
        - **Assessment Scores:** {scores_text}
        - **Available Courses for Domain:** {', '.join(available_courses)}

        **Task & Reasoning:**
        1.  **Analyze Profile:** Identify the biggest skill gap based on both low skill scores and low assessment scores.
        2.  **Select Course:** Choose the single best course from the "Available Courses" list that directly addresses this gap.
        3.  **Craft Narrative:** Write a short, personalized explanation for *why* this course is being recommended.
        4.  **Generate Output:** Create a ranked learning path.

        **Output Format (use Markdown):**
        **Recommended Learning Path:**
        1.  **Course:** [Full Course Name]
            - **Reasoning:** [Your crafted narrative explanation]
        """
        output = call_ai(prompt)
        return {
            "agent": "Recommender Agent",
            "summary": "Your Personalized Learning Path:",
            "details": [line.strip() for line in output.split('\n') if line.strip()]
        }
    except Exception as e:
        return {"error": f"An error occurred in the Recommender Agent: {e}"}
    finally:
        if conn and conn.open: conn.close()

# --- REMODELED AGENT 4: Tracker Agent ---
def tracker_agent(emp_id: int):
    """
    Analyzes completion patterns, quiz re-scores to detect plateaus, and provides AI-powered refreshment recommendations.
    Enhanced to clearly show enrolled courses and their calibration/progress.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get employee information
            cursor.execute("SELECT NAME, domain FROM employee WHERE id = %s", (emp_id,))
            employee = cursor.fetchone()
            if not employee or 'NAME' not in employee:
                return {"error": "Employee not found or missing NAME field."}
            
            # Get course progress data with more details
            cursor.execute("""
                SELECT 
                    ca.course_name, 
                    ca.status, 
                    ca.progress,
                    c.Domain as course_domain,
                    c.CourseFile
                FROM course_assigned ca
                LEFT JOIN course c ON ca.course_name = c.CourseName
                WHERE ca.emp_id = %s
                ORDER BY ca.status DESC, ca.progress DESC
            """, (emp_id,))
            courses = cursor.fetchall() or []
            
            # Get assessment attempts and scores
            cursor.execute("""
                SELECT 
                    course_name, 
                    COUNT(*) as attempts,
                    MAX(marks_obtained) as best_score,
                    AVG(marks_obtained) as avg_score
                FROM assessment_marks 
                WHERE emp_id = %s 
                GROUP BY course_name
            """, (emp_id,))
            assessment_data = {row['course_name']: row for row in (cursor.fetchall() or [])}
            
            # Get recent assessment scores
            cursor.execute("""
                SELECT course_name, marks_obtained
                FROM assessment_marks 
                WHERE emp_id = %s 
                ORDER BY marks_obtained DESC 
                LIMIT 10
            """, (emp_id,))
            recent_scores = cursor.fetchall() or []

        if not courses:
            summary = f"📊 **Learning Tracker for {employee.get('NAME', 'Employee')}**\n\nNo learning activity to track yet."
            details = ["🎯 **Get Started**: Request a course recommendation from the main dashboard to begin your learning journey!"]
            refreshment = "🤖 **AI Recommendation**: Start with a foundational course in your domain to build momentum!"
        else:
            # Calculate overall statistics
            total_courses = len(courses)
            completed_courses = len([c for c in courses if c.get('status') == 'Completed'])
            in_progress_courses = len([c for c in courses if c.get('status') == 'In Progress'])
            not_started_courses = len([c for c in courses if c.get('status') == 'Not Started'])
            avg_progress = sum(c.get('progress', 0) for c in courses) / total_courses if total_courses > 0 else 0
            
            # Create detailed summary
            summary = f"""📊 **Learning Tracker for {employee.get('NAME', 'Employee')}**

🎯 **Overall Progress Summary:**
• **Total Enrolled Courses**: {total_courses}
• **Completed**: {completed_courses} ({completed_courses/total_courses*100:.1f}%)
• **In Progress**: {in_progress_courses} ({in_progress_courses/total_courses*100:.1f}%)
• **Not Started**: {not_started_courses} ({not_started_courses/total_courses*100:.1f}%)
• **Average Progress**: {avg_progress:.1f}%

🏆 **Domain**: {employee.get('domain', 'Not Assigned')}"""

            # Create detailed course breakdown
            details = []
            details.append("📚 **Enrolled Courses & Calibration:**")
            details.append("─" * 50)
            
            # Group courses by status
            status_groups = {
                'Completed': [],
                'In Progress': [],
                'Not Started': []
            }
            
            for course in courses:
                cname = course.get('course_name', 'Unknown Course')
                cstatus = course.get('status', 'Unknown')
                cprogress = course.get('progress', 0)
                cdomain = course.get('course_domain', 'General')
                
                # Get assessment data for this course
                assessment_info = assessment_data.get(cname, {})
                attempts = assessment_info.get('attempts', 0)
                best_score = assessment_info.get('best_score', 0)
                avg_score = assessment_info.get('avg_score', 0)
                
                course_info = {
                    'name': cname,
                    'status': cstatus,
                    'progress': cprogress,
                    'domain': cdomain,
                    'attempts': attempts,
                    'best_score': best_score,
                    'avg_score': avg_score
                }
                
                status_groups[cstatus].append(course_info)
            
            # Display completed courses
            if status_groups['Completed']:
                details.append("\n✅ **COMPLETED COURSES:**")
                for course in status_groups['Completed']:
                    details.append(f"  🎓 **{course['name']}** ({course['domain']})")
                    details.append(f"     • Progress: {course['progress']}%")
                    if course['attempts'] > 0:
                        details.append(f"     • Assessment: {course['best_score']}/10 (Best), {course['avg_score']:.1f}/10 (Avg)")
                        details.append(f"     • Attempts: {course['attempts']}")
                    details.append("")
            
            # Display in-progress courses
            if status_groups['In Progress']:
                details.append("🔄 **IN PROGRESS COURSES:**")
                for course in status_groups['In Progress']:
                    details.append(f"  📖 **{course['name']}** ({course['domain']})")
                    details.append(f"     • Progress: {course['progress']}%")
                    if course['attempts'] > 0:
                        details.append(f"     • Assessment: {course['best_score']}/10 (Best), {course['avg_score']:.1f}/10 (Avg)")
                        details.append(f"     • Attempts: {course['attempts']}")
                    details.append("")
            
            # Display not started courses
            if status_groups['Not Started']:
                details.append("⏳ **NOT STARTED COURSES:**")
                for course in status_groups['Not Started']:
                    details.append(f"  📋 **{course['name']}** ({course['domain']})")
                    details.append(f"     • Progress: {course['progress']}%")
                    details.append("")
            
            # Add recent performance section
            if recent_scores:
                details.append("📈 **Recent Assessment Performance:**")
                details.append("─" * 30)
                for score in recent_scores[:5]:  # Show last 5 assessments
                    details.append(f"  • {score['course_name']}: {score['marks_obtained']}/10")
                details.append("")
            
            # Detect learning plateaus
            plateau_courses = []
            for course in courses:
                cname = course.get('course_name', 'Unknown Course')
                assessment_info = assessment_data.get(cname, {})
                attempts = assessment_info.get('attempts', 0)
                
                if attempts > 1:
                    plateau_courses.append(cname)
            
            if plateau_courses:
                details.append("⚠️ **Learning Plateaus Detected:**")
                details.append("These courses have multiple assessment attempts, indicating potential learning challenges:")
                for course in plateau_courses:
                    details.append(f"  • {course}")
                details.append("")
            
            # Generate AI-powered refreshment recommendations
            refreshment = generate_refreshment_recommendations(
                employee_name=employee.get('NAME', 'Employee'),
                domain=employee.get('domain', 'General'),
                total_courses=total_courses,
                completed_courses=completed_courses,
                in_progress_courses=in_progress_courses,
                avg_progress=avg_progress,
                plateau_courses=plateau_courses,
                recent_scores=recent_scores,
                courses=courses
            )
        
        return {
            "agent": "Tracker Agent", 
            "summary": summary, 
            "details": details,
            "refreshment": refreshment
        }
    except Exception as e:
        return {"error": f"An error occurred in the Tracker Agent: {e}"}
    finally:
        if conn and conn.open: conn.close()

def generate_refreshment_recommendations(employee_name, domain, total_courses, completed_courses, 
                                       in_progress_courses, avg_progress, plateau_courses, 
                                       recent_scores, courses):
    """
    Generate AI-powered refreshment recommendations based on learning patterns.
    Enhanced to provide more specific and actionable advice.
    """
    
    # Create a comprehensive prompt for AI analysis
    prompt = f"""
    As an AI Learning Coach, analyze this employee's learning data and provide personalized refreshment recommendations:

    **Employee Profile:**
    - Name: {employee_name}
    - Domain: {domain}
    
    **Learning Statistics:**
    - Total Courses: {total_courses}
    - Completed Courses: {completed_courses}
    - In Progress Courses: {in_progress_courses}
    - Average Progress: {avg_progress:.1f}%
    
    **Current Courses:**
    {chr(10).join([f"- {c['course_name']}: {c['status']} ({c['progress']}%)" for c in courses])}
    
    **Learning Plateaus:**
    {chr(10).join([f"- {course}" for course in plateau_courses]) if plateau_courses else "None detected"}
    
    **Recent Assessment Performance:**
    {chr(10).join([f"- {score['course_name']}: {score['marks_obtained']}/10" for score in recent_scores]) if recent_scores else "No recent assessments"}
    
    **Provide Detailed Refreshment Recommendations:**
    
    1. **Progress Analysis** - Analyze their current learning pace and progress patterns
    2. **Strengths & Weaknesses** - Identify areas where they excel and areas needing improvement
    3. **Learning Strategy** - Suggest specific strategies based on their performance
    4. **Next Steps** - Recommend what to focus on next for optimal learning
    5. **Study Tips** - Provide domain-specific study techniques
    6. **Motivation** - Give personalized encouragement and motivation
    7. **Plateau Solutions** - If plateaus detected, suggest specific ways to overcome them
    
    Format your response with clear sections and actionable advice.
    Be encouraging, specific, and practical.
    Focus on helping them improve their learning efficiency and overcome any challenges.
    """
    
    try:
        ai_response = call_ai(prompt)
        return f"🤖 **AI Learning Coach Recommendations:**\n\n{ai_response}"
    except Exception as e:
        # Enhanced fallback recommendations if AI fails
        fallback_recommendations = []
        
        # Progress-based recommendations
        if avg_progress < 30:
            fallback_recommendations.append("🐌 **Slow Progress Alert**: Your average progress is below 30%. Consider:\n   • Setting smaller, daily learning goals\n   • Allocating dedicated study time each day\n   • Reviewing completed sections before moving forward")
        elif avg_progress < 60:
            fallback_recommendations.append("📈 **Steady Progress**: You're making good progress! To accelerate:\n   • Try to complete one course before starting another\n   • Take practice quizzes regularly\n   • Review material weekly to reinforce learning")
        else:
            fallback_recommendations.append("🚀 **Excellent Progress**: You're progressing well! Keep up the momentum by:\n   • Maintaining your current study routine\n   • Helping others who might be struggling\n   • Exploring advanced topics in your domain")
        
        # Plateau-specific recommendations
        if plateau_courses:
            fallback_recommendations.append("🔄 **Plateau Solutions**: For courses with multiple attempts:\n   • Review the course material from the beginning\n   • Take notes while studying\n   • Practice with different learning methods (videos, reading, hands-on)\n   • Consider taking a short break and returning with fresh perspective")
        
        # Course load recommendations
        if in_progress_courses > 2:
            fallback_recommendations.append("📚 **Course Load Management**: You have multiple courses in progress:\n   • Focus on completing one course at a time\n   • Prioritize courses closest to completion\n   • Set weekly targets for each course")
        
        # Assessment performance recommendations
        if recent_scores:
            recent_avg = sum(score['marks_obtained'] for score in recent_scores) / len(recent_scores)
            if recent_avg < 6:
                fallback_recommendations.append("📝 **Assessment Improvement**: Your recent scores are below 60%:\n   • Review course material more thoroughly before assessments\n   • Take practice quizzes to identify weak areas\n   • Focus on understanding concepts rather than memorizing")
            elif recent_avg < 8:
                fallback_recommendations.append("📊 **Good Performance**: Your scores are solid! To reach excellence:\n   • Review missed questions to understand gaps\n   • Practice with more challenging problems\n   • Help others to reinforce your own understanding")
            else:
                fallback_recommendations.append("🏆 **Outstanding Performance**: Excellent scores! Consider:\n   • Mentoring others in your strong areas\n   • Exploring advanced topics\n   • Taking on more challenging courses")
        
        # Domain-specific advice
        if domain == "Frontend Developer":
            fallback_recommendations.append("🎨 **Frontend Focus**: As a Frontend Developer:\n   • Practice building small projects regularly\n   • Stay updated with latest CSS and JavaScript features\n   • Experiment with different frameworks and libraries")
        elif domain == "Backend Developer":
            fallback_recommendations.append("⚙️ **Backend Focus**: As a Backend Developer:\n   • Practice writing clean, efficient code\n   • Learn about database optimization\n   • Understand system architecture and design patterns")
        elif domain == "Database Engineer":
            fallback_recommendations.append("🗄️ **Database Focus**: As a Database Engineer:\n   • Practice writing complex queries\n   • Learn about database optimization and indexing\n   • Understand data modeling and normalization")
        
        # General encouragement
        fallback_recommendations.append(f"💪 **Personal Motivation**: Keep pushing forward, {employee_name}!\n   • Every completed course brings you closer to your goals\n   • Learning is a journey, not a destination\n   • Your dedication to improvement is admirable")
        
        return f"🤖 **AI Learning Coach Recommendations:**\n\n" + "\n\n".join(fallback_recommendations)


# --- Utility and Other Agents (Unchanged) ---
def generate_quiz_questions(course_name: str):
    """
    Generate assessment questions based on the actual course content.
    This function reads the course file and generates questions from the material covered.
    """
    import os
    
    # Get the course file path from database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CourseFile FROM course WHERE CourseName = %s", (course_name,))
            course_file = cursor.fetchone()
            
            if not course_file:
                # Fallback to generic quiz if course file is missing
                print(f"Course file not found in database for '{course_name}', generating fallback quiz.")
                fallback_prompt = f"""
                Generate a 10-question multiple-choice quiz on '{course_name}'.
                Provide the output as a valid JSON array of objects with keys: 'question', 'options' (array of 4), and 'correctAnswerIndex' (int 0-3).
                Return only the raw JSON array.
                """
                try:
                    response = llm.invoke(fallback_prompt)
                    raw_response = response.content.strip()
                    json_start = raw_response.find('[')
                    json_end = raw_response.rfind(']') + 1
                    if json_start == -1 or json_end == 0:
                        raise ValueError("No JSON array in fallback response.")
                    json_str = raw_response[json_start:json_end]
                    questions = json.loads(json_str)
                    if isinstance(questions, list) and len(questions) > 0 and all(k in questions[0] for k in ["question", "options", "correctAnswerIndex"]):
                        for q in questions:
                            if 'correctAnswerIndex' in q:
                                q['correct_answer'] = q.pop('correctAnswerIndex')
                        return {"success": True, "questions": questions, "note": "Generated fallback questions due to missing course file"}
                    else:
                        raise ValueError("Invalid JSON structure in fallback.")
                except Exception as fallback_error:
                    print(f"Fallback quiz generation also failed for '{course_name}': {fallback_error}")
                    return {"success": False, "message": "Failed to generate a valid quiz for this course."}
            
            course_file_name = course_file['CourseFile']
            course_file_path = os.path.join('static', 'courses', course_file_name)
            
            if not os.path.exists(course_file_path):
                # Fallback to generic quiz if course file is missing on server
                print(f"Course file not found on server for '{course_name}', generating fallback quiz.")
                fallback_prompt = f"""
                Generate a 10-question multiple-choice quiz on '{course_name}'.
                Provide the output as a valid JSON array of objects with keys: 'question', 'options' (array of 4), and 'correctAnswerIndex' (int 0-3).
                Return only the raw JSON array.
                """
                try:
                    response = llm.invoke(fallback_prompt)
                    raw_response = response.content.strip()
                    json_start = raw_response.find('[')
                    json_end = raw_response.rfind(']') + 1
                    if json_start == -1 or json_end == 0:
                        raise ValueError("No JSON array in fallback response.")
                    json_str = raw_response[json_start:json_end]
                    questions = json.loads(json_str)
                    if isinstance(questions, list) and len(questions) > 0 and all(k in questions[0] for k in ["question", "options", "correctAnswerIndex"]):
                        for q in questions:
                            if 'correctAnswerIndex' in q:
                                q['correct_answer'] = q.pop('correctAnswerIndex')
                        return {"success": True, "questions": questions, "note": "Generated fallback questions due to missing course file"}
                    else:
                        raise ValueError("Invalid JSON structure in fallback.")
                except Exception as fallback_error:
                    print(f"Fallback quiz generation also failed for '{course_name}': {fallback_error}")
                    return {"success": False, "message": "Failed to generate a valid quiz for this course."}
            
            # Read the course content
            with open(course_file_path, 'r', encoding='utf-8') as f:
                course_content = f.read()
            
            # Extract text content from HTML (remove HTML tags)
            import re
            # Remove HTML tags but keep text content
            text_content = re.sub(r'<[^>]+>', ' ', course_content)
            # Remove extra whitespace
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            # Limit content length to avoid token limits
            text_content = text_content[:8000]  # Limit to 8000 characters
            
            # Generate questions based on the actual course content
            prompt = f"""
            Based on the following course content from "{course_name}", generate a 10-question multiple-choice assessment quiz.
            
            Course Content:
            {text_content}
            
            Instructions:
            1. Generate questions that test understanding of the specific content covered in this course
            2. Questions should be based on the actual material presented, not general knowledge
            3. Focus on key concepts, definitions, and practical applications mentioned in the content
            4. Make sure all questions are answerable from the provided course material
            
            Provide the output as a valid JSON array of objects with keys: "question", "options" (array of 4), and "correctAnswerIndex" (int 0-3).
            Return only the raw JSON array.
            """
            
            response = llm.invoke(prompt)
            raw_response = response.content.strip()
            json_start = raw_response.find('[')
            json_end = raw_response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array in AI response.")
            
            json_str = raw_response[json_start:json_end]
            questions = json.loads(json_str)
            
            if isinstance(questions, list) and len(questions) > 0 and all(k in questions[0] for k in ["question", "options", "correctAnswerIndex"]):
                # Convert correctAnswerIndex to correct_answer for template compatibility
                for q in questions:
                    if 'correctAnswerIndex' in q:
                        q['correct_answer'] = q.pop('correctAnswerIndex')
                return {"success": True, "questions": questions}
            else:
                raise ValueError("Invalid JSON structure.")
                
    except Exception as e:
        print(f"Error generating quiz from course content for '{course_name}': {e}")
        # Fallback to general questions if content-based generation fails
        fallback_prompt = f"""
        Generate a 10-question multiple-choice quiz on "{course_name}".
        Provide the output as a valid JSON array of objects with keys: "question", "options" (array of 4), and "correctAnswerIndex" (int 0-3).
        Return only the raw JSON array.
        """
        try:
            response = llm.invoke(fallback_prompt)
            raw_response = response.content.strip()
            json_start = raw_response.find('[')
            json_end = raw_response.rfind(']') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array in fallback response.")
            json_str = raw_response[json_start:json_end]
            questions = json.loads(json_str)
            if isinstance(questions, list) and len(questions) > 0 and all(k in questions[0] for k in ["question", "options", "correctAnswerIndex"]):
                for q in questions:
                    if 'correctAnswerIndex' in q:
                        q['correct_answer'] = q.pop('correctAnswerIndex')
                return {"success": True, "questions": questions, "note": "Generated fallback questions due to content parsing error"}
            else:
                raise ValueError("Invalid JSON structure in fallback.")
        except Exception as fallback_error:
            print(f"Fallback quiz generation also failed for '{course_name}': {fallback_error}")
            return {"success": False, "message": "Failed to generate a valid quiz from course content."}
    finally:
        conn.close()

def get_ai_course_recommendation(emp_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employee WHERE id = %s", (emp_id,))
            employee = cursor.fetchone()
            
            if not employee:
                return {"success": False, "message": "Employee not found."}
            
            # If no domain assigned, try to assign one
            if not employee.get('domain'):
                assigned_domain = assign_domain_with_ai(emp_id)
                if assigned_domain:
                    employee['domain'] = assigned_domain
                else:
                    # If AI can't assign domain, use a default domain
                    employee['domain'] = 'Web Development'
            
            employee_domain = employee['domain']
            skill_columns = ['HTML', 'CSS', 'JAVASCRIPT', 'PYTHON', 'C', 'CPP', 'JAVA', 'SQL_TESTING', 'TOOLS_COURSE']
            skills = {skill: employee.get(skill, 0) or 0 for skill in skill_columns}
            
            # Get all available courses for the domain
            cursor.execute("SELECT CourseName FROM course WHERE Domain = %s", (employee_domain,))
            available_courses = [row['CourseName'] for row in cursor.fetchall()]
            
            # If no courses for this domain, try other domains
            if not available_courses:
                cursor.execute("SELECT DISTINCT Domain FROM course")
                all_domains = [row['Domain'] for row in cursor.fetchall()]
                for domain in all_domains:
                    cursor.execute("SELECT CourseName FROM course WHERE Domain = %s", (domain,))
                    domain_courses = [row['CourseName'] for row in cursor.fetchall()]
                    if domain_courses:
                        available_courses = domain_courses
                        employee_domain = domain
                        break
            
            if not available_courses:
                return {"success": False, "message": "No courses found in the system."}
            
            # Get already assigned courses to avoid duplicates
            cursor.execute("SELECT course_name FROM course_assigned WHERE emp_id = %s", (emp_id,))
            assigned_courses = [row['course_name'] for row in cursor.fetchall()]
            
            # Filter out already assigned courses
            available_courses = [course for course in available_courses if course not in assigned_courses]
            
            if not available_courses:
                return {"success": False, "message": "All available courses have already been assigned to you."}
            
            # Check if employee has courses in progress (but don't block completely)
            cursor.execute("SELECT * FROM course_assigned WHERE emp_id = %s AND status = 'In Progress'", (emp_id,))
            in_progress = cursor.fetchone()
            
            # Generate AI recommendation
            prompt = f"""
            Recommend one course from the list for an employee.
            Domain: {employee_domain}, Skills: {skills}
            Available Courses: {"- ".join(available_courses)}
            Return ONLY the course name.
            """
            recommended_course = call_ai(prompt)
            
            # Fallback logic if AI fails
            if "AI Error" in recommended_course or recommended_course not in available_courses:
                # Find course that matches weakest skill
                weakest_skill_name = min(skills, key=skills.get)
                for course in available_courses:
                    if weakest_skill_name.lower() in course.lower():
                        recommended_course = course
                        break
                else:
                    # If no skill match, pick the first available course
                    recommended_course = available_courses[0]
            
            # Add warning if employee has courses in progress
            warning = ""
            if in_progress:
                warning = f" Note: You have a course in progress ({in_progress['course_name']}). Consider completing it first."
            
            return {
                "success": True, 
                "recommendation": recommended_course,
                "warning": warning,
                "domain": employee_domain
            }
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}
    finally:
        conn.close()

def hr_agent_process_file(df: pd.DataFrame):
    conn = get_db_connection()
    employees_added = 0
    df.columns = [col.strip().upper() for col in df.columns]
    expected_cols = ['NAME', 'HTML', 'CSS', 'JAVASCRIPT', 'PYTHON', 'C', 'CPP', 'JAVA', 'SQL_TESTING', 'TOOLS_COURSE']
    if 'NAME' not in df.columns: return 0, "File is missing the required 'NAME' column."
    try:
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                employee_name = row['NAME']
                skill_values = {col: row.get(col, 0) for col in expected_cols if col != 'NAME'}
                cols = ", ".join(skill_values.keys()); placeholders = ", ".join(["%s"] * len(skill_values))
                sql_employee = f"INSERT INTO employee (NAME, {cols}) VALUES (%s, {placeholders})"
                cursor.execute(sql_employee, (employee_name, *skill_values.values()))
                new_emp_id = cursor.lastrowid
                username = f"{employee_name.lower().split()[0]}{new_emp_id}"; password = f"pass{new_emp_id}"; email = f"{username}@company.com"
                sql_credentials = "INSERT INTO credentials (emp_id, username, password, email, is_admin) VALUES (%s, %s, %s, %s, 0)"
                cursor.execute(sql_credentials, (new_emp_id, username, password, email))
                employees_added += 1
        conn.commit()
        return employees_added, None
    except Exception as e: conn.rollback(); return 0, str(e)

    finally: conn.close()
