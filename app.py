import os
import json
import requests
from flask import Flask, render_template, request

from dialogflow import get_suggestions

app = Flask(__name__)

ZENDESK_SUBDOMAIN = 'your zendesk subdomain'
ZENDESK_API_TOKEN = 'your zendesk api token'

@app.route('/ask_question',methods = ['POST', 'GET'])
def ask_question():
    if request.method == 'POST':
        # Get the issue description from the form data
        description = request.form.get('description')
        # ask dialogflow for suggestions
        articles = get_suggestions(description)
        # render the articles page
        return render_template('articles.html', articles=articles, description=description)

    return render_template('ask_question.html')

@app.route('/contact_form',methods = ['POST', 'GET'])
def contact_form():
    description = ""
    # if POST is called, fill in the description automatically
    if request.method == 'POST':
        description = request.form.get('description')
    return render_template('ticket_form.html', description=description)


@app.route('/create_ticket',methods = ['POST'])
def create_ticket():
    success, feedback = True, None
    # Get the form data
    subject = request.form.get('subject')
    description = request.form.get('description')
    email = request.form.get('email')
    # define the request body
    data = {'request': {'subject': subject, 'comment': {'body': description}}}
    ticket = json.dumps(data)
    # Make the API request to create a new ticket
    user = email + '/token'
    headers = {'content-type': 'application/json'}
    api_url = 'https://' + ZENDESK_SUBDOMAIN + '.zendesk.com/api/v2/requests.json'
    r = requests.post(
        api_url,
        data=ticket,
        auth=(user, ZENDESK_API_TOKEN),
        headers=headers
    )
    if r.status_code != 201:
        success = False
        if r.status_code == 401 or 422:
            feedback = 'Could not authenticate you. Check your email address or register.'
        else:
            feedback = 'Problem with the request. Status ' + str(r.status_code)
    # the feedback template will let the user now about the outcome of this action
    return render_template('feedback.html', success=success, feedback=feedback)

if __name__ == '__main__':
    app.run()
