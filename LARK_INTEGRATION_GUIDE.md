# Lark/Feishu Integration Guide

## Overview
This guide explains how to set up Lark/Feishu integration with OpenClaw using the lark-integration skill.

## Prerequisites
- A Lark/Feishu account (either international larksuite.com or China feishu.cn)
- Administrative rights to create an app in the Lark/Feishu developer console

## Step 1: Create a Lark/Feishu App

1. Go to the Lark/Feishu Developer Console:
   - International: https://open.larksuite.com/
   - China: https://open.feishu.cn/

2. Click "Create App" and select "Custom App"

3. Fill in the app information:
   - App Name: OpenClaw Assistant
   - App Description: AI assistant integration
   - Upload an app icon (optional)

## Step 2: Configure App Capabilities

1. In the left sidebar, click "App Capabilities"

2. Add the following capabilities:
   - "Messaging" - To send and receive messages
   - "Bot permissions" - To enable bot functionality

3. Under "Permissions & Scopes", enable these scopes:
   - `im:message` - Send and receive messages
   - `im:message:send_as_bot` - Send messages as bot
   - `im:resource` - Download message resources (images)

## Step 3: Get App Credentials

1. Go to "Credentials & Basic Info"
2. Note down the "App ID" and "App Secret"
3. Also note the "Verification Token" under "Event Subscriptions"

## Step 4: Configure Webhook

1. In the left sidebar, click "Event Subscriptions"
2. Add the following event:
   - `im.message.receive_v1` - To receive messages
3. Set the webhook URL to: `https://YOUR_CODESAPCE_URL-3000.app.github.dev/webhook`
   - Replace YOUR_CODESAPCE_URL with your actual GitHub Codespace URL
   - Our Codespace is: friendly-couscous-97j9qjrpgvv42pvvj
   - So the URL would be: https://friendly-couscous-97j9qjrpgvv42pvvj-3000.app.github.dev/webhook

## Step 5: Configure OpenClaw

1. Set the environment variables:
   ```bash
   export FEISHU_APP_ID='your_app_id'
   echo 'your_app_secret' > ~/.openclaw/secrets/feishu_app_secret
   ```

2. Start the bridge:
   ```bash
   cd /home/codespace/.openclaw/workspace/skills/lark-integration/scripts
   node bridge-webhook.mjs
   ```

## Step 6: Test the Integration

1. Add your Lark/Feishu bot to a chat
2. Send a message mentioning the bot or ending with "?" to trigger a response
3. The bot should respond via OpenClaw

## Notes

- For public deployment, you'll need to ensure the webhook port (3000) is accessible
- In group chats, the bot responds when mentioned, when the message ends with "?" or "？", or when trigger words are detected
- Individual messages are responded to by default
- Images and rich text content are supported bi-directionally

## Troubleshooting

If you encounter issues:
1. Check that the webhook URL is accessible
2. Verify the app has the correct permissions
3. Ensure the verification token matches between OpenClaw and Lark/Feishu
4. Review logs in the bridge application