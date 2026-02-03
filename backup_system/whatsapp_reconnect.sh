#!/bin/bash
# WhatsApp Gateway Reconnection Script
# This script handles reconnection after WhatsApp gateway disconnection

echo "WhatsApp Gateway Reconnection Script"
echo "====================================="
echo "Timestamp: $(date)"
echo ""

# Function to check gateway status
check_gateway_status() {
    echo "Checking gateway status..."
    status=$(openclaw gateway status 2>&1)
    echo "$status"
    if echo "$status" | grep -q "connected"; then
        echo "Gateway is already connected."
        exit 0
    fi
}

# Function to reconnect WhatsApp
reconnect_whatsapp() {
    echo "Starting WhatsApp reconnection process..."
    
    # Start WhatsApp login process
    echo "Initiating WhatsApp login..."
    whatsapp_login action=start
    
    # Wait for QR code generation
    sleep 5
    
    # Wait for successful connection
    echo "Waiting for WhatsApp connection to establish..."
    timeout 60 bash -c '
        while ! openclaw gateway status | grep -q "connected"; do
            echo "Waiting for connection..."
            sleep 5
        done
    '
    
    # Check final status
    if openclaw gateway status | grep -q "connected"; then
        echo "WhatsApp gateway successfully reconnected!"
        return 0
    else
        echo "Failed to reconnect WhatsApp gateway."
        return 1
    fi
}

# Main execution
main() {
    echo "Starting reconnection procedure..."
    
    # Check current status
    check_gateway_status
    
    # Attempt reconnection
    if reconnect_whatsapp; then
        echo ""
        echo "Reconnection successful!"
        echo "WhatsApp gateway is now operational."
        echo "Last updated: $(date)"
    else
        echo ""
        echo "Reconnection failed. Please check manually."
        echo "Consider restarting the OpenClaw service:"
        echo "  openclaw gateway restart"
        exit 1
    fi
}

# Execute main function
main