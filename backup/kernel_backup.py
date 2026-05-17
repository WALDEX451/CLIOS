# The code snippet you provided at the beginning of your script is importing various Python modules
# that are necessary for different functionalities within your program. Here's a breakdown of what
# each import statement is doing:
# alle benodigheden
import os
import sys
import time
# voor random dingen in line 161
import random
import uuid
import getpass
import json
import shutil
import json # json voor de username instellingen
from pathlib import Path
import socket
import random
import platform
import subprocess # subprocces voor de linux commando's
from datetime import datetime
from pathlib import Path
#voor betere terminal output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
# voor systeem ram/cpu
import psutil




CONFIG_FILE = Path("config.json")

if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    password = config["password"]
    hostname = config["hostname"]
    username = config["username"]
    user_id = config["user_id"]

else:
    password = getpass.getpass("Create your password: ")
    hostname = input("Your computer hostname: ")
    username = input("Your username: ")
    user_id = str(uuid.uuid4())

    config = {
        "password": password,
        "hostname": hostname,
        "username": username,
        "user_id": user_id
    }

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def loading_bar(total=20):
    for i in range(total + 1):
        done = "#" * i
        left = "." * (total - i)
        percent = int((i / total) * 100)

        print(f"\rLoading: [{done}{left}] {percent}%", end="", flush=True)
        time.sleep(0.1)

    print()


loading_bar()
users = []
version = 1.0

