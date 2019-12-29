import fake_useragent
import os
curr = os.getcwd()
location = curr+'\\fake_useragent%s.json' % fake_useragent.VERSION

def getFakeUA():
    ua = fake_useragent.UserAgent(path=location)
    # print(ua.random)
    return ua.random    