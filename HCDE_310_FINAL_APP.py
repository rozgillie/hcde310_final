import urllib.parse, urllib.request, urllib.error, json
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import pyaztro
horoscope = pyaztro.Aztro(sign='capricorn')

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

#initial request of URL
def get_url_info(url):
    r = urllib.request.Request(url)
    get = safe_get(r)
    if get is not None:
        return json.load(get)
    
print(horoscope.mood)
print(horoscope.current_date)
