import pandas as pd


long_absences = pd.read_csv('step1_output.csv')


student_data = {
    'student_id': [101, 107, 108],
    'student_name': ['Alice', 'Bob', 'Charlie'],
    'parent_email': ['alice_parent@gmail.com', 'invalid_email@', 'charlie@gmail.com']
}

students_df = pd.DataFrame(student_data)

merged_df = long_absences.merge(students_df, on='student_id', how='left')

def is_valid_email(email):
    if '@' in email:
        local, domain = email.split('@')
        if '.' in domain and local.isidentifier() and not local[0].isdigit():
            return True
    return False


merged_df['email'] = merged_df['parent_email'].apply(lambda x: x if is_valid_email(x) else None)

merged_df['msg'] = merged_df.apply(
    lambda row: f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date']} to {row['absence_end_date']} for {row['total_absent_days']} days. Please ensure their attendance improves."
    if row['email'] else None,
    axis=1
)


merged_df.to_csv('final_output.csv', index=False)
print("Step 2 completed. Final results saved to 'final_output.csv'.")
