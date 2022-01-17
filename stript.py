import requests
import json
import time
import re
token = "5063650210:AAHP4HCU4UkzdG7htxKsczHFKxuN4y9V7sM"
url = "https://api.telegram.org/bot{}/".format(token)
name = "@forwardscoverbotbot"

def get_msg():
    url_getUpdates = url+"getUpdates"
    #print(url_getUpdates)
    ctn =requests.post(url_getUpdates).text
    msg = json.loads(ctn)
    #update_id = msg["result"][-1]["update_id"]
    return msg

#最新的update_id
#update_id=msg["result"][-1]["update_id"]
def get_tg_msg_offset(msg):
    update_id=msg["result"][-1]["update_id"]
    url_getUpdates = url+"getUpdates"+"?offset="+str(update_id-10)#只保留10条，单条信息最多10条
    #print(url_getUpdates)
    ctn =requests.post(url_getUpdates).text
    msg = json.loads(ctn)
    return msg

#msg = get_tg_msg_offset(get_msg())
def dis_user_msg_test(msg,num):
    message=msg["result"][num]["message"] # 只处理 单个 信息
    alist = list(message)
    adict = {}
    if "forward_from_chat" in alist:
        adict["forward_from_chat"]=message["forward_from_chat"]["id"]
    if "forward_from" in alist:
        adict["forward_from_id"]=message["forward_from"]["id"]
    if "text" in alist:
        adict["text"]=msg["result"][num]["message"]["text"]
    if "caption" in alist:
        adict["caption"]=msg["result"][num]["message"]["caption"]
    if "chat" in alist:
        adict["chat_id"]=msg["result"][num]["message"]["chat"]["id"]
    if 'photo' in alist:
        if("phote" in adict):
            clist = adict["photo"]
            file_id = msg["result"][num]["message"]["photo"][0]["file_id"]
            clist.append(file_id)
            adict["photo"]=clist
        else:
            clist = []
            file_id = msg["result"][num]["message"]["photo"][0]["file_id"]
            clist.append(file_id)
            adict["photo"]=clist
    if 'video' in alist:
        if("video" in adict):
            clist = adict["video"]
            file_id = msg["result"][num]["message"]["video"]["thumb"]["file_id"]
            clist.append(file_id)
            adict["video"]=clist
        else:
            clist = []
            file_id = msg["result"][num]["message"]["video"]["thumb"]["file_id"]
            clist.append(file_id)
            adict["video"]=clist
    return adict

def get_msg_num(msg):
    num = 0
    media_group_id=0
    alist = list(msg["result"][-1]["message"])
    clist = []
    if("media_group_id" not in alist):
        return 1
    else:
        for i in range(1,11):
            #print(i)
            blist = list(msg["result"][-i]["message"])
            if("media_group_id" in blist):

                media_group_id = msg["result"][-i]["message"]["media_group_id"]
                clist.append(media_group_id)
                #print(clist)
    
    return clist.count(clist[0])


def dis_user_msg_most(msg,msg_num):
    rdict = {'chat_id':"-1", 'photo': [], 'caption': '', 'video': [],"text":"","forward_from_id":""}
    for i in range(-1,-(msg_num+1),-1):
        adict = dis_user_msg_test(msg,i)
        alist = list(adict)
        #print(alist)
        if("forward_from_id" in alist):
            rdict["forward_from_id"]=adict["forward_from_id"]
        if("forward_from_chat" in alist):
            rdict["forward_from_chat"]=adict["forward_from_chat"]
        if("text" in alist):
            rdict["text"]=adict["text"]
        if("chat_id" in alist):
            rdict["chat_id"]=adict["chat_id"]
        if("caption" in alist):
            rdict["caption"]=adict["caption"]
        if("photo" in alist):
            blist = rdict["photo"]
            blist.append(adict["photo"][0])
            rdict["photo"]=blist
        if("video" in alist):
            blist = rdict["video"]
            blist.append(adict["video"][0])
            #print(blist)
            rdict["video"]=blist
            
    return rdict
#msg = get_tg_msg_offset(get_msg())
#msg_num = get_msg_num(msg)
#print(dis_user_msg_most(msg,msg_num))



def send_tg_msg(data={}):
    ctn=requests.post(url,data=data)
    ctn = ctn.text
    ctn = json.loads(ctn)
    if(ctn["ok"]==1):
        print("发送成功")
    else:
        print("发送失败")
        print(ctn)

msg = get_tg_msg_offset(get_msg())
def main():
    print("name:{},token:{}".format(name,token))
    msg = get_tg_msg_offset(get_msg())
    date = msg["result"][-1]["message"]["date"]
    while(1):
        msg = get_tg_msg_offset(get_msg())
        new_date = msg["result"][-1]["message"]["date"]
        if(new_date == date):
            time.sleep(0.01)
        else:
            date = new_date
            msg_num = get_msg_num(msg)
            text = dis_user_msg_most(msg,msg_num)
            data = {"method": "sendMessage",
            "chat_id": text["chat_id"],
            "text":str(text)}
            send_tg_msg(data)

main()          
    



