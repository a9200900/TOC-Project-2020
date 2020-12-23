import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction)

from fsm import TocMachine
from utils import send_text_message


load_dotenv()


machine = TocMachine(
    states=["intro", "start", "state_fight"],
    transitions=[
        {
            "trigger": "to_start",
            "source": "intro",
            "dest": "start",
        },
        {
            "trigger": "to_state_fight",
            "source": "start",
            "dest": "state_fight",  
        },
        {"trigger": "go_back_intro",
         "source": "start",
          "dest": "intro" ,
        },
        {"trigger": "go_back_start",
         "source": "state_fight",
          "dest": "start" ,
        },
    ],
    initial="intro",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            # if machine.state == "intro":
            #     if event.message.text == "進入":
            #         line_bot_api.reply_message(
            #             event.reply_token,
            #             TemplateSendMessage(
            #                 alt_text ='Buttons template',
            #                 template = ButtonsTemplate(
            #                     title = '選項',
            #                     text = '無盡天使:歡迎來到這個世界，你一定是上帝派來拯救我們的勇者，請你幫助我們打到大魔王『斯巴拉斯．魔迪耶爾』!',
            #                     actions=[
            #                         MessageTemplateAction(
            #                             label = '人物介紹',
            #                             text = '人物介紹'
            #                         ),
            #                         MessageTemplateAction(
            #                             label = '開始冒險',
            #                             text = '開始冒險'
            #                         )
            #                     ]
            #                 )
            #             )
            #         )

            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        # intro state
        if machine.state == "intro":
            if event.message.text == "人物介紹":
                machine.introduce(event)
        if machine.state == "intro":
            if event.message.text == "進入":
                machine.line_buttons(event)
        if event.message.text == "開始冒險":
            machine.to_start(event)
        

        #start state
        if machine.state == "start":
            if event.message.text == "返回":
                machine.go_back_intro(event)
        if event.message.text == "戰鬥":
            machine.to_state_fight(event)

        #fight state
        if machine.state == "state_fight":
            if event.message.text == "返回":
                machine.go_back_start(event)


        #response = machine.advance(event)
        #if response == False:
        #    send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
