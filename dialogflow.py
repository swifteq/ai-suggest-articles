import os
import random
import dialogflow_v2 as dialogflow

# path to the Google API credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="path to your Google API credetials file"

# Google project ID from the agent settings page
PROJECT_ID = "your dialogflow project ID"
# the language your agent is trained on
LANGUAGE_CODE = "en-US"

session_client = dialogflow.SessionsClient()


def get_suggestions(text, session_id=None):
    # if no session, create a random session id (default behaviour)
    if session_id is None:
        session_id = str(random.randint(0, 10000))

    # get the dialogflow session
    session = session_client.session_path(PROJECT_ID, session_id)
    # create a new input using the text description
    text_input = dialogflow.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    # call the Dialogflow API to ask for suggested articles given text in input
    response = session_client.detect_intent(session=session, query_input=query_input)
    result = response.query_result
    # if the matching intent is fallback, no suggested articles were found
    if result.intent.is_fallback or len(result.fulfillment_messages) == 0:
        return None
    # return the list of suggested articles as a list of dict
    articles = []
    for msg in result.fulfillment_messages:
        fields = msg.payload.fields
        articles.append({"url": fields["url"].string_value,
                         "title": fields["title"].string_value,
                         "confidence": result.intent_detection_confidence})

    return articles if len(articles)>0 else None
