import csv
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='resume_screening_system',
            user='root',
            password='root'
        )
        return connection
    except Error as e:
        print(f"❌ Error: {e}")
        return None

def load_csv_to_database():
    """Load the Kaggle CSV into MySQL"""
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    # Read CSV file
    csv_file = 'data/AI_Resume_Screening.csv'
    
    print("📂 Reading CSV file...")
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        inserted_count = 0
        for row in csv_reader:
            try:
                job_title = row.get('Job Role', 'Unknown Position')
                skills = row.get('Skills', '')
                experience = row.get('Experience (Years)', '0')
                education = row.get('Education', '')
                
                # Create job description text
                job_description = f"""
We are looking for a {job_title} with the following qualifications:

Required Skills: {skills}
Experience: {experience} years
Education: {education} or equivalent

Responsibilities include working with modern technologies and contributing to our team's success.
                """.strip()
                
                # Check if this job already exists
                cursor.execute("""
                    SELECT id FROM job_descriptions 
                    WHERE title = %s LIMIT 1
                """, (job_title,))
                
                result = cursor.fetchone()
                
                if not result:
                    # Insert new job description
                    cursor.execute("""
                        INSERT INTO job_descriptions (title, description, required_skills)
                        VALUES (%s, %s, %s)
                    """, (job_title, job_description, skills))
                    inserted_count += 1
                
            except Error as e:
                print(f"⚠️  Error inserting row: {e}")
                continue
        
        connection.commit()
        print(f"✅ Successfully inserted {inserted_count} job descriptions!")
    
    cursor.close()
    connection.close()
    print("✅ Database updated successfully!")

if __name__ == "__main__":
    print("🚀 Loading Kaggle dataset into MySQL...")
    load_csv_to_database()
    print("🎉 Done!")