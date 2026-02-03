# WhatsApp Gateway Keep-Alive Configuration

## Purpose
Configuration and setup instructions for maintaining stable WhatsApp gateway connection.

## Components

### 1. Keep-Alive Service (`keep_alive.py`)
Python script that continuously monitors and maintains WhatsApp gateway connection.

### 2. Systemd Service File (`whatsapp-keepalive.service`)
Service file to run the keep-alive script as a system service.

### 3. Cron Job Configuration
Alternative method using cron jobs for periodic connection checks.

## Installation Instructions

### Method 1: Systemd Service (Recommended)
1. Copy `keep_alive.py` to `/opt/openclaw/keepalive/`
2. Copy `whatsapp-keepalive.service` to `/etc/systemd/system/`
3. Enable and start the service:
   ```bash
   sudo systemctl enable whatsapp-keepalive
   sudo systemctl start whatsapp-keepalive
   ```

### Method 2: Cron Job
Add to crontab for periodic checks:
```bash
# Check connection every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/keep_alive.py --check-only
```

## Configuration Options

### Check Interval
- Default: 60 seconds
- Adjust in `keep_alive.py` or via command-line argument

### Failed Attempts Threshold
- Default: 3 failed checks before attempting reconnection
- Adjustable in configuration

### Logging
- Logs to `/tmp/whatsapp_keepalive.log`
- Rotate logs as needed

## Monitoring

### Service Status
```bash
sudo systemctl status whatsapp-keepalive
```

### Logs
```bash
sudo journalctl -u whatsapp-keepalive -f
```

## Troubleshooting

### Common Issues
1. Permission errors accessing OpenClaw commands
2. Network connectivity issues
3. WhatsApp Web session expiration

### Resolution
1. Ensure proper permissions for executing OpenClaw commands
2. Check network connectivity
3. Manually refresh WhatsApp session if needed