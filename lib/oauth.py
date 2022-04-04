#!/usr/bin/env python3

import requests

def request_oauth_token(url, client_id, client_secret, audience):
    """
    retrieve an OAuth access token using a shared secret
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_payload = {
        'grant_type':    'client_credentials',
        'audience':      audience,
        'client_id':     client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=auth_payload)

    if response.status_code != requests.codes.ok:
        raise Exception(f"Error authenticating to Wiz [{response.status_code}] - {response.text}")
    try:
        response_json = response.json()
        token = response_json.get('access_token')
        if not token:
            message = f"Could not retrieve token from Wiz: {response_json.get('message')}"
            raise Exception(message)
    except ValueError as exception:
        print(exception)
        raise Exception("Could not parse API response")
    return token
