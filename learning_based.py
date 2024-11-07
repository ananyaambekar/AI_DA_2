import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression

class LearningAgent:
    def __init__(self, schedule_file, history_file):
        # Load schedule and history data from CSV
        self.schedule = pd.read_csv(schedule_file) 
        self.history = pd.read_csv(history_file)
        
        # Train the model
        self.model = self.train_model()

    def train_model(self):
        # Preprocess the history data and train the model
        if 'Day' in self.history.columns:
            self.history['Start Time'] = self.history['Time'].apply(lambda x: x.split('-')[0])  # Extract start time
            self.history['Start Time'] = self.history['Start Time'].apply(lambda x: int(x.split(':')[0])*60 + int(x.split(':')[1]))  # Convert to minutes

        features = self.history[['Day', 'Start Time', 'Course', 'Crucial']].apply(lambda x: hash(tuple(x)), axis=1).values.reshape(-1, 1)
        labels = self.history['Attended']

        model = LogisticRegression()
        model.fit(features, labels)
        return model

    def notify_class(self):
        # Get the current day and time
        current_day = datetime.now().strftime("%A")
        current_time = datetime.now().strftime("%H:%M")

        # Print the current day and time
        print(f"Current Day: {current_day}, Current Time: {current_time}")
        
        for index, row in self.schedule.iterrows():
            if row['Day'] == current_day and row['Holiday'] == 'No':
                start_time, end_time = row['Time'].split('-')
                if start_time <= current_time <= end_time:
                    feature = hash((current_day, start_time, row['Course'], row['Crucial']))
                    will_attend = self.model.predict([[feature]])[0]
                    if not will_attend:
                        print(f"Reminder: It seems you might miss {row['Course']} today. Consider attending.")
                    else:
                        print(f"No reminder needed for {row['Course']} based on your past attendance.")

    def log_attendance(self, course, attended):
        # Append today's attendance to history
        new_data = {
            'Date': datetime.now().strftime("%Y-%m-%d"),
            'Day': datetime.now().strftime("%A"),
            'Time': datetime.now().strftime("%H:%M"),
            'Course': course,
            'Attended': attended
        }
        self.history = pd.concat([self.history, pd.DataFrame([new_data])], ignore_index=True)
        self.history.to_csv('history_file.csv', index=False)
        self.model = self.train_model()  # Retrain the model with updated data

if __name__ == "__main__":
    schedule_file = 'schedule.csv'  # Adjust file path if needed
    history_file = 'history.csv'    # Adjust file path if needed
    agent = LearningAgent(schedule_file, history_file)
    agent.notify_class()
