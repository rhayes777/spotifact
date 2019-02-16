import json

import requests

import config

with open(config.CREDENTIALS_FILE) as f:
    access_token = json.loads(f.read())["access_token"]

authorization_header = {"Authorization": "Bearer {}".format(access_token)}


def make_request(endpoint):
    response = requests.get(endpoint, headers=authorization_header)
    return json.loads(response.text)


def pprint(response_dict):
    print(json.dumps(response_dict, indent=4))


user_profile_api_endpoint = "{}/me".format(config.SPOTIFY_API_URL)
profile_data = make_request(user_profile_api_endpoint)

playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
playlist_data = make_request(playlist_api_endpoint)

pprint(playlist_data)


"""
{
    "collaborative": false,
    "external_urls": {
        "spotify": "https://open.spotify.com/playlist/0uDn2TE7eouHnAZPHLXtF7"
    },
    "href": "https://api.spotify.com/v1/playlists/0uDn2TE7eouHnAZPHLXtF7",
    "id": "0uDn2TE7eouHnAZPHLXtF7",
    "images": [
        {
            "height": null,
            "url": "https://pl.scdn.co/images/pl/default/cc5e818ac8330461fafc532a690d0f93463d85a6",
            "width": null
        }
    ],
    "name": "Watford Gap (Service station archives)",
    "owner": {
        "display_name": "amsilverwood",
        "external_urls": {
            "spotify": "https://open.spotify.com/user/amsilverwood"
        },
        "href": "https://api.spotify.com/v1/users/amsilverwood",
        "id": "amsilverwood",
        "type": "user",
        "uri": "spotify:user:amsilverwood"
    },
    "primary_color": null,
    "public": true,
    "snapshot_id": "MTMxLDgzZTU3YTFjM2ZlNmQyOTVhYTMxMGIyNmQ4YTU0YWI4ZTUwMTYzYzM=",
    "tracks": {
        "href": "https://api.spotify.com/v1/playlists/0uDn2TE7eouHnAZPHLXtF7/tracks",
        "total": 1002
    },
    "type": "playlist",
            "uri": "spotify:user:amsilverwood:playlist:0uDn2TE7eouHnAZPHLXtF7"
}
"""
