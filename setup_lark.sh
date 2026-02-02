#!/bin/bash

# Lark Integration Setup Script

echo "Setting up Lark/Feishu integration for OpenClaw..."

# Create necessary directories
mkdir -p ~/.openclaw/secrets
mkdir -p ~/.env

echo "Lark Integration setup prepared."
echo "To complete the setup, you will need:"
echo "1. Create a Lark/Feishu app at https://open.larksuite.com or https://open.feishu.cn"
echo "2. Get your App ID and App Secret"
echo "3. Configure the webhook URL in the Lark developer console"
echo ""
echo "Example commands to run after obtaining credentials:"
echo "export FEISHU_APP_ID='your_app_id'"
echo "echo 'your_app_secret' > ~/.openclaw/secrets/feishu_app_secret"
echo "cd /home/codespace/.openclaw/workspace/skills/lark-integration/scripts"
echo "node bridge-webhook.mjs"