import os
import flask

import cloud_storage
bucket_name = 'bucket-line-bot-storage'

import functions_framework

# Load secrets from environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

# Fallback to legacy SDK if 'V3' environment variable exists and contains 'legacy'
V3 = os.environ.get('LINE_SDK')
if type(V3) == str and V3.lower() == 'legacy':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import (
        MessageEvent,
        TextMessage, TextSendMessage,
        ImageMessage,
    )

    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        print(event.message)
        # Echo back the user input message
        response = event.message.text
        message = TextSendMessage(text=response)
        line_bot_api.reply_message(
            event.reply_token,
            message)

    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(event):
        print(event.message)
        message_id = event.message.id
        image_content = line_bot_api.get_message_content(message_id)
        cloud_storage.blob_upload(bucket_name, 'image.jpg',
                                  image_content.content,
                                  'image/jpeg')

    @handler.default()
    def handle_message(event):
        print(event.message)

else:
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
        ImageMessageContent,
    )

    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
            cloud_storage.blob_upload(bucket_name, 'image.jpg',   original_image, 'image/jpeg')
            cloud_storage.blob_upload(bucket_name, 'preview.jpg', preview_image,  'image/jpeg')

    @handler.default()
    def handle_message(event):
        print(event.message)

@functions_framework.http
def webhook(request: flask.Request) -> flask.typing.ResponseReturnValue:
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print('Request: {}'.format(body))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature. Please check your channel access token/channel secret.', 400
    return 'OK', 200
