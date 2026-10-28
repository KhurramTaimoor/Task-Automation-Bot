# Task Automation Bot — Python Desktop Workflow Prototype

A configurable **desktop GUI automation** project written in Python. It combines a Tkinter control panel with PyAutoGUI-driven, coordinate-based actions for repeating desktop workflows.

## Features
- Dark-themed Tkinter desktop dashboard
- Configurable channel/workflow count and action interval
- Screen-coordinate configuration stored in JSON
- Start/stop workflow controls and status feedback
- A desktop-focused implementation that can be adapted to similar repetitive UI tasks

## Tech stack
Python · Tkinter / ttk · PyAutoGUI · JSON · threading

## Getting started
Requires Python 3 and a desktop session with an interactive screen.

```bash
git clone https://github.com/KhurramTaimoor/Task-Automation-Bot.git
cd Task-Automation-Bot
python -m pip install pyautogui
python autobot.py
```

Tkinter is bundled with many Python desktop installations. On some Linux systems it must be installed separately.

## Configuration
The script reads `bot_config_dynamic.json`. Its coordinates refer to positions **on the current computer's screen**. Calibrate them for your display resolution, scaling, and application layout before starting automation.

## Limitations and safety
This is an **experimental coordinate-based automation tool**, not a universal AI agent. Screen positions and timing may need readjustment whenever the target application changes. Test with a non-critical workflow and keep a way to interrupt automation before use.

## Engineering focus
GUI programming · event-driven controls · configuration management · desktop automation.

**Maintainer:** [Khurram Taimoor](https://github.com/KhurramTaimoor)
