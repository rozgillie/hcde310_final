import urllib.parse, urllib.request, urllib.error, json
from flask import Flask, render_template, request
import pyaztro
import requests



app = Flask(__name__)


def safe_get(url):
    try:
        a = urllib.request.urlopen(url)
        if a.getcode() == 200:
            return a
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


class spotiClient():
    def __init__(self):
        self.accessToken = None
        self.spotifyAuth()

    def spotifyAuth(self):
        from spotify_id import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        import base64
        authorization = base64.standard_b64encode((SPOTIFY_CLIENT_ID +
                                                   ':' + SPOTIFY_CLIENT_SECRET).encode())
        headers = {"Authorization": "Basic " + authorization.decode()}
        params = {"grant_type": "client_credentials"}
        encodedparams = urllib.parse.urlencode(params).encode()
        request = urllib.request.Request(
            'https://accounts.spotify.com/api/token',
            data=encodedparams, headers=headers)
        resp = safe_get(request)
        respdata = json.load(resp)
        self.accessToken = respdata['access_token']

    def apiRequest(self,
                   version="v1",
                   endpoint="search",
                   item=None,
                   params=None, q=None):
        if self.accessToken is None:
            print(
                "Sorry, you must have an access token for this to work.")
            return {}

        baseurl = "https://api.spotify.com/"
        endpointurl = "%s%s/%s" % (baseurl, version, endpoint)

        if item is not None:
            endpointurl = endpointurl + "/" + item
        if params is not None:
            fullurl = endpointurl + "?" + urllib.parse.urlencode(params)

        headers = {"Authorization": "Bearer " + self.accessToken}
        request = urllib.request.Request(fullurl, headers=headers)
        resp = safe_get(request)
        return json.load(resp)


# returns the name of horoscope sign based on users birthday
def get_sign_name(bday):
    url = "https://zodiac-sign.p.rapidapi.com/sign"
    querystring = {"date": bday}
    headers = {
        'x-rapidapi-key': "2db129df32msh8326f7f994b4d7bp168776jsn38211f38cdd2",
        'x-rapidapi-host': "zodiac-sign.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text
# url = "https://zodiac-sign.p.rapidapi.com/sign"
# querystring = {"date": '2000-01-04'}
# headers = {
#     'x-rapidapi-key': "2db129df32msh8326f7f994b4d7bp168776jsn38211f38cdd2",
#     'x-rapidapi-host': "zodiac-sign.p.rapidapi.com"
# }
# u = "https://aztro.sameerkumar.website/" + urllib.parse.urlencode(querystring, headers
# print(u)
# response = urllib.request.Request(url, headers, querystring)
# get = safe_get(response)

# main page
@app.route('/')
def get_information():
    return render_template('template.html')


# results page
@app.route("/forms/notify.php")
def get_response():
    bday = ''
    bday = request.args.get('bday')
    horoscope = pyaztro.Aztro(sign=get_sign_name(bday))
    sign = horoscope.sign.capitalize()
    mood = horoscope.mood
    description = horoscope.description
    response = spotiClient().apiRequest(params={"type": "playlist", "q": mood + "&20music"})
    id = response['playlists']['items'][0]['id']
    src = "https://open.spotify.com/embed/playlist/{}".format(id)
    return render_template('template2.html', src=src, bday=bday, mood=mood, sign=sign, description=description)
