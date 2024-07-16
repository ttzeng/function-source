## LINE Chat Bot Template ##

The source code in this repository serves as a template for creating chat bots on LINE Platform using [Google Cloud Functions][1]. Google Cloud Functions is a FaaS (*Function as a Service*) product provided by Google, which can be invoked to receive user messages sent from the LINE Platform through [webhook][2] events. As a code template, the chat bot not only dumps all event messages to logs, but also echo back text messages it receives from the user, and upload the received images to [Google Cloud Storage][4] for inspection.

In addition to `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` environment variables required to [access the channel][3] on LINE platform, an optional variable `LINE_SDK` can be set to `legacy`, to switch between the previous 2.x SDK and the latest OpenAPI based LINE bot SDK 3.x for experiments and comparison.

[1]: <https://cloud.google.com/functions/docs/concepts/overview> "Google Cloud Functions"
[2]: <https://developers.line.biz/en/docs/messaging-api/receiving-messages> "LINE Webhook"
[3]: <https://developers.line.biz/en/docs/basics/channel-access-token> "LINE Channel Access Token"
[4]: <https://cloud.google.com/storage/docs> "Google Cloud Storage"
