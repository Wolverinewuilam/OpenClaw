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