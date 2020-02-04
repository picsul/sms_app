from apscheduler.schedulers.blocking import BlockingScheduler
from sms_app.send_sms import outgoing_sms, message_the_list, list_of_numbers, message_the_list_unique

sched = BlockingScheduler()

usc_numbers = ['+18652361445', '+12022588130', '+18186205367', '+18593947313', '+15172400923']
picsul_numbers = ['+15172400923', '+18652361445']

@sched.scheduled_job('cron', day_of_week='mon', hour='17', minute='00', timezone='US/Eastern')
def eastern_message():
    message_the_list(picsul_numbers, "Hey")
   
sched.start()
