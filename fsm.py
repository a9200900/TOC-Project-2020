from transitions.extensions import GraphMachine
import os
import random
from utils import send_text_message
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage)
from linebot import LineBotApi, WebhookParser

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
name = ''
occupation = ''
health_max = 0
health_now =0
health_body=0
health_equip=0
attack = 0 
attak_body=0
attack_equip=0
defense = 0
defense_body =0
defense_equip=0
level = 1
exp = 0
money = 0
backpack = []
equipment = []
attribute = [["普通大劍" , "0" ,"1","1","武器"] ,["短杖","0","1","1","武器"] ,["短弓","0","1","1","武器"] ,["破舊的大衣","1","0","1","防具"],
["初級魔法袍","1","0","1","防具"],["簡陋的衣裝","1","0","1","防具"],["鋒利的彎刀","1","2","1","武器"],["鎖子甲","3","0","1","防具"],["精緻魔杖","1","2","1","武器"],
["上等法袍","3","0","1","防具"],["骨製彎曲弓","1","2","1","武器"],["上等絲綢服","3","0","1","防具"],["角龍大劍","2","3","1","武器"],["女巫法書","2","3","1","武器"],
["角龍弓","2","3","1","武器"],["兇財龍套裝","5","1","2","防具"],["雷狼龍魔劍","4","5","2","武器"],["雷狼龍魔杖","4","5","2","武器"],["雷狼龍魔弓","4","5","2","武器"],
["泥魚龍套裝","7","2","3","防具"],["滅盡龍太刀","5","6","3","武器"],["滅盡龍魔書","5","6","3","武器"],["滅盡龍弓","5","6","3","武器"],["蒼火龍防具","6","1","3","防具"],
["炎王龍雙刀","6","7","4","武器"],["炎王龍火杖","6","7","4","武器"],["炎王龍火弓","6","7","4","武器"],["鋼龍套服","10","2","5","防具"]] 
monster_1 =[["哥布林","5","3","1","2"],["奇面族","8","2","5","2"],["女巫","5","3","2","2"],["騷鳥","5","2","5","2"],["凶豺龍","10","5","3","2"],
["雷狼龍","3","8","1","2"],["眩鳥","8","2","5","2"],["土沙龍","10","2","2","2"],["泥魚龍","6","2","4","2"],["神秘龍人","8","2","5","2"]] 
monster_2 =[["地精長老","8","3","1","10"],["毒妖鳥","9","5","5","10"],["火龍","9","5","10","10"],["雌火龍","10","4","5","10"],["櫻火龍","10","5","3","10"],
["蒼火龍","8","8","1","10"],["角龍","8","10","5","10"],["黑角龍","10","10","6","10"],["浮空龍","8","6","5","10"],["風漂龍","8","4","5","10"]]
monster_3 =[["痺賊龍","12","8","10","20"],["麒麟","12","8","8","20"],["鋼龍","15","8","8","20"],["炎王龍","15","16","10","20"],["炎妃龍","15","15","13","20"],
["滅盡龍","13","18","10","20"],["熔山龍","18","20","8","20"],["屍套龍","13","20","20","20"],["恐暴龍","18","20","8","20"],["蠻顎龍","18","20","9","20"]]
monster_url = [
    ["哥布林","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%93%A5%E5%B8%83%E6%9E%97.png"],
    ["奇面族","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%85%B6%E9%BA%B5%E6%97%8F.jpg"],
    ["女巫","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%A5%B3%E5%B7%AB.png"],
    ["騷鳥","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E8%89%98%E9%B3%A5.jpg"],
    ["凶豺龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%85%87%E8%B2%A1%E9%9A%86.png"],
    ["雷狼龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%9B%B7%E9%83%8E%E9%BE%8D.png"],
    ["眩鳥","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E7%9C%A9%E9%B3%A5.png"],
    ["土沙龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%9C%9F%E6%B2%99%E9%BE%8D.png"],
    ["泥魚龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%B3%A5%E6%96%BC%E9%9A%86.jpg"],
    ["神秘龍人","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E7%A5%9E%E7%A7%98%E8%81%BE%E4%BA%BA.png"],
    ["地精長老","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%9C%B0%E7%B2%BE%E9%95%B7%E8%80%81.png"],
    ["毒妖鳥","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%AF%92%E9%82%80%E9%B3%A5.png"],
    ["火龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E7%81%AB%E9%BE%8D.jpg"],
    ["雌火龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%9B%8C%E7%81%AB%E9%BE%8D.png"],
    ["櫻火龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%87%89%E7%81%AB%E9%BE%8D.jpg"],
    ["蒼火龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%80%89%E7%81%AB%E9%BE%8D.jpg"],
    ["角龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E8%A7%92%E9%BE%8D.png"],
    ["黑角龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%BB%91%E8%A7%92%E9%BE%8D.png"],
    ["浮空龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%9C%8D%E7%A9%BA%E9%BE%8D.jpg"],
    ["風漂龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%A2%A8%E9%A3%84%E9%BE%8D.png"],
    ["痺賊龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%BF%85%E8%B3%8A%E9%BE%8D.jpg"],
    ["麒麟","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%BA%92%E9%BA%9F.jpg"],
    ["鋼龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%89%9B%E9%BE%8D.jpg"],
    ["炎王龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%96%BB%E7%8E%8B%E9%BE%8D.jpg"],
    ["炎妃龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%BB%B6%E9%A3%9B%E9%BE%8D.png"],
    ["滅盡龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%BB%85%E9%80%B2%E9%9A%86.jpg"],
    ["熔山龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%AE%B9%E6%9D%89%E9%BE%8D.jpg"],
    ["屍套龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%B8%AB%E5%A5%97%E9%BE%8D.jpg"],
    ["恐暴龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E6%81%90%E6%9A%B4%E9%BE%8D.jpg"],
    ["蠻顎龍","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E9%B0%BB%E6%83%A1%E9%BE%8D.png"]
]
monster_now = []
monster_now_url=""
monster_now_count = -1
map = [["新手鎮","休息"],["幽靜小路","戰鬥"],["被詛咒的沼澤","戰鬥"],["山洞","戰鬥"],["市集","商店"]]
map_1 = [["古代樹之森","戰鬥"],["大蟻塚荒地","戰鬥"],["北東營地","商店"],["幽靜小路","戰鬥"],["被詛咒的沼澤","戰鬥"],["山洞","戰鬥"]]
map_2 = [["瘴氣之谷","戰鬥"],["東營地","商店"],["陸珊瑚台地","戰鬥"],["邪魔神之地","戰鬥"],["岩漿地區","戰鬥"],["魔物巢穴","戰鬥"]]
map_3 = [["龍結晶之地","戰鬥"],["星辰據點","商店"],["永霜凍土","戰鬥"],["雪山洞穴","戰鬥"],["沙漠山丘","戰鬥"],["強風之古","戰鬥"]]
map_now = ""
map_now_count = -1
drops = [["狂戰士","鋒利的彎刀","鎖子甲","角龍大劍","兇財龍套裝","雷狼龍魔劍","泥魚龍套裝","滅盡龍太刀","蒼火龍防具","炎王龍雙刀","鋼龍套服"] ,
 ["黑暗法師","精緻魔杖","上等法袍","女巫法書","兇財龍套裝","雷狼龍魔杖","泥魚龍套裝","滅盡龍魔書","蒼火龍防具","炎王龍火杖","鋼龍套服"] 
 , ["精靈射手","骨製彎曲弓","上等絲綢服","角龍弓","兇財龍套裝","雷狼龍魔弓","泥魚龍套裝","滅盡龍弓","蒼火龍防具","炎王龍火弓","鋼龍套服"]]
