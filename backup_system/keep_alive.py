#!/usr/bin/env python3
"""
WhatsApp Gateway Keep-Alive Service
This script maintains stable connection to WhatsApp gateway by implementing
periodic checks and automatic reconnection mechanisms.
"""

import time
import subprocess
import logging
import signal
import sys
from datetime import datetime
import threading
import requests

class WhatsAppKeepAlive:
    def __init__(self, check_interval=60):
        self.check_interval = check_interval
        self.running = True
        self.connection_status = "unknown"
        self.last_check = None
        self.failed_attempts = 0
        self.max_failed_attempts = 3
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/tmp/whatsapp_keepalive.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info("Received shutdown signal, stopping keep-alive service...")
        self.running = False
        
    def check_connection(self):
        """Check the current connection status"""
        try:
            # Try to get gateway status
            result = subprocess.run(
                ['openclaw', 'gateway', 'status'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            output = result.stdout.lower()
            
            # Check for various indicators of connection status
            is_connected = (
                'connected' in output or 
                'running' in output or 
                'active' in output or
                'up' in output
            )
            
            self.last_check = datetime.now()
            
            if is_connected:
                self.failed_attempts = 0  # Reset failure count on success
                self.connection_status = "connected"
                return True
            else:
                self.connection_status = "disconnected"
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Gateway status check timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error checking connection: {e}")
            return False
    
    def reconnect(self):
        """Attempt to reconnect to WhatsApp"""
        try:
            self.logger.info("Attempting to reconnect to WhatsApp...")
            
            # Start WhatsApp login process
            result = subprocess.run(
                ['whatsapp_login', 'action=start'], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            self.logger.info(f"Reconnection attempt completed with return code: {result.returncode}")
            
            if result.returncode == 0:
                self.logger.info("Reconnection initiated successfully")
                # Wait a bit to see if connection establishes
                time.sleep(10)
                return True
            else:
                self.logger.error(f"Reconnection failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Reconnection attempt timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error during reconnection: {e}")
            return False
    
    def heartbeat_check(self):
        """Perform a heartbeat check to maintain connection"""
        try:
            # Send a simple test message to ensure connection is alive
            result = subprocess.run([
                'openclaw', 'message', 
                'action=send', 
                'channel=whatsapp', 
                'target=+85294851476', 
                'message=Heartbeat check'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.debug("Heartbeat check successful")
                return True
            else:
                self.logger.warning(f"Heartbeat check failed: {result.stderr}")
                return False
        except Exception as e:
            self.logger.warning(f"Heartbeat check error: {e}")
            return False
    
    def run(self):
        """Main keep-alive loop"""
        self.logger.info("Starting WhatsApp Gateway Keep-Alive Service")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        while self.running:
            try:
                # Check current connection status
                is_connected = self.check_connection()
                
                if is_connected:
                    self.logger.debug("Connection is healthy")
                    # Reset failure counter
                    self.failed_attempts = 0
                    
                    # Perform heartbeat check occasionally
                    if self.last_check and \
                       (datetime.now() - self.last_check).seconds > self.check_interval * 2:
                        self.heartbeat_check()
                else:
                    self.failed_attempts += 1
                    self.logger.warning(f"Connection lost (attempt #{self.failed_attempts})")
                    
                    # If we've failed too many times, try to reconnect
                    if self.failed_attempts >= self.max_failed_attempts:
                        self.logger.info("Too many failed attempts, initiating reconnection...")
                        if self.reconnect():
                            self.failed_attempts = 0  # Reset after successful reconnection
                        else:
                            self.logger.error("Reconnection failed, will retry later")
                
                # Wait before next check
                for _ in range(self.check_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Unexpected error in keep-alive loop: {e}")
                time.sleep(self.check_interval)
        
        self.logger.info("Keep-Alive Service stopped")

def main():
    """Main entry point"""
    print("WhatsApp Gateway Keep-Alive Service")
    print("===================================")
    print(f"Started at: {datetime.now()}")
    print("Monitoring connection and maintaining stability...")
    print("")
    
    # Create and run keep-alive service
    keepalive = WhatsAppKeepAlive(check_interval=60)  # Check every minute
    keepalive.run()

if __name__ == "__main__":
    main()