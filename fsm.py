from transitions.extensions import GraphMachine

from utils import send_text_message


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
        send_text_message(reply_token, "歡迎進入世界。")
        send_text_message(reply_token, "輸入 人物介紹 可了解基本背景\n輸入 開始冒險 可開始偉大的旅程")

    def on_enter_start(self , event):

        reply_token = event.reply_token
        send_text_message(reply_token, "即將踏上旅途\n輸入 戰鬥 可開始戰鬥\n輸入 返回 可回到介紹畫面")

    def on_enter_state_fight(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "戰鬥開始")

    def on_exit_state_fight(self , event):
        reply_token = event.reply_token
        send_text_message(reply_token, "戰鬥結束")
