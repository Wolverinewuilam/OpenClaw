# WhatsApp Gateway Troubleshooting Suite

This suite contains tools and documentation to handle WhatsApp gateway disconnection issues, specifically addressing error 1006 (abnormal WebSocket closure).

## Components

### 1. Troubleshooting Guide (`whatsapp_troubleshooting.md`)
Comprehensive guide explaining the disconnection issue, root causes, and resolution steps.

### 2. Auto-Reconnection Script (`whatsapp_reconnect.sh`)
Bash script to automatically reconnect the WhatsApp gateway when disconnections occur.

### 3. Connection Monitor (`whatsapp_monitor.py`)
Python script that continuously monitors the WhatsApp gateway connection and performs automatic recovery.

### 4. Health Check System (`whatsapp_health_check.md`)
Documentation for implementing scheduled health checks using cron jobs.

## Usage

### Manual Reconnection
```bash
chmod +x whatsapp_reconnect.sh
./whatsapp_reconnect.sh
```

### Continuous Monitoring
```bash
python3 whatsapp_monitor.py
```

### Scheduled Health Checks
Add to crontab:
```bash
# Check connection every 5 minutes
*/5 * * * * cd /path/to/whatsapp_troubleshooting && python3 whatsapp_monitor.py
```

## Error 1006 Resolution

The error 1006 indicates an abnormal WebSocket closure. This suite provides:

1. **Detection**: Automated detection of disconnection events
2. **Recovery**: Automatic reconnection attempts
3. **Monitoring**: Continuous monitoring with logging
4. **Alerting**: Notification system for persistent issues

## Implementation

1. Place all files in the `skills/whatsapp_troubleshooting/` directory
2. Make scripts executable: `chmod +x whatsapp_reconnect.sh`
3. Configure cron jobs as needed for automated monitoring
4. Test the reconnection script after installation