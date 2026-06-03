import time

import hmac

import hashlib

import requests


API_KEY_ID = "0282a0c3-70af-4521-a595-90cf54d7a654"

SECRET_KEY = "a6305a998a2232e8538cd45e5068ea893483693e879c1ff07b877717ec2a6a0a"


timestamp = str(
    int(time.time())
)

nonce = "abc123"

method = "GET"

path = "/api/partner/test-auth/"

body = ""


message = (

    method
    +
    path
    +
    timestamp
    +
    body

)

signature = hmac.new(

    SECRET_KEY.encode(),

    message.encode(),

    hashlib.sha256

).hexdigest()


headers = {

    "X-API-Key-ID": API_KEY_ID,

    "X-Timestamp": timestamp,

    "X-Nonce": nonce,

    "X-Signature": signature

}


response = requests.get(

    "http://localhost:8000/api/partner/test-auth/",

    headers=headers

)

print(response.status_code)

print(response.json())