import base64
import uuid

class Logger:

    def info(self, message:str):
        print(message)

logger = Logger()

def retry(func, count=5):
    ret, res = func() 
    return ret

def ord_suffix():
    return "_" + base64.b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=\n')

NOTIFICATION_ENABLE = False

def notify(notification:str):
    if NOTIFICATION_ENABLE:
        print(notification)
