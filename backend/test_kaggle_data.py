import csv
import json

def load_kaggle_dataset():
    """
    Load Kaggle data and prepare it for testing
    Hides the actual HR decision to test our AI objectively
    """
    csv_file = 'data/AI_Resume_Screening.csv'
    
    test_cases = []
    actual_decisions = []  # We'll hide this from the AI
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # What our AI will see (no decision!)
            test_case = {
                'name': row.get('Name', ''),
                'skills': row.get('Skills', ''),
                'experience': row.get('Experience (Years)', '0'),
                'education': row.get('Education', ''),
                'certifications': row.get('Certifications', ''),
                'job_role': row.get('Job Role', '')
            }
            
            # What HR actually decided (for comparison later)
            actual_decision = row.get('Recruiter Decision', 'Unknown')
            
            test_cases.append(test_case)
            actual_decisions.append(actual_decision)
    
    return test_cases, actual_decisions

def create_job_description(job_role, skills):
    """Create a job description from the data"""
    return f"""
We are hiring for a {job_role} position.

Required Skills: {skills}

The ideal candidate will have strong technical skills and experience in the field.
    """.strip()

if __name__ == "__main__":
    print("📊 Loading Kaggle dataset...")
    test_cases, actual_decisions = load_kaggle_dataset()
    
    print(f"✅ Loaded {len(test_cases)} test cases")
    print(f"\nFirst test case:")
    print(json.dumps(test_cases[0], indent=2))
    print(f"\nActual HR decision: {actual_decisions[0]}")
    print("\n🎯 Your AI will NOT see the HR decision!")
    print("   It will make its own prediction, then we compare!")
