import csv
from datetime import datetime

# Load schedule from CSV file
def load_schedule(filename):
    schedule = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            # Split the time range into start and end times
            start_time, end_time = row[2].split('-')
            schedule.append({
                "course": row[0],
                "day": row[1].strip(),
                "start_time": start_time.strip(),
                "end_time": end_time.strip(),
                "holiday": row[3].strip().lower() == 'yes',
                "attendance": int(row[4]),  # Assuming attendance is the 5th column
                "crucial_topics": row[5].strip().lower() == 'yes'  # Crucial topics information
            })
    return schedule

# Utility-based Agent function
def utility_based_agent(schedule):
    current_day = datetime.now().strftime("%A")
    current_time_str = datetime.now().strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M").time()

    for entry in schedule:
        if entry["day"] == current_day and not entry["holiday"]:
            entry_start_time = datetime.strptime(entry["start_time"], "%H:%M").time()
            entry_end_time = datetime.strptime(entry["end_time"], "%H:%M").time()
            if entry_start_time <= current_time <= entry_end_time and entry["crucial_topics"]:
                print(f"Current day: {current_day}, Current time: {current_time_str}")
                print(f"Reminder: Attend {entry['course']} class because crucial topics are being taught.")
                return True
    
    print(f"Current day: {current_day}, Current time: {current_time_str}")
    print("No crucial topics being taught at the current time.")
    return False

# Example usage
schedule = load_schedule("schedule.csv")
utility_based_agent(schedule)
