import json
import os
from agents.mailing import draft_email
from agents.scheduling import create_event
from agents.clarify import search_google
from dotenv import load_dotenv
import subprocess

load_dotenv()

USER_EMAIL = os.environ["USER_EMAIL"]

def send_notification(message, title="Notification Title"):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def handle_response(response: str):
    json_response = json.loads(response)
    if json_response['action'] == 'email':
        draft_email(json_response['recipient'], json_response['subject'], json_response['body'], USER_EMAIL)
        send_notification("Email drafted to " + json_response['recipient'] + " regarding " + json_response["subject"], "Email Drafted")

    elif json_response['action'] == 'schedule':
        create_event(json_response['attendeeEmails'], json_response['startTime'], json_response['title'], json_response["description"])
        send_notification(json_response["Title"] + " scheduled with " + json_response['attendeeEmails'] + " at " + json_response["startTime"], "Event Scheduled")

    elif json_response['action'] == 'clarify':
        if json_response['result'] != "NONE":
            send_notification(json_response['response'], "Quick Inisght")
        else:
            send_notification(search_google(json_response['search_query']), "More Info")
