# Long-Running Setup for OpenClaw

This folder contains all the necessary scripts and configurations to run OpenClaw as a long-term service with automatic restart capabilities.

## Overview

This setup includes:
- PM2 process management for OpenClaw Gateway
- Keep-alive mechanisms for Codespace environments
- Configuration for multiple communication channels
- Microsoft Teams integration
- Automatic recovery from crashes or restarts

## Files Description

### `setup_long_running.sh`
Main setup script that configures PM2 to run OpenClaw as a long-running service with automatic restart capabilities.

### `init_openclaw.sh`
Initialization script to restore OpenClaw services after system restarts or downtime.

### `ecosystem.config.js`
PM2 configuration file that defines how OpenClaw should be managed as a service.

## Installation

1. Run the setup script:
```bash
chmod +x setup_long_running.sh
./setup_long_running.sh
```

2. The script will:
   - Install PM2 if needed
   - Configure OpenClaw to run with PM2
   - Set up automatic restart mechanisms
   - Create keep-alive processes

## Monitoring

Check the status of your OpenClaw service:
```bash
pm2 status
```

View logs:
```bash
pm2 logs
```

## Channels Configuration

The setup includes configurations for:
- WhatsApp
- Feishu/Lark
- Microsoft Teams

To configure Microsoft Teams, you'll need to add your Azure Bot credentials to the configuration file.

## Microsoft Teams Integration

The Microsoft Teams plugin (`@openclaw/msteams`) is already installed and configured. To use it:

1. Register a bot in Microsoft Azure Bot Service
2. Obtain your appId, appPassword, and tenantId
3. Update the msteams configuration in your OpenClaw config file

The plugin supports:
- Direct Messages
- Group chats
- Channels
- Threads
- Media sharing
- Polls
- Adaptive Cards

## Persistence Across Restarts

The setup includes mechanisms to preserve the OpenClaw service across system restarts by adding startup commands to the shell configuration.