drop_1_sword =["鋒利的彎刀","鎖子甲","角龍大劍","兇財龍套裝"]
drop_2_sword = ["雷狼龍魔劍","泥魚龍套裝","滅盡龍太刀","蒼火龍防具"]
drop_3_sword =["炎王龍雙刀","鋼龍套服"]
drop_1_magic =["精緻魔杖","上等法袍","女巫法書","兇財龍套裝"]
drop_2_magic = ["雷狼龍魔杖","泥魚龍套裝","滅盡龍魔書","蒼火龍防具"]
drop_3_magic = ["炎王龍火杖","鋼龍套服"]
drop_1_arch = ["骨製彎曲弓","上等絲綢服","角龍弓","兇財龍套裝"]
drop_2_arch = ["雷狼龍魔弓","泥魚龍套裝","滅盡龍弓","蒼火龍防具"]
drop_3_arch = ["炎王龍火弓","鋼龍套服"]
attribute_for_health=0
attribute_for_health_equip=0
attribute_for_health_weapon=0
using_item=[]

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def introduce(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使:現在是魔王曆128年,自從上一位勇者犧牲已經100多年了，沒有人能夠與現在的魔王抗衡，希望勇者您能幫助我們打到魔王!") 
    def on_enter_intro(self , event):

        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '無盡天使:歡迎來到這個世界，你一定是上帝派來拯救我們的勇者，請你幫助我們打到大魔王『黑龍』!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '人物介紹',
                                        text = '人物介紹'
                                    ),
                                    MessageTemplateAction(
                                        label = '開始冒險',
                                        text = '開始冒險'
                                    )
                                ]
                            )
                        )
                    )
    def line_buttons_intro(self,event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '無盡天使:歡迎來到這個世界，你一定是上帝派來拯救我們的勇者，請你幫助我們打到大魔王『斯巴拉斯．魔迪耶爾』!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '人物介紹',
                                        text = '人物介紹'
                                    ),
                                    MessageTemplateAction(
                                        label = '開始冒險',
                                        text = '開始冒險'
                                    )
                                ]
                            )
                        )
                    )

    def on_enter_build(self , event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '建立角色',
                                text = '無盡天使:請依序輸入您的大名，以及想要遊玩的職業。輸入完後點擊完成，開始冒險。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '設定名稱',
                                        text = '設定名稱'
                                    ),
                                    MessageTemplateAction(
                                        label = '選擇職業',
                                        text = '選擇職業'
                                    ),
                                    MessageTemplateAction(
                                        label = '完成',
                                        text = '完成'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        )
                    )
    def check_build(self,event):
        flag = False
        global occupation,name
        if occupation !="" :
            if name != "" :
                flag = True

        return flag
    def on_enter_start(self , event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '踏上旅程，在前方是未知的道路!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '前進',
                                        text = '前進'
                                    ),
                                    MessageTemplateAction(
                                        label = '背包',
                                        text = '背包'
                                    ),
                                    MessageTemplateAction(
                                        label = '地圖',
                                        text = '地圖'
                                    ),
                                    MessageTemplateAction(
                                        label = '角色資訊',
                                        text = '角色資訊'
                                    )
                                ]
                            )
                        )
                    )
    def show_start(self , event): 
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '踏上旅程，在前方是未知的道路!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '前進',
                                        text = '前進'
                                    ),
                                    MessageTemplateAction(
                                        label = '背包',
                                        text = '背包'
                                    ),
                                    MessageTemplateAction(
                                        label = '地圖',
                                        text = '地圖'
                                    ),
                                    MessageTemplateAction(
                                        label = '角色資訊',
                                        text = '角色資訊'
                                    )
                                ]
                            )
                        )
                    )
    def character(self , event):
        global occupation,name,health_max,health_now,attack,defense,level,exp,money
        exp_max = ""
        if level == 1:
            exp_max = "/5"
        elif level == 2:
            exp_max = "/10"
        elif level == 3:
            exp_max = "/20"
        
        h = str(round(health_now,0))
        h_max = str(health_max)
        a = str(attack)
        d = str(defense)
        l = str(level)
        e= str(exp)
        m =str(money)
        line = '-----------------------\n'
        reply_token = event.reply_token
        send_text_message(reply_token,  '角色資訊:\n'+
                                        line+
                                        '名字  : '+name+'\n'+
                                        '職業  : '+occupation+'\n'+
                                        '等級  : '+l +'\n'+
                                        '經驗值: '+e + exp_max +'\n'+
                                        '生命值: '+h+"/"+h_max+'\n'+
                                        '攻擊力: '+a+'\n'+
                                        '防禦力: ' + d+'\n'+
                                        '金錢  : '+m) 
    def check_character(self , event):
        global money,health_max,health_now,attack,defense,level,attribute,backpack,health_equip,attack_equip,defense_equip,health_body,attack_body,defense_body,attribute_for_health,attribute_for_health_equip,attribute_for_health_weapon
        health_equip = 0
        attack_equip =0
        defense_equip=0
        for i in attribute:
            for j in equipment:
                if j == i[0]:
                    health_equip += int(i[1])
                    attack_equip += int(i[2])
                    defense_equip += int(i[3])
        health_max = health_body + health_equip
        attack = attack_body + attack_equip
        defense = defense_body +defense_equip
        attribute_for_health = attribute_for_health_equip + attribute_for_health_weapon
        if attribute_for_health != health_equip:
            health_now += health_equip - attribute_for_health
            attribute_for_health = health_equip
            attribute_for_health_equip = attribute_for_health/2
            attribute_for_health_weapon = attribute_for_health/2
            if attribute_for_health % 2 == 1:
                attribute_for_health_equip += 1
    def set_name(self, event):
        global name
        name = event.message.text
    def set_name_complete(self , event):
        global name
        reply_token = event.reply_token
        line = '-----------------------\n'
        send_text_message(reply_token, "無盡天使: "+name +"勇者大人，歡迎你的到來!\n"+line+"輸入 返回 回到角色選單")

    def set_occupation(self,event):
        global map_1,map_2,map_3,money,occupation,attack_body,health_body,defense_body,backpack,equipment,attribute,health_max,health_now,attack,defense,attribute_for_health,health_equip,attack_equip,defense_equip,attribute_for_health_equip , attribute_for_health_weapon,using_item
        occupation = event.message.text
        health_equip = 0
        attack_equip =0
        defense_equip=0
        if occupation == "狂戰士":
            health_body = 12
            attack_body = 200
            defense_body = 3
            equipment = ["普通大劍" , "破舊的大衣"] 
            for i in attribute:
                for j in equipment:
                    if j == i[0]:
                        health_equip += int(i[1])
                        attack_equip += int(i[2])
                        defense_equip += int(i[3])
                        if j == equipment[0]:
                            attribute_for_health_weapon = int(i[1])
                        if j == equipment[1]:
                            attribute_for_health_equip = int(i[1])
            health_max = health_body + health_equip
            health_now = health_max
            using_item.append(["生命粉塵","1"])
            using_item.append(["大生命粉塵","1"])
            using_item.append(["鬼人粉塵","1"])
            using_item.append(["硬化粉塵","1"])
            attack = attack_body + attack_equip
            defense = defense_body +defense_equip
            money = 10
        if occupation == "黑暗法師":
            health_body = 9
            attack_body = 3
            defense_body = 2
            equipment = ["短杖" , "初級魔法袍"]
            for i in attribute:
                for j in equipment:
                    if j == i[0]:
                        health_equip += int(i[1])
                        attack_equip += int(i[2])
                        defense_equip += int(i[3])
                        if j == equipment[0]:
                            attribute_for_health_weapon = int(i[1])
                        if j == equipment[1]:
                            attribute_for_health_equip = int(i[1])
            health_max = health_body + health_equip
            health_now = health_max
            using_item.append(["生命粉塵","1"])
            using_item.append(["大生命粉塵","1"])
            using_item.append(["鬼人粉塵","1"])
            using_item.append(["硬化粉塵","1"])
            attack = attack_body + attack_equip
            defense = defense_body +defense_equip
            money = 10
        if occupation == "精靈射手":
            health_body = 10
            attack_body = 3
            defense_body = 3
            equipment = ["短弓" , "簡陋的衣裝"]
            for i in attribute:
                for j in equipment:
                    if j == i[0]:
                        health_equip += int(i[1])
                        attack_equip += int(i[2])
                        defense_equip += int(i[3])
                        if j == equipment[0]:
                            attribute_for_health_weapon = int(i[1])
                        if j == equipment[1]:
                            attribute_for_health_equip = int(i[1])
            health_max = health_body + health_equip
            health_now = health_max
            using_item.append(["生命粉塵","1"])
            using_item.append(["大生命粉塵","1"])
            using_item.append(["鬼人粉塵","1"])
            using_item.append(["硬化粉塵","1"])
            attack = attack_body + attack_equip
            defense = defense_body +defense_equip
            money = 10
        line = '-----------------------\n'
        random.shuffle(map_1)
        random.shuffle(map_2)
        random.shuffle(map_3)
        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使: 你選擇的職業是 "+occupation +"，馬上展開你的冒險吧!\n"+line+"輸入 返回 回到角色選單")

    def on_enter_state_fight(self , event):
        global health_equip,attack_equip,defense_equip,attribute,equipment,health_max,attack,defense,health_body,attack_body,defense_body
        health_equip=0
        attack_equip =0
        defense_equip=0
        for i in attribute:
            for j in equipment:
                if j == i[0]:
                    health_equip += int(i[1])
                    attack_equip += int(i[2])
                    defense_equip += int(i[3])
        health_max = health_body + health_equip
        attack = attack_body + attack_equip
        defense = defense_body +defense_equip
        line = '-----------------------\n'
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '遭遇怪物，立刻攻擊!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '攻擊',
                                        text = '攻擊1'
                                    ),
                                    MessageTemplateAction(
                                        label = '攻擊2',
                                        text = '攻擊2'
                                    ),
                                    MessageTemplateAction(
                                        label = '道具',
                                        text = '道具'
                                    ),
                                    MessageTemplateAction(
                                        label = '當前狀態',
                                        text = '當前狀態'
                                    )
                                ]
                            )
                        ),TextSendMessage(text="當前怪物為: "+monster_now[0]+"\n"+
                                                "生命值: "+monster_now[1]+"\n"+
                                                "攻擊力: "+monster_now[2]+"\n"+
                                                "防禦力: "+monster_now[3]+"\n"+
                                                line+
                                                "你的狀態: \n"+
                                                "生命值: "+str(health_now)+"/"+str(health_max)+"\n"+
                                                "攻擊力: "+str(attack)+"\n"+
                                                "防禦力: "+str(defense)+"\n")
                        ]
                    )

    
    def on_enter_state_store(self , event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '神秘商人:這裡充滿神祕的商品，想要甚麼就拿走吧',
                                actions=[
                                    MessageTemplateAction(
                                        label = '藥水',
                                        text = '藥水'
                                    ),
                                    MessageTemplateAction(
                                        label = '刀',
                                        text = '刀'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        )
                    )
              
    
    def item(self , event):
        global backpack,attribute,drops,using_item
        item_in_backpack = ""
        weapon = ""
        equip = ""
        space_length=""
        spa_length=""
        item_tmp =""
        line = '-----------------------\n'
        for i in backpack:
            for j in attribute:
                if i == j[0]:
                    item_length = len(i)
                    for k in range(5 - item_length):
                        space_length += " "
                    item_in_backpack += i+ space_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 

        weapon += "武器: " + equipment[0]
        weapon_attribute = ""
        equip += "防具: " + equipment[1]
        equip_attribute = ""
        for i in range(len(equipment)):
            for j in attribute:
                if equipment[i] == j[0]:
                    equip_length = len(equipment[i])
                    for k in range(5-equip_length):
                        spa_length += " "
                    if i == 0:
                        weapon_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
                    if i == 1:
                        equip_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
        for i in using_item:
            item_tmp += i[0] +": x"+i[1]+"\n"
        
        reply_token = event.reply_token
        send_text_message(reply_token,  '背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        weapon + weapon_attribute + "\n"+
                                        equip + equip_attribute +"\n"+
                                        line+
                                        "道具:\n"+item_tmp+
                                        line+
                                        "輸入 更換裝備 以更換裝備。\n"+
                                        "輸入 道具介紹 可了解各藥草的功能") 
    def item_introduce(self,event):
    

        reply_token = event.reply_token
        send_text_message(reply_token, "生命粉塵  : 使用後回復5生命值\n"+
                                       "大生命粉塵: 使用後回復10生命值\n"+
                                       "鬼人粉塵  : 使用後永久增加1攻擊力\n"+
                                       "硬化粉塵  : 使用後永久增加1防禦力")
    def on_enter_state_change(self,event):
        global backpack,equipment,backpack,attribute,drops
        item_in_backpack = ""
        weapon = ""
        equip = ""
        space_length=""
        spa_length=""
        line = '-----------------------\n'
        for i in backpack:
            for j in attribute:
                if i == j[0]:
                    item_length = len(i)
                    for k in range(5 - item_length):
                        space_length += " "
                    item_in_backpack += i+ space_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 

        weapon += "武器: " + equipment[0]
        weapon_attribute = ""
        equip += "防具: " + equipment[1]
        equip_attribute = ""
        for i in range(len(equipment)):
            for j in attribute:
                if equipment[i] == j[0]:
                    equip_length = len(equipment[i])
                    for k in range(5-equip_length):
                        spa_length += " "
                    if i == 0:
                        weapon_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
                    if i == 1:
                        equip_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 


        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '更換裝備',
                                text = '請先選擇要更換武器或是防具,再輸入想要更換的裝備。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '更換武器',
                                        text = '更換武器'
                                    ),
                                    MessageTemplateAction(
                                        label = '更換防具',
                                        text = '更換防具'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        ),TextSendMessage(text='背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        weapon + weapon_attribute + "\n"+
                                        equip + equip_attribute )
                        ]
                        
                    )

    def on_enter_state_change_weapon(self,event):
        global backpack,equipment,backpack,attribute,drops
        item_in_backpack = ""
        weapon = ""
        equip = ""
        space_length=""
        spa_length=""
        line = '-----------------------\n'
        for i in backpack:
            for j in attribute:
                if i == j[0]:
                    item_length = len(i)
                    for k in range(5 - item_length):
                        space_length += " "
                    item_in_backpack += i+ space_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 

        weapon += "武器: " + equipment[0]
        weapon_attribute = ""
        equip += "防具: " + equipment[1]
        equip_attribute = ""
        for i in range(len(equipment)):
            for j in attribute:
                if equipment[i] == j[0]:
                    equip_length = len(equipment[i])
                    for k in range(5-equip_length):
                        spa_length += " "
                    if i == 0:
                        weapon_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
                    if i == 1:
                        equip_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
        reply_token = event.reply_token
        send_text_message(reply_token,  '背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        weapon + weapon_attribute + "\n"+
                                        equip + equip_attribute +"\n"+
                                        line+
                                        "輸入 欲更換裝備的名稱。") 

    def on_enter_state_change_equip(self,event):
        global backpack,equipment,backpack,attribute,drops
        item_in_backpack = ""
        weapon = ""
        equip = ""
        space_length=""
        spa_length=""
        line = '-----------------------\n'
        for i in backpack:
            for j in attribute:
                if i == j[0]:
                    item_length = len(i)
                    for k in range(5 - item_length):
                        space_length += " "
                    item_in_backpack += i+ space_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 

        weapon += "武器: " + equipment[0]
        weapon_attribute = ""
        equip += "防具: " + equipment[1]
        equip_attribute = ""
        for i in range(len(equipment)):
            for j in attribute:
                if equipment[i] == j[0]:
                    equip_length = len(equipment[i])
                    for k in range(5-equip_length):
                        spa_length += " "
                    if i == 0:
                        weapon_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
                    if i == 1:
                        equip_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
        reply_token = event.reply_token
        send_text_message(reply_token,  '背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        weapon + weapon_attribute + "\n"+
                                        equip + equip_attribute +"\n"+
                                        line+
                                        "輸入 欲更換裝備的名稱。") 

    
    def change_weapon(self,event):
        global backpack,equipment,backpack,attribute,drops,attribute_for_health,health_equip,attribute_for_health_weapon
        weapon_name =""
        weapon_name = event.message.text
        tmp = ""
        flag = "False"
        #health_equip_tmp = health_equip
        for i in attribute:
            if equipment[0] == i[0]:
                attribute_for_health_weapon = int(i[1]) 
                #health_equip_tmp += attribute_for_health
        for i in backpack:
            if i == weapon_name:
                tmp = equipment[0]
                equipment[0] = i
                backpack.append(tmp)
                backpack.remove(i)
                flag = "True"
 
        return flag
    def change_complete(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "裝備更換成功。\n輸入 返回 回到角色選單")

    def change_equip(self,event):
        global backpack,equipment,backpack,attribute,drops,attribute_for_health,health_equip,attribute_for_health_equip
        equip_name =""
        equip_name = event.message.text
        tmp = ""
        flag = "False"
        #health_equip_tmp = health_equip
        for i in attribute:
            if equipment[1] == i[0]:
                attribute_for_health_equip = int(i[1])
                #health_equip_tmp += attribute_for_health
        for i in backpack:
            if i == equip_name:
                tmp = equipment[1]
                equipment[1] = i
                backpack.append(tmp)
                backpack.remove(i)
                flag = "True"
        return flag
    def show_change_item(self,event):
        global backpack,equipment,backpack,attribute,drops
        item_in_backpack = ""
        weapon = ""
        equip = ""
        space_length=""
        spa_length=""
        line = '-----------------------\n'
        for i in backpack:
            for j in attribute:
                if i == j[0]:
                    item_length = len(i)
                    for k in range(5 - item_length):
                        space_length += " "
                    item_in_backpack += i+ space_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 

        weapon += "武器: " + equipment[0]
        weapon_attribute = ""
        equip += "防具: " + equipment[1]
        equip_attribute = ""
        for i in range(len(equipment)):
            for j in attribute:
                if equipment[i] == j[0]:
                    equip_length = len(equipment[i])
                    for k in range(5-equip_length):
                        spa_length += " "
                    if i == 0:
                        weapon_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 
                    if i == 1:
                        equip_attribute = spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] 


        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '更換裝備',
                                text = '請先選擇要更換武器或是防具,再輸入想要更換的裝備。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '更換武器',
                                        text = '更換武器'
                                    ),
                                    MessageTemplateAction(
                                        label = '更換防具',
                                        text = '更換防具'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        ),TextSendMessage(text='背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        weapon + weapon_attribute + "\n"+
                                        equip + equip_attribute )
                        ]
                        
                    )

    

    def on_enter_enter_name(self ,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使:請告訴我您的大名。")
    def show_build(self,event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '建立角色',
                                text = '無盡天使:請依序輸入您的大名，以及想要遊玩的職業。輸入完後點擊完成，開始冒險。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '設定名稱',
                                        text = '設定名稱'
                                    ),
                                    MessageTemplateAction(
                                        label = '選擇職業',
                                        text = '選擇職業'
                                    ),
                                    MessageTemplateAction(
                                        label = '完成',
                                        text = '完成'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        )
                    )

    def on_enter_choose_occupation(self,event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選擇職業',
                                text = '無盡天使:請選擇想要遊玩的職業，每個職業都有其強大的力量。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '狂戰士',
                                        text = '狂戰士'
                                    ),
                                    MessageTemplateAction(
                                        label = '黑暗法師',
                                        text = '黑暗法師'
                                    ),
                                    MessageTemplateAction(
                                        label = '精靈射手',
                                        text = '精靈射手'
                                    ),
                                    MessageTemplateAction(
                                        label = '職業介紹',
                                        text = '職業介紹'
                                    )
                                ]
                            )
                        )
                    )
    def show_choose_occupation(self,event):
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選擇職業',
                                text = '無盡天使:請選擇想要遊玩的職業，每個職業都有其強大的力量。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '狂戰士',
                                        text = '狂戰士'
                                    ),
                                    MessageTemplateAction(
                                        label = '黑暗法師',
                                        text = '黑暗法師'
                                    ),
                                    MessageTemplateAction(
                                        label = '精靈射手',
                                        text = '精靈射手'
                                    ),
                                    MessageTemplateAction(
                                        label = '職業介紹',
                                        text = '職業介紹'
                                    )
                                ]
                            )
                        ),
                            TextSendMessage(text="無盡天使:角色職業總共分為三大類,\n"+
                                        '-----------------------\n'+
                                        "狂戰士: 具有強大防禦力以及血量的維京人戰士，能夠穩定的輸出且續戰力驚人。\n使用武器為:刀、劍類\n\n"+
                                        "黑暗法師: 掌握魔法力量的法師，來自地下神秘組織，試圖用魔法掌控世界的走向。攻擊力相當高，防禦則相對薄弱。\n使用武器為:法仗\n\n"+
                                        "精靈射手: 來自據有長生不老之力的古老精靈族，世世代代傳承著驚人的弓術及戰鬥技巧，屬性方面相當的平衡。\n使用武器為:弓劍")
                        ]
                        
                    )



    def on_enter_state_map(self,event):
        global map,map_now,map_1,map_2,map_3,map_now_count
        path = ""
        line = '-----------------------\n'
        if map_now_count == -1:
            path = "新手鎮 ==> "
            for i in map_1:
                path += i[0] +" ==> "
                map_now = "新手鎮"
            path += "傳送門"
        if map_now_count >=0:
            if map_now_count <6:
                path = "新手鎮 ==> "
                for i in map_1:
                    path += i[0] + " ==> "
                map_now = map_1[map_now_count][0]
                path += "傳送門"
        if map_now_count >=6:
            if map_now_count <12:
                path = "傳送門 ==> "
                for i in map_2:
                    path += i[0] + " ==> "
                map_now = map_2[map_now_count-6][0]
                path += "傳送門"
        if map_now_count >=12:
            if map_now_count <18:
                path = "傳送門 ==> "
                for i in map_3:
                    path += i[0] + " ==> "
                map_now = map_3[map_now_count-12][0]
                path += "終點"

        
        reply_token = event.reply_token
        send_text_message(reply_token, "路線為: \n"+ path +"\n"+
                                        line+
                                        "當前位置為: \n"+ map_now +"\n"+
                                        line+
                                        "輸入 返回 回到選單" ) 

    def forward(self,event):
        global map_now_count,map_1,map_2,map_3,map_now,attribute,equipment,health_equip,attack_equip,defense_equip,health_max,health_now,attack,defense,health_body,attack_body,defense_body,attribute_for_health,attribute_for_health_equip , attribute_for_health_weapon
        map_now_count += 1
        if map_now_count >=0:
            if map_now_count <6:
                map_now = map_1[map_now_count][0]
        if map_now_count >=6:
            if map_now_count <12:
                map_now = map_2[map_now_count-6][0]
        if map_now_count >=12:
            if map_now_count <18:
                map_now = map_3[map_now_count-12][0]

        health_equip = 0
        attack_equip =0
        defense_equip=0
        for i in attribute:
            for j in equipment:
                if j == i[0]:
                    health_equip += int(i[1])
                    attack_equip += int(i[2])
                    defense_equip += int(i[3])
        health_max = health_body + health_equip
        attack = attack_body + attack_equip
        defense = defense_body +defense_equip 
        
        attribute_for_health = attribute_for_health_equip + attribute_for_health_weapon
        if attribute_for_health != health_equip:
            health_now += health_equip - attribute_for_health
            attribute_for_health = health_equip
            attribute_for_health_equip = attribute_for_health/2
            attribute_for_health_weapon = attribute_for_health/2
            if attribute_for_health % 2 == 1:
                attribute_for_health_equip += 1

    def check_map(self,event):
        global map_now_count,map,map_now,monster_1,monster_2,monster_3,monster_now,monster_now_count,monster_url,monster_now_url,map_now_count,map_1,map_2,map_3
        #monster_now_count +=1
        if map_now_count >= 0:
            if map_now_count <6:
                monster_now = random.choice(monster_1)
                monster_1.remove(monster_now)
        if map_now_count >= 6:
            if map_now_count <12:
                monster_now = random.choice(monster_2)
                monster_2.remove(monster_now)
        if map_now_count >= 12:
            if map_now_count <18:
                monster_now = random.choice(monster_3)
                monster_3.remove(monster_now)
        for i in monster_url:
            if monster_now[0] == i[0]:
                monster_now_url = i[1]
        if map_now_count >= 0 :
            if map_now_count <6:
                if map_1[map_now_count][1] == "戰鬥":
                    line_bot_api.reply_message(
                                event.reply_token,[
                                TemplateSendMessage(
                                    alt_text ='Buttons template',
                                    template = ButtonsTemplate(
                                        title = '對決',
                                        text = '可先查看當前狀態已了解魔物，在決定下一步怎麼辦。',
                                        actions=[
                                            MessageTemplateAction(
                                                label = '攻擊',
                                                text = '攻擊'
                                            ),
                                            MessageTemplateAction(
                                                label = '攻擊2',
                                                text = '攻擊2'
                                            ),
                                            MessageTemplateAction(
                                                label = '道具',
                                                text = '道具'
                                            ),
                                            MessageTemplateAction(
                                                label = '當前狀態',
                                                text = '當前狀態'
                                            )
                                        ]
                                    )
                                ),
                                    TextSendMessage(text="遇到了"+monster_now[0]+"，立刻攻擊!"),
                                    ImageSendMessage(original_content_url=monster_now_url,preview_image_url=monster_now_url)
                                    
                                ]
                                
                            )
                    return "戰鬥"  
        if map_now_count >=6 :
            if map_now_count <12:
                if map_2[map_now_count-6][1] == "戰鬥":
                    line_bot_api.reply_message(
                                event.reply_token,[
                                TemplateSendMessage(
                                    alt_text ='Buttons template',
                                    template = ButtonsTemplate(
                                        title = '對決',
                                        text = '可先查看當前狀態已了解魔物，在決定下一步怎麼辦。',
                                        actions=[
                                            MessageTemplateAction(
                                                label = '攻擊',
                                                text = '攻擊'
                                            ),
                                            MessageTemplateAction(
                                                label = '攻擊2',
                                                text = '攻擊2'
                                            ),
                                            MessageTemplateAction(
                                                label = '道具',
                                                text = '道具'
                                            ),
                                            MessageTemplateAction(
                                                label = '當前狀態',
                                                text = '當前狀態'
                                            )
                                        ]
                                    )
                                ),
                                    TextSendMessage(text="遇到了"+monster_now[0]+"，立刻攻擊!"),
                                    ImageSendMessage(original_content_url=monster_now_url,preview_image_url=monster_now_url)
                                    
                                ]
                                
                            )
                    return "戰鬥"      
        if map_now_count >=12 :
            if map_now_count <18:
                if map_3[map_now_count-12][1] == "戰鬥":
                    line_bot_api.reply_message(
                                event.reply_token,[
                                TemplateSendMessage(
                                    alt_text ='Buttons template',
                                    template = ButtonsTemplate(
                                        title = '對決',
                                        text = '可先查看當前狀態已了解魔物，在決定下一步怎麼辦。',
                                        actions=[
                                            MessageTemplateAction(
                                                label = '攻擊',
                                                text = '攻擊'
                                            ),
                                            MessageTemplateAction(
                                                label = '攻擊2',
                                                text = '攻擊2'
                                            ),
                                            MessageTemplateAction(
                                                label = '道具',
                                                text = '道具'
                                            ),
                                            MessageTemplateAction(
                                                label = '當前狀態',
                                                text = '當前狀態'
                                            )
                                        ]
                                    )
                                ),
                                    TextSendMessage(text="遇到了"+monster_now[0]+"，立刻攻擊!"),
                                    ImageSendMessage(original_content_url=monster_now_url,preview_image_url=monster_now_url)
                                    
                                ]
                            )
                    return "戰鬥"
        if map_now_count >= 0 :
            if map_now_count <6:
                if map_1[map_now_count][1] == "商店":
                    reply_token = event.reply_token
                    send_text_message(reply_token, "遇到商人,可購買商品。") 
                    return "商店"  
        if map_now_count >=6 :
            if map_now_count <12:
                if map_2[map_now_count-6][1] == "商店":
                    reply_token = event.reply_token
                    send_text_message(reply_token, "遇到商人,可購買商品。") 
                    return "商店"  
        if map_now_count >=12 :
            if map_now_count <18:
                if map_3[map_now_count-12][1] == "商店":
                    reply_token = event.reply_token
                    send_text_message(reply_token, "遇到商人,可購買商品。") 
                    return "商店"  
        
    def situation(self,event):
        global monster_now,map_now_count,health_max,health_now,attack,defense
        line = '-----------------------\n'
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '對決',
                                text = '可先查看當前狀態已了解魔物，在決定下一步怎麼辦。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '攻擊',
                                        text = '攻擊'
                                    ),
                                    MessageTemplateAction(
                                        label = '攻擊2',
                                        text = '攻擊2'
                                    ),
                                    MessageTemplateAction(
                                        label = '道具',
                                        text = '道具'
                                    ),
                                    MessageTemplateAction(
                                        label = '當前狀態',
                                        text = '當前狀態'
                                    )
                                ]
                            )
                        ),  
                            TextSendMessage(text="當前怪物為: "+monster_now[0]+"\n"+
                                                "生命值: "+monster_now[1]+"\n"+
                                                "攻擊力: "+monster_now[2]+"\n"+
                                                "防禦力: "+monster_now[3]+"\n"+
                                                line+
                                                "你的狀態: \n"+
                                                "生命值: "+str(health_now)+"/"+str(health_max)+"\n"+
                                                "攻擊力: "+str(attack)+"\n"+
                                                "防禦力: "+str(defense)+"\n")
                        ]
                        
                    )
    def attacking(self,event):
        global monster_now,map_now_count,attack,defense
        damage = attack - int(monster_now[3])
        if damage <= 0 :
            damage =0
        monster_now[1] = str(int(monster_now[1]) - damage)
        
        if int(monster_now[1]) <= 0 :
            return  "死亡"
        
    def show_attacking(self,event):
        global monster_now,map_now_count,health_max,health_now,attack,defense
        line = '-----------------------\n'
        damage = int(monster_now[2]) - defense
        if damage <= 0:
            damage =0
        d = attack - int(monster_now[3])
        if d <= 0:
            d=0
        health_now = health_now - damage
        if health_now <=0 :
            return "角色死亡"
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '對決',
                                text = '可先查看當前狀態已了解魔物，在決定下一步怎麼辦。',
                                actions=[
                                    MessageTemplateAction(
                                        label = '攻擊',
                                        text = '攻擊'
                                    ),
                                    MessageTemplateAction(
                                        label = '攻擊2',
                                        text = '攻擊2'
                                    ),
                                    MessageTemplateAction(
                                        label = '道具',
                                        text = '道具'
                                    ),
                                    MessageTemplateAction(
                                        label = '當前狀態',
                                        text = '當前狀態'
                                    )
                                ]
                            )
                        ),
                            TextSendMessage(text="你對怪物造成了 "+str(d) +" 傷害!\n"+
                                                 "怪物沒有死亡，並造成 "+str(damage)+" 點傷害" +
                                                 line+
                                                 "當前怪物為: "+monster_now[0]+"\n"+
                                                "生命值: "+monster_now[1]+"\n"+
                                                "攻擊力: "+monster_now[2]+"\n"+
                                                "防禦力: "+monster_now[3]+"\n"+
                                                line+
                                                "你的狀態: \n"+
                                                "生命值: "+str(health_now)+"/"+str(health_max)+"\n"+
                                                "攻擊力: "+str(attack)+"\n"+
                                                "防禦力: "+str(defense)+"\n")
                        ]
                        
                    )
    def show_result(self,event):
        global money,monster_now,map_now_count,health_max,health_now,attack,defense,exp,level,occupation,drops,backpack,health_body,attack_body,defense_body,drop_1_sword,drop_2_sword
        global drop_3_sword,drop_1_magic,drop_2_magic,drop_3_magic,drop_1_arch,drop_2_arch,drop_3_arch,monster_now_count
        tmp_level = level
        upgrade_text =""
        tmp = 0
        drop_tmp = ""
        tmp_text = ""
        exp += int(monster_now[4])
        if exp >=5 :
            level = 2
            if exp >=10:
                level = 3
                if exp >=20:
                    level = 4
        if tmp_level != level:  ##升等
            upgrade_text = "\n並且等級提升了一等,屬性值獲得提升。"
            if level == 2:
                health_body += 3
                health_now += 3
                attack_body += 2
                defense_body += 1

            if level == 3:
                health_body += 3
                health_now += 3
                attack_body += 2
                defense_body += 1

        if occupation =="狂戰士":
            tmp = random.randint(1,10)
            if tmp <= 5:
                if monster_now_count>=0:
                    if monster_now_count <6:
                        drop_tmp = random.choice(drop_1_sword)
                        backpack.append(drop_tmp)
                        backpack.append("炎王龍雙刀")
                        tmp_text ="\n怪物掉落了 "+drop_tmp
                if monster_now_count>=6:
                    if monster_now_count <12:
                        drop_tmp = random.choices(drop_2_sword)
                        backpack.append(drop_tmp)
                if monster_now_count>=12:
                    if monster_now_count <18:
                        drop_tmp = random.choices(drop_3_sword)
                        backpack.append(drop_tmp)

        
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選擇',
                                text = '踏上旅程，在前方是未知的道路!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '前進',
                                        text = '前進'
                                    ),
                                    MessageTemplateAction(
                                        label = '背包',
                                        text = '背包'
                                    ),
                                    MessageTemplateAction(
                                        label = '地圖',
                                        text = '地圖'
                                    ),
                                    MessageTemplateAction(
                                        label = '角色資訊',
                                        text = '角色資訊'
                                    )
                                ]
                            )
                        ),TextSendMessage(text="你打敗了"+monster_now[0]+"\n"+"獲得"+monster_now[4]+"經驗值" +upgrade_text+tmp_text)
                            
                        ]
                        
                    )
    def on_enter_state_dead(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "你被魔物殺死了，真是可惜。\n是否支付50金幣來復活呢?\n輸入 復活 重新回到世界!") 

    def on_enter_state_item(self,event):
        global using_item
        item_tmp = ""
        for i in using_item:
            item_tmp += i[0] +": x"+i[1]+"\n"
        #item_tmp -= "\n"

        line = '-----------------------\n'
        reply_token = event.reply_token
        send_text_message(reply_token,"道具:\n"+
                                      line+
                                      item_tmp+
                                      line+
                                      "輸入 道具的名稱 來使用道具。\n"+
                                      "輸入 返回 回到對決選單")

    def use_item(self,event):
        global using_item,health_now,health_max,attack_body,defense_body
        item_tmp = ""
        item_tmp = event.message.text
        flag = "False"

        if item_tmp == "生命粉塵":
            for i in range(len(using_item)):
                if using_item[i][0] == "生命粉塵":
                    if int(using_item[i][1]) >0 :
                        using_item[i][1]= str(int(using_item[i][1]) - 1)
                        flag = "True"
                        health_now += 5
                        if health_now >= health_max:
                            health_now = health_max
        if item_tmp == "大生命粉塵":
            for i in range(len(using_item)):
                if using_item[i][0] == "大生命粉塵":
                    if int(using_item[i][1]) >0 :
                        using_item[i][1]= str(int(using_item[i][1]) - 1)
                        flag = "True"
                        health_now += 10
                        if health_now >= health_max:
                            health_now = health_max
        if item_tmp == "鬼人粉塵":
            for i in range(len(using_item)):
                if using_item[i][0] == "鬼人粉塵":
                    if int(using_item[i][1]) > 0:
                        using_item[i][1]= str(int(using_item[i][1]) - 1)
                        flag = "True"
                        attack_body += 1
        if item_tmp == "硬化粉塵":
            for i in range(len(using_item)):
                if using_item[i][0] == "硬化粉塵":
                    if int(using_item[i][1]) > 0:
                        using_item[i][1]= str(int(using_item[i][1]) - 1)
                        flag = "True"
                        defense_body += 1
        return flag
    def use_item_complete(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "道具使用成功。\n輸入 返回 回到對決選單")
        
    def use_item_not_complete(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token, "道具使用失敗。\n輸入 返回 回到對決選單")

    def reborn(self,event):
        global health_now,health_max,money

        health_now = health_max
        money -= 50
        if money <=0:
            money =0