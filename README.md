# OpenClaw

OpenClaw is an AI-powered assistant platform.

## Features

- Multi-channel communication (currently supporting WhatsApp, with Lark/Feishu integration)
- Modern todo list application
- Extensible skill system
- Cloud-ready deployment
- PM2 process management for long-running operations

## Available Channels

- WhatsApp: Fully configured and operational
- Lark/Feishu: Integration available and configured
- Microsoft Teams: Plugin installed and ready for configuration

## Todo List Application

A modern, responsive todo list application is available in the `todo-app` directory, featuring:

- Modern UI with gradient designs
- Task management (add, edit, delete, mark complete)
- Filtering options (all, active, completed)
- Local storage persistence
- Responsive design for mobile and desktop
- Smooth animations and transitions

To run the todo app:
```bash
cd todo-app
python3 server.py
```

Visit http://localhost:8082 to access the application (running on port 8082 to avoid conflicts).

## Skills

Various skills are available to extend functionality, including the Lark/Feishu integration and long-running process management.

## Long-Running Operations

The system includes PM2 configuration for maintaining long-running operations with automatic restart capabilities.