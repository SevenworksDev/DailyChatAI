import time,base64,hashlib,requests,os,markovify
from itertools import cycle

print("Starting...")
with open("models/SevenworksDailyChat_600K.txt") as f:
    text = f.read()

print("Building AI Model...")
text_model = markovify.Text(text)

def comment_chk(*,username,comment,levelid,percentage,type):
	part_1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
	return base64.b64encode(xor(hashlib.sha1(part_1.encode()).hexdigest(),"29481").encode()).decode()
def xor(data, key):
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
def gjp_encrypt(data):
	return base64.b64encode(xor(data,"37526").encode()).decode()
def gjp_decrypt(data):
	return xor(base64.b64decode(data.encode()).decode(),"37526")

def getGJUsers(target):
    data={
        "secret":"Wmfd2893gb7",
        "str":target
    }
    request =  requests.post("http://www.boomlings.com/database/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)

def uploadGJComment(name,passw,comment,perc,level):
        try:
                accountid = getGJUsers(name)[1]
                gjp = gjp_encrypt(passw)
                c = base64.b64encode(comment.encode()).decode()
                chk = comment_chk(username=name,comment=c,levelid=str(level),percentage=perc,type="0")
                data={
                    "secret":"Wmfd2893gb7",
                    "accountID":accountid,
                    "gjp":gjp,
                    "userName":name,
                    "comment":c,
                    "levelID":level,
                    "percent":perc,
                    "chk":chk
                }
                return requests.post("http://www.boomlings.com/database/uploadGJComment21.php",data=data,headers={"User-Agent": ""}).text
        except:
                return "problem"


un = input("Username: ")
pw = input(f"Password to {un}: ")
lvlid = input("Level ID: ") # TODO: fetch automatically

def PostComment(commentText):
    uploadGJComment(un,pw,commentText,"0",lvlid)

while True:
  try:
    com = text_model.make_short_sentence(70)
    if com:
      PostComment(com)
      time.sleep(15)
    else:
      pass
  except:
    pass
