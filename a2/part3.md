Because Google and Facebook use HTTPS across their entire site. Data transferred through HTTPS is encrypted, so even the mallory gets to the stream, he won’t be able to read it. SSL/TLS can help the user know that the webpage being served is the same as it was when it left the server.

If mallory perform a SSL Stripping attack, he will try to pretend to be gateway, connect with the victim with HTTP, get all the messages the victim trying to communicate with the server, and send them to the server using HTTPS.

But the problem here is that server like Google and Facebook don’t accept HTTP connection, if the user tries to use HTTP, they will be redirected to HTTPS.
And if the url changes to HTTP, the browser can detect it and tell the user.
So if the user is cautious, he/she can notice the differences.

Therefore the mallory is not able to get the victim’s message and the server’s response using man-in-the-middle attack when the victim is browsing Google or Facebook.
