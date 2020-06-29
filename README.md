# Suggest articles with AI
Smart contact form to deflect customer support tickets with Zendesk and Dialogflow API

## Setup

We recommend Python 3.6 or higher.

Install the following dependencies (preferably in a new virtual env):

`pip install -U flask requests dialogflow`

Clone this repository.

You need a Google Cloud account and a Dialogflow agent with the API enabled. 
Download the Dialog flow credentials file and the agent project ID (see instructions [here](https://cloud.google.com/dialogflow/docs/quick/setup#auth)). 

Configure your Zendesk account in `app.py`

`ZENDESK_SUBDOMAIN = 'your zendesk subdomain'`

`ZENDESK_API_TOKEN = 'your zendesk api token'`

Configure the Google credentials file in `dialogflow.py`:

`os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="path to your Google API credetials file"`


Run the tutorial using the command below from the main project folder:

`python app.py`

Open http://127.0.0.1:5001/ask_question and start playing!