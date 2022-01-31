
Deploy

```bash
export PROJECT_ID=bots-for-telegram
export TOKEN=your-telegram-bot-token
```

```bash
gcloud run deploy container \
    --source "$(pwd)/container" \
    --region us-central1 \
    --allow-unauthenticated \
    --platform managed \
    --project ${PROJECT_ID}
```

```bash
gcloud run deploy compliquer \
    --source "$(pwd)/bot" \
    --region us-central1 \
    --allow-unauthenticated \
    --platform managed \
    --set-env-vars TOKEN=${TOKEN} \
    --set-env-vars JSON_RPC=$(gcloud run services describe container --format 'value(status.url)' --project ${PROJECT_ID}) \
    --project ${PROJECT_ID}
```

Set Webhook (only need to be done once)

```shell
curl "https://api.telegram.org/bot${TOKEN}/setWebhook?url=$(gcloud run services describe compliquer --format 'value(status.url)' --project ${PROJECT_ID})"
```