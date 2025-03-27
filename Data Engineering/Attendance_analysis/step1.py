import pandas as pd


data = {
    'student_id': [101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101],
    'attendance_date': [
        '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04',
        '2024-03-05', '2024-03-06', '2024-03-08', '2024-03-09',
        '2024-03-10', '2024-03-11', '2024-03-12', '2024-03-13',
        '2024-03-14', '2024-03-16'
    ],
    'status': ['Absent', 'Present', 'Absent', 'Present', 'Present', 'Absent', 'Absent', 'Absent', 'Present', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent']
}

attendance_df = pd.DataFrame(data)
attendance_df['attendance_date'] = pd.to_datetime(attendance_df['attendance_date'])


attendance_df['group'] = (attendance_df['status'] != 'Absent').cumsum()

streaks = (
    attendance_df[attendance_df['status'] == 'Absent']
    .groupby(['student_id', 'group'])
    .agg(
        absence_start_date=('attendance_date', 'min'),
        absence_end_date=('attendance_date', 'max'),
        total_absent_days=('attendance_date', 'count')
    )
    .reset_index()
)


long_absences = streaks[streaks['total_absent_days'] > 3]


latest_absences = (
    long_absences.sort_values('absence_end_date')
    .groupby('student_id')
    .tail(1)
    .drop(columns=['group'])
)


latest_absences.to_csv('step1_output.csv', index=False)
print("Step 1 completed. Output saved to 'step1_output.csv'.")
