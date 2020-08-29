import os
from typing import Union


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"pelican_google_credits.json"


def detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str) -> Union[str, bool]:
    try:
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation."""
        import dialogflow_v2 as dialogflow
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        # print('Session path: {}\n'.format(session))

        #for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        # print('=' * 20)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        # print('Fulfillment text: {}\n'.format(
        #     response.query_result.fulfillment_text))
        
        if response.query_result.fulfillment_text == "":
            return False

        return response.query_result.fulfillment_text
    except:
        return False
