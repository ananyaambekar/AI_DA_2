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
                "attendance": int(row[4])  # Assuming attendance is the 5th column
            })
    return schedule

# Model-based Reflex Agent function
def model_based_reflex_agent(schedule):
    current_day = datetime.now().strftime("%A")
    current_time_str = datetime.now().strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M").time()

    for entry in schedule:
        if entry["day"] == current_day:
            if entry["holiday"]:
                print(f"Current day: {current_day}, Current time: {current_time_str}")
                print("No class today due to holiday.")
                return False
            entry_start_time = datetime.strptime(entry["start_time"], "%H:%M").time()
            entry_end_time = datetime.strptime(entry["end_time"], "%H:%M").time()
            if entry_start_time <= current_time <= entry_end_time:
                print(f"Current day: {current_day}, Current time: {current_time_str}")
                print(f"Reminder: You have a {entry['course']} class from {entry['start_time']} to {entry['end_time']} on {entry['day']}.")
                return True
    
    print(f"Current day: {current_day}, Current time: {current_time_str}")
    print("No class scheduled at the current time.")
    return False

# Goal-based Agent function
def goal_based_agent(schedule, target_percentage=75):
    for entry in schedule:
        if entry["attendance"] < target_percentage:
            print(f"Reminder: Attend {entry['course']} class to maintain required attendance.")
            return True
    return False

# Example usage
schedule = load_schedule("schedule.csv")
model_based_reflex_agent(schedule)
goal_based_agent(schedule)
