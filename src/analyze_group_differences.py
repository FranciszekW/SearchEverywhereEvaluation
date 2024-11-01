import pandas as pd
import json

# Load dataset
df = pd.read_csv('../data/2024InternshipData.csv')

# Parse the event_data json column
df['event_data'] = df['event_data'].apply(json.loads)

# Extract the session id and create unique identifier for each (device, session) pair,
# it will be useful to calculate average session time later
df['session_id'] = df['event_data'].apply(lambda x: x['session_id'])
df['unique_id'] = df['device_id'] + '_' + df['session_id']
# Extract experiment groups into a new column
df['experimentGroup'] = df['event_data'].apply(lambda x: x['experimentGroup'])

# Split data into experiment groups
groups = {
    0: df[df['experimentGroup'] == 0],
    1: df[df['experimentGroup'] == 1]
}


# Function to calculate successful searches
def calculate_successful_searches(df_group):
    successful_searches = len(
        df_group[df_group['event_data'].apply(lambda x: x['selectedIndexes'] is not None)])
    finished_searches = len(df_group[df_group['event_id'] == 'sessionFinished'])
    return successful_searches, successful_searches / finished_searches if finished_searches > 0 else 0


# Function to calculate average session duration
def calculate_average_session_time(df_group):
    session_durations = df_group.groupby('unique_id')['time_epoch'].agg(['min', 'max'])
    session_durations['duration'] = session_durations['max'] - session_durations['min']
    return round(session_durations['duration'].mean() / 1000, 4)  # Convert ms to seconds and round to 4 decimal places


# Calculate and print results for each group
for group_id, group_df in groups.items():
    print(f'\nGroup {group_id} size: {len(group_df)}')

    # Successful searches
    successful_searches, success_rate = calculate_successful_searches(group_df)
    print(f'Group {group_id} successful searches: {successful_searches}')
    print(f'Group {group_id} percentage of successful searches: {success_rate}')

    # Average session duration
    avg_time_spent = calculate_average_session_time(group_df)
    print(f'Group {group_id} average time spent on the Search Everywhere tab: {avg_time_spent}s')