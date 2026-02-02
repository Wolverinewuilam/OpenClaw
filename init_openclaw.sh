#!/bin/bash
# Initialization script for OpenClaw long-running service

echo "Initializing OpenClaw long-running service..."

# Ensure PM2 is running
if ! pgrep -f "PM2" > /dev/null; then
    echo "Starting PM2 daemon..."
    pm2 ping > /dev/null 2>&1 || pm2 resurrect > /dev/null 2>&1
fi

# Start OpenClaw if not already running
if ! pm2 list | grep -q "openclaw-gateway"; then
    echo "Starting OpenClaw gateway..."
    pm2 start /home/codespace/.openclaw/ecosystem.config.js
    pm2 save
else
    echo "OpenClaw gateway is already running"
fi

# Ensure keepalive script is running
if ! pgrep -f "keepalive.sh" > /dev/null; then
    echo "Starting keepalive script..."
    nohup /home/codespace/.openclaw/keepalive.sh > /tmp/keepalive.log 2>&1 &
fi

echo "Initialization complete!"
echo "Current status:"
pm2 status