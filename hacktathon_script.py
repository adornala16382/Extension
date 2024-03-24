from canvasapi import Canvas
import regex as re
from datetime import datetime
from dateutil import relativedelta
import pytz
from dotenv import load_dotenv
import os

class Canpanion:

    def __init__(self):
        # init
        load_dotenv()
        self.utc = pytz.UTC

        # class_name, late assignments, due assignments
        # for both late assignments and due assignments:
            # due date
            # how long theyre open until

        # Canvas API URL
        API_URL = "https://rutgers.instructure.com"
        # Canvas API key
        API_KEY = os.getenv("CANVAS_SECRET")

        # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)
        self.user = canvas.get_current_user()
        self.courses = self.user.get_courses()

    def __get_active_courses(self, courses):
        # getting current courses
        active_courses = []
        pattern = r"^(\d{4}-\d{2}-\d{2})T.*Z"

        for course in courses:
            try:
                matched = re.search(pattern, course.start_at)
                matched_date = datetime.strptime(matched.group(1), "%Y-%m-%d")
                delta = relativedelta.relativedelta(datetime.now(), matched_date)

                if delta.years >= 1 or (delta.years == 0 and delta.months > 3):
                    continue
                active_courses.append(course)
            except Exception as e:
                # print(e)
                continue
        return active_courses

    def get_active_assignments(self):
        active_courses = self.__get_active_courses(self.courses)

        late_assignments = []
        due_assignments = []

        for course in active_courses:
            cur_active_assignments = course.get_assignments()
            for assignment in cur_active_assignments:
                try:
                    has_submitted = assignment.get_submission(self.user.id).submitted_at

                    if has_submitted is None:
                        class_name = course.name
                        assignment_name = assignment.name
                        assignment_due_date = assignment.due_at_date
                        assignment_id = assignment.id
                        open_until = assignment.lock_at_date

                        if open_until < self.utc.localize(datetime.now()):
                            continue

                        new_entry = {
                            "CLASS_NAME" : class_name,
                            "ASSIGNMENT_NAME": assignment_name,
                            "ASSIGNMENT_ID": assignment_id,
                            "DUE_DATE": assignment_due_date,
                            "OPEN_UNTIL": open_until
                        }

                        if assignment_due_date < self.utc.localize(datetime.now()):
                            late_assignments.append(new_entry)
                        else:
                            due_assignments.append(new_entry)
                except Exception as e:
                    print(e)
                    continue

        late_assignments = sorted(late_assignments, key=lambda x: x["DUE_DATE"])
        due_assignments = sorted(due_assignments, key=lambda x: x["DUE_DATE"])

        for i in range(len(late_assignments)):
            late_assignments[i]["DUE_DATE"] = late_assignments[i]["DUE_DATE"].strftime("%m-%d-%Y, %H:%M:%S")
            late_assignments[i]["OPEN_UNTIL"] = late_assignments[i]["OPEN_UNTIL"].strftime("%m-%d-%Y, %H:%M:%S")

        for i in range(len(due_assignments)):
            due_assignments[i]["DUE_DATE"] = due_assignments[i]["DUE_DATE"].strftime("%m-%d-%Y, %H:%M:%S")
            due_assignments[i]["OPEN_UNTIL"] = due_assignments[i]["OPEN_UNTIL"].strftime("%m-%d-%Y, %H:%M:%S")

        return due_assignments, late_assignments
    
if __name__ == "__main__":
    app = Canpanion()
    due, late = app.get_active_assignments()
    print(late)