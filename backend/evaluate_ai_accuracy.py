import csv
import json
from sentence_transformers import SentenceTransformer, util

# Load the AI model
print("🤖 Loading AI model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✅ Model loaded!\n")

def create_synthetic_resume(candidate):
    """Create a resume text from candidate data"""
    return f"""
{candidate['name']}
Education: {candidate['education']}
Experience: {candidate['experience']} years

Skills:
{candidate['skills']}

Certifications:
{candidate['certifications']}

Looking for: {candidate['job_role']} position
    """.strip()

def create_job_description(job_role, required_skills):
    """Create a job description"""
    return f"""
We are hiring for a {job_role} position.

Required Skills: {required_skills}
Experience level: Mid to Senior level
Education: Bachelor's degree or equivalent

The ideal candidate will have strong technical skills and proven experience in the field.
    """.strip()

def calculate_ai_score(resume_text, job_description, experience_years, education):
    """
    Calculate AI match score with multiple factors:
    - Semantic similarity (60% weight)
    - Experience bonus (25% weight)
    - Education bonus (15% weight)
    """
    # 1. Semantic similarity (base score)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity = util.cos_sim(resume_embedding, job_embedding)
    semantic_score = float(similarity.item()) * 100
    
    # 2. Experience bonus
    try:
        exp = int(experience_years)
        if exp >= 10:
            exp_bonus = 25
        elif exp >= 7:
            exp_bonus = 20
        elif exp >= 5:
            exp_bonus = 15
        elif exp >= 3:
            exp_bonus = 10
        else:
            exp_bonus = 5
    except:
        exp_bonus = 5
    
    # 3. Education bonus
    edu_lower = education.lower()
    if 'phd' in edu_lower or 'ph.d' in edu_lower:
        edu_bonus = 15
    elif 'master' in edu_lower or 'm.sc' in edu_lower or 'm.tech' in edu_lower or 'mba' in edu_lower:
        edu_bonus = 12
    elif 'bachelor' in edu_lower or 'b.sc' in edu_lower or 'b.tech' in edu_lower:
        edu_bonus = 10
    else:
        edu_bonus = 5
    
    # Weighted combination
    final_score = (semantic_score * 0.60) + (exp_bonus * 1.0) + (edu_bonus * 1.0)
    
    return round(final_score, 2)

def ai_decision(score):
    """Convert score to BINARY decision (Hire or Reject)"""
    if score >= 55:  
        return "Hire"
    else:
        return "Reject"


def evaluate_system():
    """Test the AI on all 1000 resumes"""
    csv_file = 'data/AI_Resume_Screening.csv'
    
    results = []
    correct_predictions = 0
    total_cases = 0
    
    # Statistics
    tp = 0  # True Positive (correctly predicted Hire)
    tn = 0  # True Negative (correctly predicted Reject)
    fp = 0  # False Positive (predicted Hire, was Reject)
    fn = 0  # False Negative (predicted Reject, was Hire)
    
    print("📊 Testing AI on 1,000 resumes...\n")
    print("=" * 70)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for i, row in enumerate(csv_reader, 1):
            candidate = {
                'name': row.get('Name', ''),
                'skills': row.get('Skills', ''),
                'experience': row.get('Experience (Years)', '0'),
                'education': row.get('Education', ''),
                'certifications': row.get('Certifications', ''),
                'job_role': row.get('Job Role', '')
            }
            
            resume_text = create_synthetic_resume(candidate)
            job_description = create_job_description(
                candidate['job_role'], 
                candidate['skills']
            )
            
            # AI makes its prediction (with enhanced scoring)
            ai_score = calculate_ai_score(
                resume_text, 
                job_description,
                candidate['experience'],
                candidate['education']
            )
            ai_pred = ai_decision(ai_score)
            
            # Get actual HR decision
            actual_hr_decision = row.get('Recruiter Decision', 'Unknown')
            
            # For binary classification (Hire vs Not Hire)
            ai_hire = (ai_pred == "Hire")
            hr_hire = (actual_hr_decision == "Hire")
            
            # Update confusion matrix
            if ai_hire and hr_hire:
                tp += 1
                is_correct = True
            elif not ai_hire and not hr_hire:
                tn += 1
                is_correct = True
            elif ai_hire and not hr_hire:
                fp += 1
                is_correct = False
            else:  # not ai_hire and hr_hire
                fn += 1
                is_correct = False
            
            if is_correct:
                correct_predictions += 1
            
            total_cases += 1
            
            results.append({
                'candidate': candidate['name'],
                'job_role': candidate['job_role'],
                'experience': candidate['experience'],
                'education': candidate['education'],
                'ai_score': ai_score,
                'ai_decision': ai_pred,
                'hr_decision': actual_hr_decision,
                'correct': is_correct
            })
            
            if i % 100 == 0:
                current_accuracy = (correct_predictions / total_cases) * 100
                print(f"✓ Processed {i}/1000 resumes... (Accuracy: {current_accuracy:.1f}%)")
    
    print("=" * 70)
    print("\n🎉 Testing Complete!\n")
    
    # Calculate metrics
    accuracy = (correct_predictions / total_cases) * 100
    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    print(f"Total Resumes Tested:     {total_cases}")
    print(f"Correct Predictions:      {correct_predictions}")
    print(f"Incorrect Predictions:    {total_cases - correct_predictions}")
    print(f"\n🎯 ACCURACY:  {accuracy:.2f}%")
    print(f"📈 PRECISION: {precision:.2f}%")
    print(f"📊 RECALL:    {recall:.2f}%")
    print(f"⭐ F1-SCORE:  {f1_score:.2f}%")
    print("=" * 70)
    
    print("\n📝 Confusion Matrix:")
    print(f"True Positives (Correctly hired):    {tp}")
    print(f"True Negatives (Correctly rejected): {tn}")
    print(f"False Positives (Wrongly hired):     {fp}")
    print(f"False Negatives (Wrongly rejected):  {fn}")
    
    # Show examples
    print("\n📝 Sample Results (First 10):")
    print("-" * 70)
    for i, result in enumerate(results[:10], 1):
        status = "✅" if result['correct'] else "❌"
        print(f"{i}. {result['candidate']} - {result['job_role']}")
        print(f"   Exp: {result['experience']}y | Edu: {result['education']}")
        print(f"   AI Score: {result['ai_score']}% | AI: {result['ai_decision']} | HR: {result['hr_decision']} {status}")
        print()
    
    # Save results
    with open('ai_evaluation_results.json', 'w') as f:
        json.dump({
            'summary': {
                'total_cases': total_cases,
                'correct_predictions': correct_predictions,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            },
            'confusion_matrix': {
                'true_positives': tp,
                'true_negatives': tn,
                'false_positives': fp,
                'false_negatives': fn
            },
            'detailed_results': results
        }, f, indent=2)
    
    print("\n💾 Detailed results saved to: ai_evaluation_results.json")
    
    return accuracy, results

if __name__ == "__main__":
    print("=" * 70)
    print("🔬 AI RESUME SCREENING SYSTEM - IMPROVED EVALUATION")
    print("=" * 70)
    print("\nEnhancements:")
    print("✓ Multi-factor scoring (semantic + experience + education)")
    print("✓ Adjusted thresholds for realistic predictions")
    print("✓ Detailed metrics (Precision, Recall, F1-Score)\n")
    
    input("Press Enter to start the evaluation...")
    print()
    
    accuracy, results = evaluate_system()
    
    print("\n🎓 This is your research data!")
