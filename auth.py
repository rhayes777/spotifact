import base64
import json
from urllib import request as r

import requests
from flask import Flask, request, redirect, jsonify


app = Flask(__name__)

CREDENTIALS_FILE = "credentials.json"

#  Client Keys
CLIENT_ID = "5b236ca2ef774c849b57ec576ab1f2fa"
CLIENT_SECRET = "861b372b9996407a931fff37d5a34e77"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_ENDPOINT = "/callback/q"
REDIRECT_URI = "{}:{}{}".format(CLIENT_SIDE_URL, PORT, REDIRECT_ENDPOINT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, r.quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route(REDIRECT_ENDPOINT)
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    with open(CREDENTIALS_FILE, "w+") as f:
        f.write(post_request.text)

    response_data = json.loads(post_request.text)
    return jsonify(response_data)


    # access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]
    #
    # # Auth Step 6: Use the access token to access Spotify API
    # authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    #
    # # Get profile data
    # user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    # profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    # profile_data = json.loads(profile_response.text)
    #
    # # Get user playlist data
    # playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    # playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    # playlist_data = json.loads(playlists_response.text)
    #
    # # Combine profile and playlist data to display
    # display_arr = [profile_data] + playlist_data["items"]



if __name__ == "__main__":
    app.run(debug=True, port=PORT)
