import os
import flask

import functions_framework

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent,
    ImageMessageContent,
    AudioMessageContent,
    VideoMessageContent,
    FileMessageContent,
    LocationMessageContent,
)

# Load secrets from environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@functions_framework.http
def webhook(request: flask.Request) -> flask.typing.ResponseReturnValue:
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature. Please check your channel access token/channel secret.', 400
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    print(event.message)
    with ApiClient(configuration) as api_client:
        # Echo back the user input message
        response = event.message.text
        api = MessagingApi(api_client)
        api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    print(event.message)
    with ApiClient(configuration) as api_client:
        api_blob = MessagingApiBlob(api_client)
        message_id = event.message.id
        original_image = api_blob.get_message_content(message_id)
        preview_image  = api_blob.get_message_content_preview(message_id)
        print('Size of image/preview image: {} {}'.format(len(original_image), len(preview_image)))

@handler.add(MessageEvent, message=StickerMessageContent)
@handler.add(MessageEvent, message=AudioMessageContent)
@handler.add(MessageEvent, message=VideoMessageContent)
@handler.add(MessageEvent, message=FileMessageContent)
@handler.add(MessageEvent, message=LocationMessageContent)
@handler.add(MessageEvent, message=LocationMessageContent)
def handle_message(event):
    print(event.message)
