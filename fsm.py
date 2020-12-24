from transitions.extensions import GraphMachine
import os

from utils import send_text_message
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction)
from linebot import LineBotApi, WebhookParser

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
name = ''
occupation = ''
health = 0
attack = 0
defense = 0
# backpack = []
# equipment = []
# moster = ["哥布林","巫女","盜賊","墮落的勇者","史萊姆"]
# map = []


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
                                        label = '戰鬥',
                                        text = '戰鬥'
                                    ),
                                    MessageTemplateAction(
                                        label = '商店',
                                        text = '商店'
                                    ),
                                    MessageTemplateAction(
                                        label = '角色資訊',
                                        text = '角色資訊'
                                    ),
                                    MessageTemplateAction(
                                        label = '返回',
                                        text = '返回'
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
        global occupation,health,attack,defense
        occupation =  '狂戰士'
        health = 12
        attack = 3
        defense = 2
        
        h = str(health)
        a = str(attack)
        d = str(defense)
        line = '-----------------------\n'
        reply_token = event.reply_token
        send_text_message(reply_token, "角色資訊\n"+
                                        line+
                                        "職業: "+occupation+'\n'+
                                        "生命值: "+h+'\n'+
                                        "攻擊力: "+a+'\n'+
                                        "防禦力: "+d) 

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
        send_text_message(reply_token, "無盡天使: "+name +"勇者大人，歡迎你的到來!\n輸入 返回 回到角色選單")
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

    def set_occupation(self,event):
        global occupation
        occupation = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使: 你選擇的職業是 "+occupation +"，馬上展開你的冒險吧!\n輸入 返回 回到角色選單")

    def check_build(self,event):
        flag = False
        global occupation,name
        if occupation !="" :
            if name != "" :
                flag = True

        return flag