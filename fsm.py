from transitions.extensions import GraphMachine
import os

from utils import send_text_message
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction)
from linebot import LineBotApi, WebhookParser

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
occupation = ""
health = 0
attack = 0
defense = 0
backpack = []
equipment = []
moster = ["哥布林","巫女","盜賊","墮落的勇者","史萊姆"]
map = []


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)


    def on_enter_intro(self , event):

        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使:歡迎來到這個世界，你一定是上帝派來拯救我們的勇者，請你幫助我們打到大魔王『斯巴拉斯．魔迪耶爾』!")   

    def on_enter_start(self , event):
        global occupation,health ,attack,defense
        occupation =  "狂戰士"
        health = 12
        attack = 3
        defense = 2
        
        line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text ='Buttons template',
                            template = ButtonsTemplate(
                                title = '選項',
                                text = '踏上旅程，在前方是未知的道路!\n'+
                                        '職業:'+occupation+'\n'+
                                        '生命:'+health+'\n'+
                                        '攻擊力:'+attack+'\n'+
                                        '防禦力:'+defense+'\n',
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
                                text = '這裡充滿神祕的商品，想要甚麼就拿走吧',
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
