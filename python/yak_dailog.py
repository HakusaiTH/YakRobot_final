import os
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'joshu-2-0-iypf'
DIALOGFLOW_LANGUAGE_CODE = 'th'
SESSION_ID = 'me'

# Define intent constants
INTENT_IOT_SL = "iot sl"
INTENT_WEATHER = "สภาพอากาศ"
INTENT_PM25 = "pm25"

INTENT_CALL_YAK = "call yak"
INTENT_CALL_GPT = "call gpt"

def detect_intent(text_to_be_analyzed):
    client = dialogflow.SessionsClient()
    session = client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = client.detect_intent(request={"session": session, "query_input": query_input})
    except InvalidArgument:
        raise

    re_intent = response.query_result.intent.display_name

    if re_intent == INTENT_CALL_GPT:
        return "gpt"
    elif re_intent == INTENT_IOT_SL:
        return handle_iot_intent(response)
    elif re_intent == INTENT_WEATHER:
        return "สภาพอากาศ"
    elif re_intent == INTENT_PM25:
        return "pm25"

def handle_iot_intent(response):
    action = response.query_result.action
    parameters = response.query_result.parameters

    value = parameters.get('value', None)
    sta = parameters.get('sta', None)

    return [value, sta]
