#!/bin/bash
# Setup script for WhatsApp Gateway Keep-Alive Service

set -e  # Exit on any error

echo "WhatsApp Gateway Keep-Alive Service Setup"
echo "========================================"

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="whatsapp-keepalive"
SYSTEMD_SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"
KEEPALIVE_DIR="/opt/openclaw/keepalive"
LOGROTATE_PATH="/etc/logrotate.d/whatsapp-keepalive"

# Check if running as root for systemd operations
if [ "$EUID" -ne 0 ]; then
    SUDO_CMD="sudo"
else
    SUDO_CMD=""
fi

echo "Creating directories..."
$SUDO_CMD mkdir -p "$KEEPALIVE_DIR"
$SUDO_CMD mkdir -p "/opt/openclaw/keepalive"

echo "Copying files..."
$SUDO_CMD cp "$SCRIPT_DIR/keep_alive.py" "$KEEPALIVE_DIR/"
$SUDO_CMD chmod +x "$KEEPALIVE_DIR/keep_alive.py"

# Copy the service file to systemd directory
$SUDO_CMD cp "$SCRIPT_DIR/whatsapp-keepalive.service" "$SYSTEMD_SERVICE_PATH"
$SUDO_CMD chmod 644 "$SYSTEMD_SERVICE_PATH"

# Create logrotate configuration
cat > /tmp/whatsapp_keepalive_logrotate << EOF
/tmp/whatsapp_keepalive.log {
    daily
    missingok
    rotate 10
    compress
    delaycompress
    copytruncate
    notifempty
}
EOF

$SUDO_CMD mv /tmp/whatsapp_keepalive_logrotate "$LOGROTATE_PATH"
$SUDO_CMD chmod 644 "$LOGROTATE_PATH"

# Reload systemd to recognize the new service
echo "Reloading systemd daemon..."
$SUDO_CMD systemctl daemon-reload

echo "Setting up service..."

# Enable and start the service
echo "Enabling service..."
$SUDO_CMD systemctl enable "$SERVICE_NAME"

echo "Starting service..."
$SUDO_CMD systemctl start "$SERVICE_NAME"

# Check service status
echo "Checking service status..."
if $SUDO_CMD systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "✓ Service is running successfully!"
    echo ""
    echo "Service status:"
    $SUDO_CMD systemctl status "$SERVICE_NAME" --no-pager -l
else
    echo "⚠ Service may have failed to start. Check logs with:"
    echo "  sudo journalctl -u $SERVICE_NAME -f"
fi

echo ""
echo "Setup completed!"
echo ""
echo "Commands for managing the service:"
echo "  Start:     sudo systemctl start $SERVICE_NAME"
echo "  Stop:      sudo systemctl stop $SERVICE_NAME"
echo "  Restart:   sudo systemctl restart $SERVICE_NAME"
echo "  Status:    sudo systemctl status $SERVICE_NAME"
echo "  Logs:      sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "Configuration files location:"
echo "  Service:   $SYSTEMD_SERVICE_PATH"
echo "  Script:    $KEEPALIVE_DIR/keep_alive.py"
echo "  Logs:      /tmp/whatsapp_keepalive.log (rotated via $LOGROTATE_PATH)"