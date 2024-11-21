from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import os

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def get_firebase_access_token():
    """
    Generates an access token for Firebase Cloud Messaging API using the service account file.
    """
    credentials = service_account.Credentials.from_service_account_file(
    os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH'),
    scopes=SCOPES
)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def send_firebase_notification(fcm_token, title, body):
    """
    Sends a notification via Firebase Cloud Messaging HTTP v1 API.
    """
    url = "https://fcm.googleapis.com/v1/projects/hotelcrew-7f89e/messages:send"  # Replace with your project ID

    payload = {
        "message": {
            "token": fcm_token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    access_token = get_firebase_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
