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
    states=["intro","build","enter_name","choose_occupation","occupation_intro", "start", "state_fight", "state_store"],
    transitions=[
        {
            "trigger": "to_build",
            "source": "intro",
            "dest": "build",
        },
        {
            "trigger": "to_start",
            "source": "build",
            "dest": "start",
        },
        {
            "trigger": "to_enter_name",
            "source": "build",
            "dest": "enter_name",
        },
        {
            "trigger": "to_choose_occupation",
            "source": "build",
            "dest": "choose_occupation",
        },
        {
            "trigger": "to_occupation_intro",
            "source": "choose_occupation",
            "dest": "occupation_intro",
        },
        {
            "trigger": "go_back_choose_occupation",
            "source": "occupation_intro",
            "dest": "choose_occupation",
        },
        {
            "trigger": "go_back_build_name",
            "source": "enter_name",
            "dest": "build",
        },
        {
            "trigger": "go_back_build_occupation",
            "source": "choose_occupation",
            "dest": "build",
        },
        {
            "trigger": "go_back_build_start",
            "source": "start",
            "dest": "build",
        },
        {
            "trigger": "to_state_fight",
            "source": "start",
            "dest": "state_fight",  
        },
        {"trigger": "go_back_intro",
         "source": "build",
          "dest": "intro" ,
        },
        {"trigger": "go_back_start_fight",
         "source": "state_fight",
          "dest": "start" ,
        },
        {"trigger": "to_state_store",
         "source": "start",
          "dest": "state_store" ,
        },
        {"trigger": "go_back_start_store",
         "source": "state_store",
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
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        # intro state
        if machine.state == "intro":
            if event.message.text == "進入":
                machine.line_buttons_intro(event)
        if machine.state == "intro":
            if event.message.text == "人物介紹":
                machine.introduce(event)
                machine.line_buttons_intro(event)
        if event.message.text == "開始冒險":
            machine.to_build(event)

        #build state
        if machine.state == "build":
            if event.message.text == "設定名稱":
                machine.to_enter_name(event)
        if machine.state == "build":
            if event.message.text == "選擇職業":
                machine.to_choose_occupation(event)
        if machine.state == "build":
            if event.message.text == "返回":
                machine.go_back_intro(event)
        
        #name state
        if machine.state == "enter_name":  
            if event.message.text != "":
                machine.set_name(event)
                machine.set_name_complete(event)
                machine.go_back_build_name(event)
                machine.on_enter_build(event)
        #occupation state
        if machine.state == "choose_occupation":
            if event.message.text == "返回":
                machine.go_back_build_occupation(event)
        if machine.state == "choose_occupation":
            if if event.message.text == "職業介紹":
                machine.occupation_intro(event)
                machine.on_enter_choose_occupation(event)
        

        #start state
        if machine.state == "start":
            if event.message.text == "返回":
                machine.go_back_build_start(event)
        if machine.state == "start":
            if event.message.text == "戰鬥":
                machine.to_state_fight(event)
        if machine.state == "start":
            if event.message.text == "商店":
                machine.to_state_store(event)
        if machine.state == "start":
            if event.message.text == "角色資訊":
                machine.character(event)

        #fight state
        if machine.state == "state_fight":
            if event.message.text == "返回":
                machine.go_back_start_fight(event)

        #store state
        if machine.state == "state_store":
            if event.message.text == "返回":
                machine.go_back_start_store(event)


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
