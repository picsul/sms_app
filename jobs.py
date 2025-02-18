from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sms_app.send_sms import outgoing_sms, message_the_list, message_the_list_unique
from sms_app.models import Number
import datetime
from sms_app import app, db 
from sms_app.config import confi
import os
import tomllib

# jobstores = {
#     'default': SQLAlchemyJobStore(url=os.environ.get('DATABASE_URL'))
# }
# 
# sched = BlockingScheduler(jobstores = jobstores)

sched = BlockingScheduler()

survey_prompt = confi['survey_prompt']
phone_number = confi['phone_number']

datetimes = ["tue 15:39", "wed 12:20", "fri 12:20", "tue 11:00", "thu 11:00", "tue 12:35", "thu 12:35", "tue 14:10", "thu 14:10"]

split_list = [x.split(" ") for x in datetimes]
days = [el[0] for el in split_list]

times = [el[1] for el in split_list]
split_times = [x.split(":") for x in times]
hours = [el[0] for el in split_times]
mins = [el[1] for el in split_times]

codes = ["M1220", "W1220", "F1220", "T1100", "R1100", "T1235", "R1235", "T1410", "R1410"]

# create list of beginning of week times to index the weeks
base = datetime.datetime(2023, 5, 21, 1,1,1)
date_list = [base + datetime.timedelta(weeks=x) for x in range(13)]

# count which week we are in by comparing a time to the beginning of week times list
def week_check(time):
    diffs = []
    for i in range(0, len(date_list)):
        if time > date_list[i]:
            diffs.append(1)
        else:
            diffs.append(0)
    return str(sum(diffs))

# create a cron job to send a message to a subset of people dependent on the week
def send_message(day, hour, minute, code):
    @sched.scheduled_job('cron', day_of_week=day, hour=hour, minute=minute, timezone='America/New_York')
    def message_job():    
        with app.app_context():
            # figure out which week we're in when job runs
            now = datetime.datetime.today()
            week = week_check(now)
            # get the right people for that week
            people = Number.query.filter(Number.week == week, Number.code.contains(code)).all()        
            # pull out their numbers
            message_numbers = [x.number for x in people]
            # send the surveys
            message_the_list(message_numbers, survey_prompt, phone_number)  
        
# create the cron jobs for each unique datetime
for i in range(0,len(datetimes)):
    send_message(days[i], hours[i], mins[i], codes[i])

sched.start()
