from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('JJD0E8rKBMJt8oJWYb7nLA+//BTO41erzPtuN8Y6ppoqip6Nxwg/J4tynEH5Dmv2QIjkyvIRIucsys9JGXfAdnWzzyr926U9HFtWZpoRAW9LjiVkycKj3tbdQfiUDc7qKqpyW/Nid0KVzP/DeKDuvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d0aeca891801277b3744c8053ef46239')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message) #回覆貼圖
        return #這個函式結束
 
    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎'
    else:
        r = msg
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()