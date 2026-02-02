#!/bin/bash
# Setup script for long-running OpenClaw instance with PM2

echo "Setting up OpenClaw for long-running operation..."

# Install PM2 if not already installed
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    npm install -g pm2
fi

# Create PM2 ecosystem configuration
cat > /home/codespace/.openclaw/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'openclaw-gateway',
    script: '/usr/local/share/nvm/versions/node/v24.11.1/bin/openclaw',
    args: 'gateway start',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      HOME: '/home/codespace'
    }
  }],
  deploy: {
    production: {
      user: 'codespace',
      host: 'localhost',
      ref: 'origin/main',
      repo: '.',
      path: '/home/codespace/.openclaw',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
EOF

# Start OpenClaw with PM2
echo "Starting OpenClaw with PM2..."
pm2 start /home/codespace/.openclaw/ecosystem.config.js

# Save PM2 configuration for auto-restart
pm2 save

# Create keep-alive script
cat > /home/codespace/.openclaw/keepalive.sh << 'EOF'
#!/bin/bash
# Keep alive script to prevent Codespace from sleeping

while true; do
  echo "$(date): Keeping Codespace alive..." >> /tmp/codespace_keepalive.log
  # Touch a file to show activity
  touch /tmp/codespace_activity_$(date +%Y%m%d_%H%M%S)
  
  # Clean up old temp files (keep only last 10)
  ls -t /tmp/codespace_activity_* 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
  
  # Wait 15 minutes before next activity
  sleep 900
done
EOF

chmod +x /home/codespace/.openclaw/keepalive.sh

# Start keepalive script in background
nohup /home/codespace/.openclaw/keepalive.sh > /tmp/keepalive.log 2>&1 &

# Create startup script for restoring PM2 processes
cat > /home/codespace/.openclaw/start_pm2.sh << 'EOF'
#!/bin/bash
# Script to restore PM2 processes after Codespace restart

# Start PM2 daemon if not running
pm2 ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Starting PM2 daemon..."
    pm2 resume > /dev/null 2>&1 || pm2 resurrect > /dev/null 2>&1 || echo "PM2 daemon started"
fi

# Restore saved processes
echo "Restoring saved PM2 processes..."
pm2 start /home/codespace/.pm2/dump.pm2 > /dev/null 2>&1

# Or use resurrect to restore from dump
pm2 resurrect > /dev/null 2>&1

echo "PM2 processes restored. Check status with: pm2 status"
EOF

chmod +x /home/codespace/.openclaw/start_pm2.sh

# Add to shell configuration for automatic restoration
echo '# Restore PM2 processes if needed' >> ~/.bashrc
echo 'if [ -f /home/codespace/.openclaw/start_pm2.sh ]; then' >> ~/.bashrc
echo '  /home/codespace/.openclaw/start_pm2.sh' >> ~/.bashrc
echo 'fi' >> ~/.bashrc

echo "Setup complete!"
echo "OpenClaw is now running with PM2 for long-term operation."
echo "Check status with: pm2 status"
echo "View logs with: pm2 logs"