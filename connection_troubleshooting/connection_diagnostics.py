#!/usr/bin/env python3
"""
Connection Diagnostics Tool
This script diagnoses connection issues and provides detailed reports
about the system's connection status and potential problems.
"""

import subprocess
import socket
import time
import json
import platform
from datetime import datetime
import os
import sys

class ConnectionDiagnostics:
    def __init__(self):
        self.diagnostics = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform.platform(),
            'hostname': socket.gethostname(),
            'checks': {}
        }
        
    def check_network_connectivity(self):
        """Check basic network connectivity"""
        print("Checking network connectivity...")
        
        try:
            # Test DNS resolution
            socket.gethostbyname('google.com')
            dns_ok = True
        except socket.gaierror:
            dns_ok = False
            
        # Test direct connection to common ports
        def test_port(host, port):
            try:
                sock = socket.create_connection((host, port), timeout=5)
                sock.close()
                return True
            except socket.error:
                return False
                
        google_connectivity = test_port('google.com', 80)
        whatsapp_connectivity = test_port('web.whatsapp.com', 443)
        
        self.diagnostics['checks']['network'] = {
            'dns_resolution': dns_ok,
            'google_connectivity': google_connectivity,
            'whatsapp_connectivity': whatsapp_connectivity
        }
        
        print(f"  DNS Resolution: {'✓' if dns_ok else '✗'}")
        print(f"  Google Connectivity: {'✓' if google_connectivity else '✗'}")
        print(f"  WhatsApp Connectivity: {'✓' if whatsapp_connectivity else '✗'}")
        
    def check_openclaw_gateway_status(self):
        """Check OpenClaw gateway status"""
        print("Checking OpenClaw gateway status...")
        
        try:
            result = subprocess.run(
                ['openclaw', 'gateway', 'status'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            status_info = {
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            self.diagnostics['checks']['gateway_status'] = status_info
            
            print(f"  Gateway Status Command: {'✓' if status_info['success'] else '✗'}")
            if not status_info['success']:
                print(f"  Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("  ✗ Gateway status check timed out")
            self.diagnostics['checks']['gateway_status'] = {
                'error': 'timeout',
                'success': False
            }
        except FileNotFoundError:
            print("  ✗ OpenClaw command not found")
            self.diagnostics['checks']['gateway_status'] = {
                'error': 'command_not_found',
                'success': False
            }
        except Exception as e:
            print(f"  ✗ Error checking gateway: {e}")
            self.diagnostics['checks']['gateway_status'] = {
                'error': str(e),
                'success': False
            }
            
    def check_process_status(self):
        """Check for running OpenClaw processes"""
        print("Checking OpenClaw processes...")
        
        try:
            # Find OpenClaw-related processes
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            openclaw_processes = []
            for line in result.stdout.split('\n'):
                if 'openclaw' in line.lower() and 'grep' not in line:
                    openclaw_processes.append(line.strip())
                    
            process_info = {
                'count': len(openclaw_processes),
                'processes': openclaw_processes
            }
            
            self.diagnostics['checks']['processes'] = process_info
            
            print(f"  Found {len(openclaw_processes)} OpenClaw processes")
            for proc in openclaw_processes[:3]:  # Show first 3 processes
                print(f"    {proc}")
                
        except Exception as e:
            print(f"  ✗ Error checking processes: {e}")
            self.diagnostics['checks']['processes'] = {
                'error': str(e),
                'count': 0,
                'processes': []
            }
            
    def check_system_resources(self):
        """Check system resources"""
        print("Checking system resources...")
        
        try:
            # Check CPU usage
            cpu_result = subprocess.run(
                ['top', '-bn1', '-p1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check memory usage
            mem_result = subprocess.run(
                ['free', '-m'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Check disk usage
            disk_result = subprocess.run(
                ['df', '-h'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            resource_info = {
                'cpu_available': cpu_result.returncode == 0,
                'memory_available': mem_result.returncode == 0,
                'disk_available': disk_result.returncode == 0,
                'memory_usage': mem_result.stdout if mem_result.returncode == 0 else None,
                'disk_usage': disk_result.stdout if disk_result.returncode == 0 else None
            }
            
            self.diagnostics['checks']['resources'] = resource_info
            
            print("  Resource checks completed")
            
        except Exception as e:
            print(f"  ✗ Error checking resources: {e}")
            self.diagnostics['checks']['resources'] = {
                'error': str(e)
            }
            
    def check_whatsapp_connection_details(self):
        """Check WhatsApp-specific connection details"""
        print("Checking WhatsApp connection details...")
        
        # Check if WhatsApp session exists
        session_exists = False
        session_path = os.path.expanduser('~/.openclaw/whatsapp_session/')
        if os.path.exists(session_path):
            session_exists = True
            # Count session files
            session_files = len(os.listdir(session_path)) if os.path.isdir(session_path) else 0
        else:
            session_files = 0
            
        # Check for WhatsApp-related errors in logs
        log_errors = []
        log_path = '/tmp/whatsapp_keepalive.log'
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:  # Check last 20 lines
                        if 'error' in line.lower() or 'exception' in line.lower():
                            log_errors.append(line.strip())
            except:
                pass  # Ignore if can't read log
                
        whatsapp_info = {
            'session_exists': session_exists,
            'session_files_count': session_files,
            'recent_errors': log_errors
        }
        
        self.diagnostics['checks']['whatsapp_details'] = whatsapp_info
        
        print(f"  WhatsApp session exists: {'✓' if session_exists else '✗'}")
        print(f"  Session files: {session_files}")
        print(f"  Recent errors in log: {len(log_errors)}")
        
    def generate_report(self):
        """Generate diagnostic report"""
        print("\n" + "="*60)
        print("CONNECTION DIAGNOSTICS REPORT")
        print("="*60)
        print(f"Generated at: {self.diagnostics['timestamp']}")
        print(f"Host: {self.diagnostics['hostname']}")
        print(f"Platform: {self.diagnostics['platform']}")
        print()
        
        # Print summary
        print("SUMMARY:")
        checks = self.diagnostics['checks']
        
        network_ok = checks.get('network', {}).get('google_connectivity', False)
        gateway_ok = checks.get('gateway_status', {}).get('success', False)
        resource_ok = checks.get('resources', {}).get('memory_available', False)
        
        print(f"  Network Connectivity: {'✓' if network_ok else '✗'}")
        print(f"  Gateway Status: {'✓' if gateway_ok else '✗'}")
        print(f"  System Resources: {'✓' if resource_ok else '✗'}")
        print()
        
        # Recommendations based on findings
        print("RECOMMENDATIONS:")
        if not network_ok:
            print("  • Check internet connection and DNS settings")
            print("  • Verify firewall settings allow outbound connections")
        if not gateway_ok:
            print("  • Restart OpenClaw gateway: openclaw gateway restart")
            print("  • Check OpenClaw configuration")
        if not resource_ok:
            print("  • Free up system memory or upgrade resources")
        if network_ok and gateway_ok and resource_ok:
            print("  • All basic checks passed")
            print("  • Consider checking WhatsApp Web session status")
            
        print()
        print("="*60)
        
    def run_all_checks(self):
        """Run all diagnostic checks"""
        print("Running connection diagnostics...")
        print()
        
        self.check_network_connectivity()
        print()
        
        self.check_openclaw_gateway_status()
        print()
        
        self.check_process_status()
        print()
        
        self.check_system_resources()
        print()
        
        self.check_whatsapp_connection_details()
        print()
        
        self.generate_report()
        
        return self.diagnostics

def main():
    print("Connection Diagnostics Tool")
    print("===========================")
    print(f"Starting diagnostics at: {datetime.now()}")
    print()
    
    diagnostics_tool = ConnectionDiagnostics()
    results = diagnostics_tool.run_all_checks()
    
    # Optionally save results to file
    output_file = f"connection_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    main()