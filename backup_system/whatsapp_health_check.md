# WhatsApp Gateway Health Check

## Purpose
Regular monitoring of WhatsApp gateway connection to detect and resolve disconnection issues automatically.

## Scheduled Tasks

### 1. Connection Status Check
Run every 5 minutes to verify WhatsApp connection status.

### 2. Automatic Recovery
Trigger reconnection process when disconnection is detected.

### 3. Alert System
Notify administrators when connection issues occur.

## Implementation

### Cron Job Configuration
```
# Check WhatsApp connection every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/whatsapp_monitor.py >> /var/log/whatsapp_monitor.log 2>&1

# Alternative: Run simple connection check every 2 minutes
*/2 * * * * /path/to/whatsapp_health_check.sh
```

### Health Check Script
```bash
#!/bin/bash
# whatsapp_health_check.sh

LOG_FILE="/tmp/whatsapp_health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check gateway status
STATUS=$(openclaw gateway status 2>&1)

if echo "$STATUS" | grep -q "connected"; then
    echo "[$TIMESTAMP] WhatsApp gateway is healthy" >> $LOG_FILE
else
    echo "[$TIMESTAMP] WhatsApp gateway disconnected: $STATUS" >> $LOG_FILE
    
    # Attempt reconnection
    echo "[$TIMESTAMP] Attempting reconnection..." >> $LOG_FILE
    whatsapp_login action=start
    
    # Wait a moment and check again
    sleep 10
    NEW_STATUS=$(openclaw gateway status 2>&1)
    
    if echo "$NEW_STATUS" | grep -q "connected"; then
        echo "[$TIMESTAMP] Reconnection successful" >> $LOG_FILE
    else
        echo "[$TIMESTAMP] Reconnection failed" >> $LOG_FILE
        # Send alert to administrator
        # Add notification logic here
    fi
fi
```

## Best Practices

1. **Regular Monitoring**: Check connection status frequently (every 2-5 minutes)
2. **Graceful Recovery**: Allow time for reconnection attempts before escalating
3. **Logging**: Maintain detailed logs for troubleshooting
4. **Alerting**: Notify administrators of persistent issues
5. **Rate Limiting**: Avoid excessive reconnection attempts that might cause additional issues

## Common Disconnection Causes

1. Network instability
2. WhatsApp Web session timeout
3. Server resource constraints
4. Authentication token expiration
5. Browser/client state corruption

## Recovery Strategy

1. Detect disconnection quickly
2. Attempt automatic reconnection
3. Monitor reconnection success
4. Escalate to manual intervention if needed
5. Document the incident for future prevention