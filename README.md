# CLIOS

> A futuristic open-source terminal operating system built in Python for Raspberry Pi, Linux, and developer experiments.
>
> Hardened mode: **DE ETHISCHE BEVEILIGER** for defensive, authorized security workflows.

![Python](https://img.shields.io/badge/Python-3-blue)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi-lightgrey)
![License](https://img.shields.io/badge/license-open--source-brightgreen)

## What is CLIOS?

CLIOS is an experimental command-line operating environment written in Python.

It combines:

* Linux-style terminal commands
* A custom Python kernel system
* File management
* User management
* Product browsing tools
* Storage systems
* Raspberry Pi support
* Authorized security auditing
* Open-source experimentation
* Future AI integration

The project is focused on learning, building, experimenting, and creating a futuristic developer environment.

---

# Features

## Current Features

* Custom CLI shell
* Username + hostname system
* Config file system
* Password support
* File creation
* Folder creation/removal
* Browse/search tools
* Linux command support
* Python kernel structure
* Raspberry Pi compatibility
* Storage system
* Loading animations
* SSH deployment support
* GitHub update workflow
* Ethical security recon and audit commands

---

# Planned Features

* AI assistant integration
* Plugin system
* Networking tools
* Package manager
* GUI mode
* Custom app ecosystem
* Cloud syncing
* Remote device management
* Multi-device storage
* System monitor
* Web dashboard
* Smart terminal themes
* Developer APIs

---

# Screenshots

Coming soon.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/WALDEX451/CLIOS.git
cd CLIOS
```

## Install Dependencies

### Debian / Raspberry Pi OS

Plug-and-play setup:

```bash
chmod +x setup_pi.sh clios
./setup_pi.sh
./clios
```

Manual package list used by the setup script:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nmap ufw net-tools iproute2 wireless-tools iw curl openssl -y
pip3 install rich psutil
```

---

# Start CLIOS

```bash
python3 main.py
```

---

# Raspberry Pi Setup

CLIOS is designed to work on Raspberry Pi systems.

After copying the repository to the Pi, setup is:

```bash
cd ~/CLIOS
chmod +x setup_pi.sh clios
./setup_pi.sh
./clios
```

Example deployment:

```bash
scp -r . ewout@raspberrypi:/home/ewout/CLIOS
```

SSH into the Pi:

```bash
ssh ewout@raspberrypi
cd ~/CLIOS
./setup_pi.sh
./clios
```

---

# Updating CLIOS

```bash
git pull
```

---

# Example Commands

```bash
ls
cd folder
mkdir test
rmdir test
create file.txt
cat file.txt
browse
security-tools
audit
scanports 127.0.0.1
recon 192.168.1.0/24
service-scan 192.168.1.1
wifi-audit
```

---

# Ethical Security Mode

CLIOS can be used as an authorized security toolkit on Raspberry Pi and Linux systems.

Included defensive workflows:

* `guardian` to show hardened security posture
* `guardian on` to enforce HTTPS/TLS/host-key hygiene
* `guardian seal` to apply the hardened guardian profile
* `mitm-check <host>` for TLS + SSH fingerprint verification
* `ssh-fingerprint <host>` to inspect SSH host identity
* `security-tools` to detect installed security utilities
* `audit` for host firewall, listening ports and SSH posture
* `scanports <host>` for authorized port scanning
* `recon <host>` for basic host discovery
* `service-scan <host>` for service fingerprinting with `nmap`
* `http-headers <host>` for HTTP security header inspection
* `tls-check <host>` for certificate and TLS handshake checks
* `wifi-audit` for local wireless inspection on Raspberry Pi/Linux

Use these commands only on systems and networks where you have explicit permission.

---

# Start And Play

For Raspberry Pi the first run is now non-interactive:

* `setup_pi.sh` installs packages and creates a virtual environment
* `config.json` is generated automatically with Pi defaults
* `./clios` starts CLIOS directly
* `clios.service` is generated automatically if you want systemd autostart

---

# Project Goals

CLIOS is not meant to be just another terminal.

The goal is to build:

* a futuristic command environment
* an educational open-source project
* a Raspberry Pi development platform
* an experimental operating environment
* a foundation for future AI systems

---

# Why This Project Exists

CLIOS started as a learning project focused on:

* Python programming
* Linux systems
* Raspberry Pi development
* terminals and shells
* storage systems
* networking
* open-source software
* future AI experiments

The project continues to grow step-by-step.

---

# Open Source

This project is open source.

Feel free to:

* fork the project
* improve the code
* suggest features
* experiment with the system
* build your own version

---

# Contributing

Pull requests and ideas are welcome.

If you find bugs or have feature ideas:

* open an issue
* create a fork
* submit improvements

---

# Developer

Created by Ewout Rutges.

Focused on:

* Python
* Raspberry Pi
* Linux
* AI
* terminal systems
* experimental technology

---

# License

This project is open source.

You may modify and experiment with the code.

---

# Star The Project

If you think CLIOS is interesting:

⭐ Star the repository
🍴 Fork the project
🚀 Follow future updates
