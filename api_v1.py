import uuid
import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
from utils import file_id

CLIENT_ID = st.secrets["CLIENT_ID"]
SECRET_KEY = st.secrets["SECRET_KEY"]


def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
    }
    payload = {"scope": "GIGACHAT_API_PERS"}
    response = requests.post(
        url=url,
        headers=headers,
        auth=HTTPBasicAuth(CLIENT_ID, SECRET_KEY),
        data=payload,
        verify=False,
    )
    access_token = response.json()["access_token"]
    return access_token


def get_image(file_id: str, access_token: str):
    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{file_id}/content"
    headers = {"Accept": "image/jpg", "Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.content


def send_message(message: str, access_token: str) -> str:
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": message,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["content"]


def sent_get_response(message: str, access_token: str) -> tuple[str, bool]:
    res = send_message(message, access_token)
    data, is_image = file_id(res)
    return data, is_image
