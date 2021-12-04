import datetime as dt
import smtplib as sm
import os
from data_manager import DataManager
email = "your eamil"
passw = "your pass"
#time table fetch
data_manager = DataManager()
QUIZ_DATE = data_manager.time_table()
#MAIL MESSAGE FORMATE
MESSAGE=""
# GENERATING TODAYS DATE USING DAYTIME MODULE
T_DATE = dt.datetime.now().strftime("%d/%m/%Y")
# FINDING IS ANY QUIZ TODAY

if T_DATE in QUIZ_DATE.keys():
    # FETCHING STUDENT FROM Google sheet using sheety api
    detail = data_manager.student_data()
    NO_OF_STUDENTS = len(detail)
    QUIZ_NO = list(QUIZ_DATE.keys()).index(T_DATE)
    with sm.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=passw)
        for i in range(NO_OF_STUDENTS):
            NAME = detail[i]["name"]
            SUB = detail[i]["subject"]
            St_EMAIL = detail[i]["emailAddress"]
            # A list that contain quiz date and time
            QUIZ_TIME = QUIZ_DATE[T_DATE]
            if QUIZ_NO % 2 == 0:
                ENDING = [list(QUIZ_DATE.values())[QUIZ_NO+1],list(QUIZ_DATE.keys())[QUIZ_NO+1]]
                MESSAGE = f"Subject:Prutor {SUB} Quiz {(QUIZ_NO // 2) + 1} live ~ \n\nHey {NAME},\n\nYour Prutor {SUB} " \
                          f"Quiz no. {(QUIZ_NO // 2) + 1} will be Start from today at {QUIZ_TIME}, please Submit" \
                          f" your quiz before {ENDING[0]} till {ENDING[1]}.\n\nthank you."
            else:
                MESSAGE = f"Subject:Prutor {SUB} Quiz {(QUIZ_NO // 2) + 1} live ~ \n\nHey {NAME},\n\nYour Prutor {SUB} " \
                          f"Quiz no. {(QUIZ_NO // 2) + 1} will End today.\nplease Submit" \
                          f" your quiz before {QUIZ_TIME}.\n\nthank you."
            connection.sendmail(from_addr=email,to_addrs=St_EMAIL,msg=MESSAGE)
       # CLEARING OUT EXCEL SHEET AFTER LAST QUIZ
        if QUIZ_NO==19:
            try:
                data_manager.clear_stud(detail1)
                data_manager.clear_time_tab()
                MESSAGE = f"Subject:Your Prutor Notifier Ready to use ~ \n\nHey {NAME},\n\nYour Prutor " \
                              f"Quiz Notifier id ready to use once again.\n\nthank you."
                connection.sendmail(from_addr=email,to_addrs="akarshitgupta29@gmail.com",msg=MESSAGE)
            except:
                with sm.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=email, password=passw)
                    MESSAGE = f"Subject:Prutor System Error \n\nHey {NAME},\n\nYour Prutor " \
                              f"site is not performing well, please fix the ERROR or clear your Google Sheet Manually.\n\nthank you."
                    connection.sendmail(from_addr=email,to_addrs="akarshitgupta29@gmail.com",msg=MESSAGE)




