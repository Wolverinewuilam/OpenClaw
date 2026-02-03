#!/usr/bin/env python3
"""
WhatsApp Gateway Monitor
This script monitors the WhatsApp gateway connection and performs automatic recovery if needed.
"""

import time
import subprocess
import logging
import json
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/whatsapp_monitor.log'),
        logging.StreamHandler()
    ]
)

class WhatsAppMonitor:
    def __init__(self):
        self.last_status = None
        self.disconnection_count = 0
        
    def get_gateway_status(self):
        """Get current gateway status"""
        try:
            result = subprocess.run(['openclaw', 'gateway', 'status'], 
                                  capture_output=True, text=True, timeout=10)
            return result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            logging.error("Gateway status check timed out")
            return None, -1
        except Exception as e:
            logging.error(f"Error checking gateway status: {e}")
            return None, -1
    
    def is_connected(self, status_output):
        """Check if gateway is connected based on status output"""
        if not status_output:
            return False
        # Look for connection indicators in the status output
        return ('connected' in status_output.lower() or 
                'running' in status_output.lower() or 
                'active' in status_output.lower())
    
    def attempt_reconnection(self):
        """Attempt to reconnect WhatsApp gateway"""
        try:
            logging.info("Attempting WhatsApp reconnection...")
            result = subprocess.run(['whatsapp_login', 'action=start'], 
                                  capture_output=True, text=True, timeout=30)
            logging.info(f"Reconnection attempt completed: {result.returncode}")
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logging.error("Reconnection attempt timed out")
            return False
        except Exception as e:
            logging.error(f"Error during reconnection: {e}")
            return False
    
    def monitor(self, check_interval=60):
        """Main monitoring loop"""
        logging.info("Starting WhatsApp gateway monitoring...")
        
        while True:
            try:
                status_output, return_code = self.get_gateway_status()
                
                if return_code != 0:
                    logging.warning("Unable to retrieve gateway status")
                else:
                    is_conn = self.is_connected(status_output)
                    
                    if is_conn:
                        if self.last_status == False:
                            logging.info("Connection restored!")
                        self.disconnection_count = 0
                        logging.debug("Gateway is connected")
                    else:
                        self.disconnection_count += 1
                        logging.warning(f"Gateway disconnected (#{self.disconnection_count})")
                        
                        # If disconnected for more than 3 checks, attempt reconnection
                        if self.disconnection_count >= 3:
                            logging.info("Attempting automatic reconnection...")
                            if self.attempt_reconnection():
                                self.disconnection_count = 0  # Reset counter after successful reconnection
                            else:
                                logging.error("Automatic reconnection failed")
                
                self.last_status = is_conn if return_code == 0 else None
                
                # Wait before next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logging.info("Monitoring stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error in monitoring: {e}")
                time.sleep(check_interval)

def main():
    print("WhatsApp Gateway Monitor")
    print("========================")
    print(f"Started at: {datetime.now()}")
    print("Monitoring WhatsApp gateway connection...")
    print("")
    
    monitor = WhatsAppMonitor()
    monitor.monitor()

if __name__ == "__main__":
    main()