import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='resume_screening_system',
            user='root',
            password='root'  # Your password
        )
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def save_screening_result(
    job_id: int,
    candidate_name: str,
    file_name: str,
    match_score: float,
    matched_skills: str,
    missing_skills: str,
    recommendation: str
) -> Optional[int]:
    """Save a screening result to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO screening_results 
                (job_id, candidate_name, file_name, match_score, 
                 matched_skills, missing_skills, recommendation)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                job_id, 
                candidate_name, 
                file_name, 
                match_score, 
                matched_skills, 
                missing_skills, 
                recommendation
            ))
            connection.commit()
            result_id = cursor.lastrowid
            print(f"✅ Saved screening result with ID: {result_id}")
            return result_id
        except Error as e:
            print(f"❌ Error saving result: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

def get_all_screenings() -> List[Dict]:
    """Get all screening results with job titles"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    s.id,
                    s.candidate_name,
                    s.file_name,
                    s.match_score,
                    s.matched_skills,
                    s.missing_skills,
                    s.recommendation,
                    s.screened_at,
                    j.title as job_title,
                    j.description as job_description
                FROM screening_results s
                LEFT JOIN job_descriptions j ON s.job_id = j.id
                ORDER BY s.screened_at DESC
            """)
            results = cursor.fetchall()
            print(f"✅ Retrieved {len(results)} screening results")
            return results
        except Error as e:
            print(f"❌ Error fetching results: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def get_job_description(job_id: int) -> Optional[Dict]:
    """Get a specific job description by ID"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM job_descriptions WHERE id = %s
            """, (job_id,))
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"❌ Error fetching job: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

def save_chat_message(user_message: str, bot_response: str) -> Optional[int]:
    """Save a chat conversation to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO chat_messages (user_message, bot_response)
                VALUES (%s, %s)
            """
            cursor.execute(query, (user_message, bot_response))
            connection.commit()
            message_id = cursor.lastrowid
            print(f"✅ Saved chat message with ID: {message_id}")
            return message_id
        except Error as e:
            print(f"❌ Error saving chat: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Test function
if __name__ == "__main__":
    print("Testing database connection...")
    conn = get_db_connection()
    if conn:
        print("✅ Database connection test successful!")
        conn.close()
    else:
        print("❌ Database connection test failed!")
