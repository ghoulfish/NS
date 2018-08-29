import httplib, urlparse, urllib, sys
from md5p import md5, padding, md5_compress

url = sys.argv[1]
mark = sys.argv[2]

tag = url[url.find("=") + 1:url.rfind("&")]
URL_param = url[url.find("&") + 1:]
msg = "&mark=" + str(mark)

# loop to try key length
for i in range(7, 17):
    l = i + len(URL_param)
    new_tag = md5(state=tag.decode("hex"), count=512)

    new_tag.state = md5_compress(new_tag.state, msg + padding(l + len(padding(l * 8)) + len(msg)) + msg)

    url = url[:url.find("=") + 1] + new_tag.hexdigest() + msg

    # parameter url is the attack url you construct
    parsedURL = urlparse.urlparse(url)

    # open a connection to the server
    httpconn = httplib.HTTPSConnection(parsedURL.hostname)

    # issue server-API request
    httpconn.request("GET", parsedURL.path + "?" + parsedURL.query)

    # httpresp is response object containing a status value and possible message
    httpresp = httpconn.getresponse()

    if httpresp.status == 200:
        # valid request will result in httpresp.status value 200
        print httpresp.status

        # in the case of a valid request, print the server's message
        print httpresp.read()
        break