while True:
    command = input(f"{username}@{hostname}$ ")
    
    if command == "help":
        print("""
╔══════════════════════════════════════════════════════╗
║                 DEVCORE CLI OS                      ║
║          Python Powered Linux CLI System            ║
╚══════════════════════════════════════════════════════╝

Welcome to Devcore CLI OS.
A lightweight Linux-inspired terminal environment for Raspberry Pi,
SSH workflows, development, networking, automation and system control.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASIC COMMANDS
help                Show this help menu
commands            Show all commands
clear               Clear the terminal
exit                Exit Devcore CLI
version             Show current version
about               Show information about Devcore CLI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM
sysinfo             Full system information
cpu                 Show CPU usage
ram                 Show memory usage
temp                Show Raspberry Pi temperature
disk                Show disk usage
uptime              Show system uptime
neofetch            Show system overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILES
ls                  List files
pwd                 Show current directory
cd <folder>         Change directory
mkdir <name>        Create folder
create <file>       Create new file
cat <file>          Read file
nano <file>         Open nano editor
rm <file>           Delete file
cp                  Copy files
mv                  Move files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NETWORK
ip                  Show IP address
wifi                Show WiFi information
ping <host>         Ping a host
scan                Scan local network
ports               Show open ports
ssh                 SSH tools
curl                Fetch URL data
wget                Download files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROCESS MANAGEMENT
ps                  Show running processes
top                 Live process monitor
kill <pid>          Kill process
services            Show services
logs                Show logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYTHON & DEVELOPMENT
python              Open Python
run <file.py>       Run Python file
pip list            Show Python packages
git status          Show git status
workspace           Open workspace

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECURITY
firewall            Firewall status
encrypt <file>      Encrypt file
decrypt <file>      Decrypt file
safe-mode           Start safe mode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FUN / HACKER
matrix              Matrix effect
terminal-rain       Terminal rain animation
ascii               ASCII tools
quote               Random quote
joke                Random joke

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type:
man <command>

Example:
man ls

For detailed command information.

Devcore CLI OS ready.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
    elif command == "manual":
        print("""
╔══════════════════════════════════════════════════════╗
║                 DEVCORE CLI OS                      ║
║        Python Powered Terminal Environment          ║
╚══════════════════════════════════════════════════════╝

Devcore CLI OS is a lightweight Linux-inspired
terminal operating environment written in Python.

The system is designed for Raspberry Pi devices,
SSH workflows, development environments, networking,
automation and advanced command-line operations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM OVERVIEW

Devcore CLI OS provides a modular terminal experience
focused on performance, simplicity and expandability.

The environment is fully CLI-based and optimized
for low resource usage while still supporting
advanced workflows and development tools.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAIN FEATURES

• Fully terminal-based environment
• Python-powered architecture
• Linux-inspired command structure
• SSH-first workflow
• Lightweight and fast
• Modular command system
• Raspberry Pi optimized
• File system management
• Networking utilities
• Development tools
• Security utilities
• Hardware interaction support
• Expandable plugin support
• Hacker-style terminal effects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM DESIGN

Devcore CLI OS uses a modular architecture where
commands, tools and system utilities are separated
into different components for easier maintenance
and future expansion.

The system is designed to grow over time with:
- plugins
- AI tools
- automation systems
- remote administration
- advanced monitoring
- package management

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TARGET PLATFORM

Primary platform:
- Raspberry Pi 4

Supported workflows:
- SSH remote access
- Local terminal usage
- Development environments
- Server management
- Networking diagnostics
- Automation tasks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFORMANCE GOALS

• Low RAM usage
• Fast startup time
• Minimal CPU overhead
• Lightweight architecture
• Stable terminal workflow
• Expandable system core

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATUS

Devcore CLI OS environment initialized successfully.

System ready.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
        
    elif command == "clear":
        os.system("cls" if os.name == "nt" else "clear")
        
    elif command == "exit":
        print("CLIOS is closed")
        break
    
    elif command == "version":
        print(f"CLIOS version {version}")
    
    elif command == "about":
        print("""
╔══════════════════════════════════════════════════════╗
║                    ABOUT DEVCORE                    ║
╚══════════════════════════════════════════════════════╝

Devcore CLI OS is a custom Python-powered
terminal operating environment inspired by Linux systems.

The project focuses on creating a lightweight,
modular and expandable command-line platform
optimized for Raspberry Pi devices and SSH workflows.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT GOALS

• Build a fully terminal-based environment
• Create a Linux-inspired CLI architecture
• Support development and automation workflows
• Keep resource usage lightweight
• Provide expandable command modules
• Support future plugins and AI integration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNOLOGIES

• Python 3
• Linux command integration
• subprocess-based command execution
• Rich terminal formatting
• Modular command system
• Raspberry Pi support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT STATUS

Devcore CLI OS is currently in active development.

Features and commands may change over time as
the platform expands with new modules and tools.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESIGNED FOR

• Raspberry Pi
• SSH environments
• Developers
• Terminal enthusiasts
• Lightweight systems
• Automation workflows

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Devcore CLI OS
Python Powered Terminal Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
    
    elif command.startswith("echo "):
        text = command.replace("echo ", "", 1)
        print(text)
        
    elif command.startswith("calc "):
        som = command.replace("calc ", "", 1)
        som = som.replace("x", "*")
        som = som.replace("X", "*")

        try:
            resultaat = eval(som)
            print(resultaat)
        except:
            print("Fout in som. G ebruik bijvoorbeeld: calc 10*5 of calc 10+5")
    
    elif command == "random":
        getal = random.randint(1, 100)
        print(getal)

    elif command == "uuid":
        unieke_id = uuid.uuid4()
        print(unieke_id)
        
    elif command =="calc":
        print(
"""calc <expression> # evaluates a mathematical expression

Examples:
calc 1+1
calc 10*5
calc 100/4
calc 12-7
calc 345x45
calc (5+3)*2

Supported operators:
+   addition
-   subtraction
*   multiplication
x   multiplication
/   division
()  grouping expressions

Example output:
clios@pi$ calc 5+5
10

The calc command uses Python expression evaluation
to process mathematical operations directly inside Devcore CLI OS.""")


# dat waren alle core commands
# nu komen de user and session commands
    elif command == "whoami":
        print(username)
        
    elif command == "id":
        print(user_id)
        
# The code snippet you provided is implementing functionality to add users and display user
# information in your Python program. Here's a breakdown of what each part of the code does:
    elif command == "adduser":
        nuser_name = input("name: ")
        nuser_age = input("age: ")
        nuser_job = input("job (optional): ")
        nuser_phone = input("phone_number (optional): ")

        users.append({
            "name": nuser_name,
            "age": nuser_age,
            "job": nuser_job,
            "phone": nuser_phone
        })

        print("User added:", nuser_name)

    elif command == "users":
        print("Main user:", username)

        if len(users) == 0:
            print("No extra users added yet.")
        else:
            print("Extra users:")
            for user in users:
                print("-", user["name"], "| age:", user["age"], "| job:", user["job"], "| phone:", user["phone"])
                
# The above code snippet is for a Python script that handles the "hostname edit" command. When this
# command is executed, the script prompts the user to enter a new hostname. It then updates the
# configuration file with the new hostname and saves the changes by writing the updated configuration
# to the file using JSON format with an indent of 4 spaces. Finally, it prints a message confirming
# that the hostname has been changed to the new value entered by the user.
    elif command == "hostname edit":
        hostname = input("Enter your new hostname: ")
        config[hostname] = hostname
        
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

        print("Hostname changed to:", hostname)

# The above code snippet is a part of a Python script. It is checking if the `command` variable is
# equal to the string "hostname". If the condition is true, it will print the value of the `hostname`
# variable.
    elif command == "hostname":
        print(hostname)
        
# The above code snippet is a part of a Python script that handles different commands related to time
# and date. Here's a breakdown of what each part does:
# The code snippet is a part of a Python script. It is checking if the variable `command` is equal to
# the string "time". If it is, then it prints the current time in the format HH:MM:SS using the
# `datetime` module in Python.
    elif command == "time" or command == "clock":
        print(datetime.now().strftime("%H:%M:%S"))
        
# The code snippet is a part of a Python script that includes a conditional block checking if the
# `command` variable is equal to "date". If the condition is met, it prints the current date in the
# format "YYYY-MM-DD" using the `datetime` module in Python.
    elif command == "date":
        print(datetime.now().strftime("%Y-%m-%d"))
    
# The code snippet is checking if the `command` variable is equal to "calender" (typo: should be
# "calendar"). If the condition is true, it retrieves the current date and time using
# `datetime.now()`, formats the date as "dd-mm-yyyy" using `strftime`, and then prints the formatted
# date.
    elif command == "calender":
        today = datetime.now()
        date_format = today.strftime("%d-%m-%Y")
        print(date_format)
        

# dat waren de de date and time commando's
# nu de system commando's

    elif command == "sysinfo":
        print("╔════════════════════════════╗")
        print("║        SYSTEM INFO         ║")
        print("╚════════════════════════════╝")

        print("Hostname:", hostname)
        print("Username:", username)
        print("User ID:", user_id)

        print("\nSYSTEM")
        print("OS:", platform.system())
        print("OS Version:", platform.version())
        print("Architecture:", platform.machine())
        print("Python Version:", platform.python_version())

        print("\nHARDWARE")
        print("CPU Cores:", psutil.cpu_count())
        print("CPU Usage:", str(psutil.cpu_percent(interval=1)) + "%")

        ram = psutil.virtual_memory()
        print("RAM Usage:", round(ram.used / 1024 / 1024 / 1024, 2), "GB /", round(ram.total / 1024 / 1024 / 1024, 2), "GB")

        disk = psutil.disk_usage("/")
        print("Disk Usage:", round(disk.used / 1024 / 1024 / 1024, 2), "GB /", round(disk.total / 1024 / 1024 / 1024, 2), "GB")
        
# The code is checking the operating system using the `platform.system()` function. If the system is
# Linux, it runs the command `vcgencmd measure_temp` using `subprocess.run()` to measure the
# temperature. If the system is not Linux, it prints a message saying that the temperature command is
# only available on Raspberry Pi.
    elif command == "temp":
        if platform.system() == "Linux":
            subprocess.run(["vcgencmd", "measure_temp"])
        else:
            print("Temperature command is only available on Raspberry Pi.")
    
    elif command == "ls":
        subprocess.run(["ls"])
        
    elif command.startswith("cd "):
        folder = command.replace("cd ", "", 1)

        try:
            os.chdir(folder)
            print("Current directory:", os.getcwd())
        except Exception as error:
            print("Folder not found:", error)

    elif command.startswith("mkdir "):
        folder = command.replace("mkdir ", "", 1)

        try:
            os.mkdir(folder)
            print("Folder created:", folder)
        except Exception as error:
            print("Could not create folder:", error)

    elif command.startswith("rmdir "):
        folder = command.replace("rmdir ", "", 1)

        try:
            os.rmdir(folder)
            print("Folder removed:", folder)
        except Exception as error:
            print("Could not remove folder:", error)

    elif command.startswith("create "):
        file = command.replace("create ", "", 1)

        try:
            open(file, "w").close()
            print("File created:", file)
        except Exception as error:
            print("Could not create file:", error)
    
# The code snippet is checking if the `command` starts with "cat " (including a space after "cat"). If
# it does, it extracts the file name from the command by removing "cat " from the beginning of the
# command. Then, it uses the `subprocess.run` function to execute the `cat` command in the terminal
# with the specified file as an argument, effectively displaying the contents of the file on the
# terminal.
    elif command.startswith("cat "):
        file = command.replace("cat ", "", 1)
        
        subprocess.run(["cat", file])
    
    elif command.startswith("nano "):
        file = command.replace("nano", "", 1)
        
        subprocess.run(["nano", file])
        
    