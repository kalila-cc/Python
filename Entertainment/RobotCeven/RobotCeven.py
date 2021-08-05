# -*- coding: utf-8 -*-

import itchat
from itchat.content import TEXT, ATTACHMENT
from random import sample


flag, this, that = {}, {}, {}
idict = [idiom[:-1] for idiom in open("./config/idioms.txt", "r", encoding="utf-8").readlines() if len(idiom) > 2]


@itchat.msg_register([TEXT])
def text_reply(msg):
    global flag, this, that, idict
    fm, tt, = msg["FromUserName"], msg["Text"]
    if flag.get(str(fm), True):
        itchat.send("你好吖╰(￣▽￣)╭，我是cc的robot，叫我Ceven就好啦！", fm)
        flag[str(fm)] = False
    elif "#领养Ceven" == str(tt):
        try:
            itchat.send_file("./config/WeChat_Ceven_dir.zip", fm)
        except:
            itchat.send("Sorry，Ceven不在源文件持有者手上，没办法去你那里玩了噢(⊙o⊙)", fm)
    elif "#使用说明" == str(tt):
        itchat.send_image("config\\intro.jpg", fm)
    elif "#" in str(tt):
        that[str(fm)] = str(tt)[1:]
        if that[str(fm)] == "成语接龙":
            this[str(fm)] = sample(idict, 1)[0]
            itchat.send("Ceven跟你玩个简单的成语接龙游戏吧ヾ(^▽^*)\n试试接下这个成语如何？\n%s"%(this[str(fm)]), fm)
        elif that[str(fm)] in idict and that[str(fm)][0] == this[str(fm)][-1]:
            itchat.send("接的漂亮，继续继续！\n(⊙ˍ⊙)，先让我找找成语哈。。", fm)
            temp = ""
            try:
                temp = [idiom for idiom in idict if idiom[0] == that[str(fm)][-1]][0]
            except:
                pass
            if temp != "":
                itchat.send("试试这个：{}".format(temp), fm)
                this[str(fm)] = temp
            else:
                itchat.send("Ceven词穷了。。。下次再来，溜了溜了✧٩(ˊωˋ*)و", fm)
        else:
            itchat.send("呵，人类，再去练练吧 (▼ヘ▼#)，Ceven不跟没水平的人类玩", fm)
    else:
        itchat.send("Ceven收到了你的信息 : {}".format(tt), fm)


@itchat.msg_register([ATTACHMENT])
def download_file(msg):
    msg["Text"](msg["FileName"])


if __name__ == '__main__':
    itchat.auto_login()
    itchat.run()
