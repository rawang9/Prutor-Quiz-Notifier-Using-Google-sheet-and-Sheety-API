import requests

students = "Your endpoint"
timetable = "your sheety endpoint"
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def _init_(self):
        self.student_d = {}
        self.ddmmyy = {}
    def student_data(self):
        request = requests.get(url=students)
        data = request.json()
        self.student_d = data["students"]
        return self.student_d
    def timer(self,time_formate):
         hour = int(time_formate[:2])
         if hour==0:
              return f"12{time_formate[2:]} AM"
         elif hour==12:
              return f"12{time_formate[2:]} PM"
         elif hour<12:
              return time_formate+" AM"
         elif hour>12:
              return f"{hour-12}{time_formate[2:]} PM"
    def time_table(self):
        req = requests.get(url=timetable)
        json_now = req.json()
        fetched_time  = json_now["timeTable"][0]
        date_and_time = []
        for quiz_list in fetched_time.keys():
             if "quiz" in quiz_list:
                  date_and_time.append(fetched_time[quiz_list].split())
        formated_data = {}
        for timing in date_and_time:
            timing[1] = self.timer(timing[1])
            formated_data[timing[0]] = timing[1]
        self.ddmmyy = formated_data
        return self.ddmmyy
    def clear_stud(self,details):
        for entry in details[::-1]:
            new_data = entry
            respons = requests.delete(url=f"{students}/{new_data['id']}"
                                      ,json=new_data)
    def clear_time_tab(self):
        rqst = requests.get(url=timetable)
        json_form = rqst.json()
        fetched = json_form["timeTable"][0]
        respons = requests.delete(url=f"{timetable}/{fetched['id']}",json=fetched)



