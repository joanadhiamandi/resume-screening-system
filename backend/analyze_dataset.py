import csv
from collections import Counter

csv_file = 'data/AI_Resume_Screening.csv'

hire_count = 0
reject_count = 0

with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        decision = row.get('Recruiter Decision', '')
        if decision == 'Hire':
            hire_count += 1
        elif decision == 'Reject':
            reject_count += 1

total = hire_count + reject_count
hire_pct = (hire_count / total) * 100
reject_pct = (reject_count / total) * 100

print("📊 HR Decision Distribution:")
print("=" * 50)
print(f"Hire:   {hire_count} ({hire_pct:.1f}%)")
print(f"Reject: {reject_count} ({reject_pct:.1f}%)")
print(f"Total:  {total}")
print("=" * 50)
