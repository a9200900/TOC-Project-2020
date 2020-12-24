from transitions.extensions import GraphMachine
import os

from utils import send_text_message
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage)
from linebot import LineBotApi, WebhookParser

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
name = ''
occupation = ''
health = 0
attack = 0
defense = 0
level = 1
exp = 0
backpack = []
equipment = []
attribute = [["普通大劍" , "0" ,"1","1"] ,["短杖","0","1","1"] ,["短弓","0","1","1"] ,["破舊的大衣","1","0","1"],["初級魔法袍","1","0","1"]
,["簡陋的衣裝","1","0","1"]] 
monster = [["哥布林","6","2","1","2"],["女巫","8","3","1","3"],["盜賊","9","3","1","5"],["墮落的勇者","12","3","2","5"],["史萊姆","20","2","2","5"]]
monster_url = [["哥布林","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%93%A5%E5%B8%83%E6%9E%97.png"],["女巫","https://raw.githubusercontent.com/a9200900/TOC-Project-2020/master/img/%E5%A5%B3%E5%B7%AB.png"]]
monster_now = []
monster_now_url=""
monster_now_count = 0
map = [["新手鎮","休息"],["幽靜小路","戰鬥"],["被詛咒的沼澤","戰鬥"],["山洞","戰鬥"],["市集","商店"]]
map_now = "新手鎮"
map_now_count = -1
drops = [["狂戰士","鋒利的彎刀","鎖子甲"] , ["黑暗法師","精緻魔杖","上等法袍"] , ["精靈射手","骨製彎曲弓","上等絲綢服"]]


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

    def on_enter_state_fight(self , event):
        
        
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '遭遇怪物，立刻攻擊!',
                                actions=[
                                    MessageTemplateAction(
                                        label = '攻擊1',
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
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        )
                    )

    # def on_exit_state_fight(self , event):
    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "戰鬥結束")

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
    def character(self , event):
        global occupation,name,health,attack,defense,level

        
        h = str(health)
        a = str(attack)
        d = str(defense)
        l = str(level)
        line = '-----------------------\n'
        reply_token = event.reply_token
        send_text_message(reply_token,  '角色資訊:\n'+
                                        line+
                                        '名字  : '+name+'\n'+
                                        '職業  : '+occupation+'\n'+
                                        '等級  : '+l +'\n'+
                                        '生命值: '+h+'\n'+
                                        '攻擊力: '+a+'\n'+
                                        '防禦力:' + d) 

    def check_character(self , event):
        global occupation,name,health,attack,defense,level,attribute,backpack
        for i in attribute:
            for j in equipment:
                if j == i[0]:
                    health += int(i[1])
                    attack += int(i[2])
                    defense += int(i[3])
            
    
    def item(self , event):
        global backpack,attribute
        item_in_backpack = ""
        item_equip = ""
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
        for i in equipment:
            for j in attribute:
                if i == j[0]:
                    equip_length = len(i)
                    for k in range(5-equip_length):
                        spa_length += " "
                    item_equip += i+ spa_length +"+" + j[1] + " +" + j[2] + " +"+ j[3] + "\n" 


        reply_token = event.reply_token
        send_text_message(reply_token,  '背包:\n'+
                                        "名稱   " + "生命" +" 攻擊"+" 防禦\n"+
                                        item_in_backpack+
                                        line+
                                        "裝備中:\n"+
                                        item_equip) 
    def on_enter_build(self , event):
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '建立角色',
                                text = '無盡天使:請依序輸入您的大名，以及想要遊玩的職業。',
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
                                text = '無盡天使:請依序輸入您的大名，以及想要遊玩的職業。',
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
    def set_name(self, event):
        global name
        name = event.message.text
    def set_name_complete(self , event):
        global name
        reply_token = event.reply_token
        line = '-----------------------\n'
        send_text_message(reply_token, "無盡天使: "+name +"勇者大人，歡迎你的到來!\n"+line+"輸入 返回 回到角色選單")
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

    def set_occupation(self,event):
        global occupation,attack,health,defense,backpack,equipment
        occupation = event.message.text
        if occupation == "狂戰士":
            health = 12
            attack = 2
            defense = 3
            backpack = ["普通大劍" , "破舊的大衣"]  
            equipment = ["普通大劍" , "破舊的大衣"] 
        if occupation == "黑暗法師":
            health = 9
            attack = 3
            defense = 2
            backpack = ["短杖" , "初級魔法袍"]
            equipment = ["短杖" , "初級魔法袍"]
        if occupation == "精靈射手":
            health = 10
            attack = 3
            defense = 3
            backpack = ["短弓" , "簡陋的衣裝"]
            equipment = ["短弓" , "簡陋的衣裝"]

        line = '-----------------------\n'
        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使: 你選擇的職業是 "+occupation +"，馬上展開你的冒險吧!\n"+line+"輸入 返回 回到角色選單")

    def check_build(self,event):
        flag = False
        global occupation,name
        if occupation !="" :
            if name != "" :
                flag = True

        return flag


    def on_enter_state_map(self,event):
        global map,map_now
        path = ""
        line = '-----------------------\n'
        for i in map:
            path += i[0] + " ==> "
        reply_token = event.reply_token
        send_text_message(reply_token, "路線為: \n"+ path +"\n"+
                                        line+
                                        "當前位置為: \n"+ map_now +"\n"+
                                        line+
                                        "輸入 返回 回到選單" ) 

    def forward(self,event):
        global map_now_count,map,map_now
        map_now_count += 1
        map_now = map[map_now_count][0]
        

    def check_map(self,event):
        global map_now_count,map,map_now,monster,monster_now,monster_now_count,monster_url,monster_now_url
        monster_now_count += 1
        monster_now = monster[monster_now_count]
        for i in monster_url:
            if monster_now[0] == i[0]:
                monster_now_url = i[1]

        if map[map_now_count][1] == "戰鬥":
            line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '對決',
                                text = '可先查看當前狀態已了解對手，在決定下一步怎麼辦。',
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
                            TextSendMessage(text="遭遇怪物，立刻攻擊!"),
                            ImageSendMessage(original_content_url=monster_now_url,preview_image_url=monster_now_url)
                            
                        ]
                        
                    )
            return "戰鬥"    

        if map[map_now_count][1] == "商店":
            reply_token = event.reply_token
            send_text_message(reply_token, "遇到商人,可購買商品。") 
            return "商店"  

        
    def situation(self,event):
        global monster_now,monster,map_now_count,health,attack,defense
        line = '-----------------------\n'
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '對決',
                                text = '可先查看當前狀態已了解對手，在決定下一步怎麼辦。',
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
                                                "生命值: "+str(health)+"\n"+
                                                "攻擊力: "+str(attack)+"\n"+
                                                "防禦力: "+str(defense)+"\n")
                        ]
                        
                    )
    def attacking(self,event):
        global monster_now,monster,map_now_count,health,attack,defense

        monster_now[1] = str(int(monster_now[1]) - (attack - int(monster_now[3])))
        
        if int(monster_now[1]) <= 0 :
            return  "死亡"
        
    def show_attacking(self,event):
        global monster_now,monster,map_now_count,health,attack,defense
        line = '-----------------------\n'
        damage = int(monster_now[2]) - defense
        if damage <= 0:
            damage =0
        line_bot_api.reply_message(
                        event.reply_token,[
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '對決',
                                text = '可先查看當前狀態已了解對手，在決定下一步怎麼辦。',
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
                            TextSendMessage(text="你對怪物造成了 "+str(attack - int(monster_now[3])) +" 傷害!\n"+
                                                 "怪物並沒有死亡，並且對你造成了 "+str(damage)+" 傷害" )
                        ]
                        
                    )
    def show_result(self,event):
        global monster_now,monster,map_now_count,health,attack,defense,exp,level,occupation,drops
        tmp_level = level
        upgrade_text =""
        exp += monster_now[4]
        if exp >5 :
            level = 1
            if exp >10:
                level = 2
                if exp >20:
                    level = 3
        if tmp_level != level:  ##升等
            upgrade_text = "\n並且等級提升了一等。"
        

        if monster_now[0]=="哥布林":
            if occupation =="狂戰士":
                backpack.append(drops[0][1])
            if occupation =="黑暗法師":
                backpack.append(drops[1][1])
            if occupation =="精靈射手":
                backpack.append(drops[2][1])

        if monster_now[0]=="女巫":
            if occupation =="狂戰士":
                backpack.append(drops[0][2])
            if occupation =="黑暗法師":
                backpack.append(drops[1][2])
            if occupation =="精靈射手":
                backpack.append(drops[2][2])
        
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
                        ),TextSendMessage(text="你打敗了"+monster_now[0]+"\n"+"獲得"+monster_now[4]+"經驗值" +upgrade_text)
                            
                        ]
                        
                    )


