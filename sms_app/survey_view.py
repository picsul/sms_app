from . import app
from .models import Survey
from flask import url_for, session, request
from twilio.twiml.messaging_response import MessagingResponse
from sms_app.send_sms import client
import datetime

pre_message = "Ready to take the CSci 127 pre-class survey? Please respond when you are ready to begin. You will have 5 minutes to complete the survey once you begin, but the survey should only take 1-2 minutes."
post_message = "Ready to take the CSci 127 post-class survey? Please respond when you are ready to begin. You will have 5 minutes to complete the survey once you begin, but the survey should only take 1-2 minutes."

@app.route('/message')
def sms_survey():
    response = MessagingResponse()
    
    now = datetime.datetime.now()
    
    from_num = request.values['From']
    to_num = request.values['To']
       
    messages = client.messages.list(from_=to_num, to=from_num, limit=1)
    message_text = messages[0].body
    
    if message_text == pre_message or message_text == post_message:
        if 'question_id' in session:
            del session['question_id']
        if 'start_time' in session:
            del session['start_time']

    if 'question_id' in session:
        delta = now - session['start_time']
        if delta.seconds > 300:
            del session['start_time']
            del session['question_id']
            response.message("The time to complete the survey has expired")
        else:
            response.redirect(url_for('answer', question_id=session['question_id']))
    else:
        if message_text == pre_message:
            survey = Survey.query.get(1)
            survey_number = 1
        elif message_text == post_message:
            survey = Survey.query.get(2)
            survey_number = 2
        else:
            survey = Survey.query.first()
            survey_number = 1
            
        if survey_error(survey, response.message):
            return str(response)
        
        welcome_user(survey, response.message, survey_number)
        redirect_to_first_question(response, survey)
    return str(response)


def redirect_to_first_question(response, survey):
    first_question = survey.questions.order_by('id').first()
    first_question_url = url_for('question', question_id=first_question.id)
    session['start_time'] = datetime.datetime.now()
    response.redirect(url=first_question_url, method='GET')


def welcome_user(survey, send_function, survey_number):
    if survey_number == 1:
        welcome_text = 'Please only answer these questions if you have consented to participating in the study. Please answer the following three questions about the upcoming week of your computer science class (CSci 127) on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree). Text “STOP” to withdraw from the study.'
    if survey_number == 2:
        welcome_text = 'Please answer the following three questions about the previous week of your computer science class (CSci 127) on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree). Text “STOP” to withdraw from the study.'
    send_function(welcome_text)

def survey_error(survey, send_function):
    if not survey:
        send_function('Sorry, but there are no surveys to be answered.')
        return True
    elif not survey.has_questions:
        send_function('Sorry, there are no questions for this survey.')
        return True
    return False
