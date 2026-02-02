#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Check if required environment variables are set
const appId = process.env.FEISHU_APP_ID;
const appSecretPath = process.env.FEISHU_APP_SECRET_PATH || path.join(process.env.HOME || '/home/codespace', '.openclaw', 'secrets', 'feishu_app_secret');

if (!appId) {
    console.error('Error: FEISHU_APP_ID environment variable is required');
    console.error('Please set it before running this script:');
    console.error('export FEISHU_APP_ID=your_app_id');
    process.exit(1);
}

if (!fs.existsSync(appSecretPath)) {
    console.error(`Error: App secret file not found at ${appSecretPath}`);
    console.error('Please create the file with your app secret:');
    console.error(`echo "your_app_secret" > ${appSecretPath}`);
    process.exit(1);
}

// Start the bridge
const { spawn } = require('child_process');

console.log('Starting Lark Integration Bridge...');
console.log(`App ID: ${appId}`);
console.log(`App Secret Path: ${appSecretPath}`);

const bridge = spawn('node', ['scripts/bridge-webhook.mjs'], {
    cwd: '/home/codespace/.openclaw/workspace/skills/lark-integration',
    env: {
        ...process.env,
        FEISHU_APP_ID: appId,
        FEISHU_APP_SECRET_PATH: appSecretPath,
        WEBHOOK_PORT: process.env.WEBHOOK_PORT || '3000'
    }
});

bridge.stdout.on('data', (data) => {
    console.log(`Bridge stdout: ${data}`);
});

bridge.stderr.on('data', (data) => {
    console.error(`Bridge stderr: ${data}`);
});

bridge.on('close', (code) => {
    console.log(`Bridge process exited with code ${code}`);
});