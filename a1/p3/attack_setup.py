from md5p import md5, padding
import struct

# Let's have
# Alice (the TA)
# Bob (the grade server)
# Mallory (the bad guy a.k.a you)
# Alice and Bob share a secret key but Mallory does not know it

# The code below is an accurate simulation of how the client (Alice)
# and the server (Bob) computes and verifies the tag (a.k.a MAC)

def B(tag, params):
    '''returns true/false whether the tag is valid given the params'''
    key = "secret"
    return md5(key + params).hexdigest() == tag

def A(params):
    '''returns true/false whether Alice sends the correct params and tag to the server'''
    key = "secret"
    tag = md5(key + params).hexdigest()
    return B(tag, params)

def M(params):
    '''returns true/false whether Mallory sends the correct tag and params to the server'''
    # Mallory does not know the key
    # but she knows one specific tag, the one resulting from md5("secret" + "show me the grade")
    tag = "9f4bb32ac843d6db979ababa2949cb52"
    new_tag = md5(state=tag.decode("hex"), count=512)
    new_tag.update(padding(2*8))
    new_tag.update(" and change it to 100")
    return B(new_tag, params)

# this returns true because Alice is able to compute the correct tag given these params
print(A("show me the grade"))
# this returns true because Alice is able to compute the correct tag given these params
print(A("show me the grade and change it to 100"))


# this returns true because Mallory knows the correct tag given these params
print(M("show me the grade"))
# this returns false because Mallory does not know the correct tag given these params
print(M("show me the grade and change it to 100"))
# and your job is to make it otherwise without modfying A or B but M only




print("----------------------------------")

k = "secret"
m = "show me the grade"
m2 = "show me the grade and change it to 100"
a = md5(k + m)
b = md5(k + m2)
print "1---> " + a.hexdigest()
print "2---> " + b.hexdigest()
h = md5(state="9f4bb32ac843d6db979ababa2949cb52".decode("hex"),count=512)
print h.hexdigest()
x = " and change it to 100"
h.update(x)
print h.hexdigest()
print md5((k + m + padding(len(k + m)*8))+ x).hexdigest()


print("----------------------------------")
def compute_magic_number(md5str):
    A = struct.unpack("I", md5str[0:8].decode('hex'))[0]
    B = struct.unpack("I", md5str[8:16].decode('hex'))[0]
    C = struct.unpack("I", md5str[16:24].decode('hex'))[0]
    D = struct.unpack("I", md5str[24:32].decode('hex'))[0]
    return A, B, C, D




print("----------------------------------")
a=md5()
a.state = compute_magic_number("9f4bb32ac843d6db979ababa2949cb52")
b=padding(len(x))
c=padding(len(k+m)*8)