# Connection Troubleshooting Tools

This directory contains tools for diagnosing and troubleshooting connection issues with the OpenClaw system, particularly focusing on WhatsApp gateway connectivity.

## Tools Included

### 1. Connection Diagnostics (`connection_diagnostics.py`)
A comprehensive diagnostic tool that checks various aspects of the system's connectivity:

- Network connectivity (DNS, general internet access)
- WhatsApp-specific connectivity (to web.whatsapp.com)
- OpenClaw gateway status
- Running processes
- System resources
- WhatsApp session details

## Usage

### Running Connection Diagnostics
```bash
python3 connection_diagnostics.py
```

This will perform a comprehensive check and provide:
- A summary of connection status
- Detailed diagnostic information
- Recommendations for fixing issues
- A JSON report saved to a timestamped file

## When to Use These Tools

Use these troubleshooting tools when experiencing:
- WhatsApp gateway disconnections
- Connection timeouts
- Intermittent connectivity issues
- Before implementing backup/redundancy solutions

## Backup vs. Troubleshooting

Note the distinction between:
- **Troubleshooting tools** (this directory): Used to diagnose and fix connection issues
- **Backup/Redundancy tools** (backup_system directory): Used to maintain system uptime and prevent issues

## Output Format

Diagnostic tools output structured JSON data along with human-readable reports, making it easy to analyze issues programmatically or manually.