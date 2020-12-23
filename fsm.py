from transitions.extensions import GraphMachine
import os

from utils import send_text_message
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction)
from linebot import LineBotApi, WebhookParser

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        #self.go_back()

    def on_exit_state1(self,event):
        print("Leaving state1")
        reply_token = event.reply_token
        send_text_message(reply_token, "Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.go_back()

    def on_exit_state2(self,event):
        print("Leaving state2")
        reply_token = event.reply_token
        send_text_message(reply_token, "Leaving state2")

    def leaving_or_not(self , event):
        text = event.message.text
        return text.lower() == "go back"

    def on_enter_user(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger user")

    def on_enter_intro(self , event):

        reply_token = event.reply_token
        send_text_message(reply_token, "無盡天使:歡迎來到這個世界，你一定是上帝派來拯救我們的勇者，請你幫助我們打到大魔王『斯巴拉斯．魔迪耶爾』!")

    def introduce(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "現在是魔王曆128年,自從上一位勇者犧牲已經100多年了，沒有人能夠與現在的魔王抗衡，希望勇者您能幫助我們打到魔王!")

    def orientation(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎進入世界。\n輸入 人物介紹 可了解基本背景\n輸入 開始冒險 可開始偉大的旅程")
        

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
                                        label = '返回',
                                        text = '返回'
                                    )
                                ]
                            )
                        )
                    )

    def on_enter_state_fight(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "戰鬥開始")

    def on_exit_state_fight(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "戰鬥結束")

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