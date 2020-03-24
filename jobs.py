from apscheduler.schedulers.blocking import BlockingScheduler
from sms_app.send_sms import outgoing_sms, message_the_list, list_of_numbers
from sms_app.models import Number
from sms_app.survey_view import pre_message, post_message

sched = BlockingScheduler()

# Pull Test #s from the DB

alex = Number.query.filter_by(name = 'alex').all()
josh = Number.query.filter_by(name = 'josh').all()
john = Number.query.filter_by(name = 'john').all()

test_group = alex + josh + john

test_numbers = []

for person in test_group:
    test_numbers.append(person.number)

# Just me for testing
alex_numbers = [alex[0].number]

# Pull Students' numbers from the DB
students = Number.query.filter_by(name = 'NA').all()

student_numbers = []

for student in students:
    student_numbers.append(student.number)
    
#print(student_numbers)

### Tests
#@sched.scheduled_job('cron', day_of_week='tue', hour='08', minute='00', timezone='America/New_York')
#def test_message_pre():
#    message_the_list(test_numbers, '+19179949576', pre_message)
    
#@sched.scheduled_job('cron', day_of_week='tue', hour='08', minute='15', timezone='America/New_York')
#def test_message_post():
#    message_the_list(test_numbers, '+19179949576', post_message)       
  
### Real Messages

@sched.scheduled_job('cron', day_of_week='tue', hour='10', minute='30', timezone='America/New_York')
def message_pre():
    message_the_list(student_numbers, '+19179949576', pre_message)
    
@sched.scheduled_job('cron', day_of_week='mon', hour='16', minute='30', timezone='America/New_York')
def message_post():
    message_the_list(student_numbers, '+19179949576', post_message)       
  



        
sched.start()
