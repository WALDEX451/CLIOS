# Devcore CLI OS — COMMANDS.md

> Een volledig terminal-based CLI-systeem in Python.  
> Gemaakt voor Raspberry Pi, SSH, Linux-commando’s, bestanden, netwerk, systeembeheer en dev-tools.

---

# 🖥️ CORE COMMANDS

```bash
help # laat hulp zien
manual # opent de handleiding
clear # maakt het scherm leeg
exit # sluit Devcore CLI af
version # toont de versie
about # toont info over Devcore CLI
echo <text> # print tekst
calc <som> # rekent een som uit
random # maakt een willekeurig getal
uuid # maakt een unieke ID
```

---

# 👤 USER & SESSION

```bash
whoami # toont huidige gebruiker
id # toont gebruikers-ID
users # toont gebruiker
adduser # maakt nieuwe gebruiker
hostname # toont apparaatnaam
hostname edit # verandert naam van de hele computer
```

---

# ⏰ TIME & DATE

```bash
time # toont huidige tijd
date # toont huidige datum
calendar # toont kalender
clock # toont klok
```

---

# 🖥️ SYSTEM INFORMATION

```bash
sysinfo # toont volledig systeemoverzicht
```

---

# 📁 FILE SYSTEM

```bash
ls # toont bestanden
cd <folder> # gaat naar map
mkdir <name> # maakt map
rmdir <name> # verwijdert lege map
create <file> # maakt bestand, bijvoorbeeld create bestand.py
cat <file> # leest bestand
less <file> # opent bestand leesbaar
nano <file> # opent nano-editor
rm <file> # verwijdert bestand
cp <source> <destination> # kopieert bestand
cp -r <source> <destination> # kopieert map
mv <source> <destination> # verplaatst bestand/map
rename <old> <new> # hernoemt bestand/map
find <name> # zoekt bestand
search <word> # zoekt tekst of naam
size <file> # toont bestandsgrootte
df # toont vrije schijfruimte
zip <file> # maakt zipbestand
unzip <file> # pakt zipbestand uit
tar <file> # maakt tar-archief
extract <file> # pakt archief uit
checksum <file> # maakt controlecode
md5 <file> # maakt MD5-hash
sha256 <file> # maakt SHA256-hash
fileinfo <file> # toont bestandinfo
filetype <file> # toont bestandstype
backup <folder> # maakt backup
restore <backup> # zet backup terug
```

---

# 🌐 NETWORKING

```bash
ip # toont IP-adres
wifi # toont wifi-status
wifi scan # zoekt wifi-netwerken
wifi connect <name> # verbindt met wifi
wifi disconnect # verbreekt wifi
ping <host> # test verbinding
traceroute <host> # toont route naar host
dns <host> # zoekt DNS-info
ports # toont poorten
scan # scant netwerk
arp # toont apparaten in netwerk
route # toont netwerkroute
gateway # toont gateway
mac # toont MAC-adres
netstat # toont netwerkverbindingen
speedtest # test internetsnelheid
ssh <user@host> # verbindt via SSH
scp <file> <target> # kopieert via SSH
rsync <source> <target> # synchroniseert bestanden
curl <url> # haalt webdata op
wget <url> # downloadt bestand
```

---

# ⚙️ PROCESSES & SERVICES

```bash
ps # toont processen
top # toont live processen
htop # opent betere taakmonitor
kill <pid> # stopt proces
killall <name> # stopt processen met naam
jobs # toont achtergrondtaken
bg # zet taak op achtergrond
fg # haalt taak naar voorgrond
services # toont services
service <name> # toont service-info
systemctl <action> <service> # beheert systemd-service
journal # toont systeemlogboek
logs <name> # toont logs
watch <command> # herhaalt commando live
```

---

# 📦 PACKAGES

```bash
apt update # vernieuwt pakketlijst
apt upgrade # installeert updates
apt install <package> # installeert pakket
apt remove <package> # verwijdert pakket
apt search <name> # zoekt pakket
apt list # toont pakketten
pip install <package> # installeert Python-package
pip remove <package> # verwijdert Python-package
pip list # toont Python-packages
venv # toont virtual environment-info
requirements # maakt of leest requirements.txt
```

---

# 🐍 PYTHON & DEVELOPMENT

```bash
python # opent Python
python3 # opent Python 3
pyver # toont Python-versie
run <file.py> # start Python-bestand
compile <file.py> # compileert Python-bestand
debug <file.py> # debugt Python-bestand
git # toont git-hulp
git clone <url> # downloadt repository
git pull # haalt updates op
git push # uploadt wijzigingen
git status # toont git-status
git commit # maakt commit
project # toont projecten
workspace # opent werkruimte
```

---

# 🔒 SECURITY

```bash
firewall # toont firewallstatus
ufw # beheert firewall
guardian # toont DE ETHISCHE BEVEILIGER status
guardian on # zet hardened mode aan
guardian off # zet hardened mode uit
guardian seal # forceert hardened profiel
mitm-check <host> # controleert TLS en SSH-identiteit tegen MITM-risico
ssh-fingerprint <host> # toont SSH host key fingerprint
security-tools # toont beschikbare ethical hacking tools
scanports # scant localhost
scanports <host> # scant geautoriseerde host
recon <host> # basic host discovery
service-scan <host> # service fingerprinting met nmap
http-headers <url-or-host> # inspecteert response headers
tls-check <host> # controleert TLS en certificaat
wifi-audit # inspecteert lokaal draadloos netwerk
hash <text> # maakt hash
encrypt <file> # versleutelt bestand
decrypt <file> # ontsleutelt bestand
keys # toont sleutels
ssh-keygen # maakt SSH-key
auth # toont authenticatie-info
safe-mode # start veilige modus
lockdown # zet strenge beveiliging aan
audit # controleert systeemveiligheid
```

---

# 🔌 RASPBERRY PI HARDWARE

```bash
gpio # toont GPIO-info
gpio read <pin> # leest GPIO-pin
gpio write <pin> <value> # schrijft naar GPIO-pin
gpio mode <pin> <mode> # zet GPIO-modus
i2c # toont I2C-info
spi # toont SPI-info
usb # toont USB-apparaten
bluetooth # toont bluetooth-status
audio # toont audioapparaten
camera # checkt camera
screen # toont scherminfo
hdmi # toont HDMI-info
fan # toont ventilatorinfo
led # bestuurt LED
sensor # leest sensor
```

---

# 🧠 TERMINAL TOOLS

```bash
notes # opent notities
note add # voegt notitie toe
todo # toont takenlijst
todo add # voegt taak toe
todo done # markeert taak klaar
journal # opent dagboek
weather # toont weer
news # toont nieuws
rss # toont RSS-feeds
quote # toont quote
joke # toont grap
ascii # maakt ASCII-art
qr # maakt QR-code
matrix # start Matrix-effect
terminal-rain # start regen-effect
glitch # start glitch-effect
decode # decodeert tekst
encode # encodeert tekst
hex # zet om naar hex
base64 # zet om naar base64
```

---

# 📡 SERVER & REMOTE

```bash
server start # start server
server stop # stopt server
server restart # herstart server
server status # toont serverstatus
host # toont host-info
webserver # start simpele webserver
flask # start Flask-app
fastapi # start FastAPI-app
socket # test socketverbinding
api # toont API-info
sqlite # opent SQLite
database # toont database-tools
remote # toont remote-info
sync # synchroniseert data
upload # uploadt bestand
download # downloadt bestand
```

---

# 🔧 SYSTEM CONTROL

```bash
reboot # herstart systeem
shutdown # sluit systeem af
poweroff # zet systeem uit
sleep # zet systeem in slaapstand
restart-network # herstart netwerk
safe-reboot # veilige herstart
emergency # noodmodus
recovery # herstelmodus
snapshot # maakt systeemmomentopname
```

---

# 🎨 CUSTOMIZATION

```bash
theme # toont thema
theme dark # zet donker thema
theme hacker # zet hacker-thema
theme matrix # zet matrix-thema
theme minimal # zet minimal-thema
colors # past kleuren aan
font # past lettertype aan
prompt # past prompt aan
animations # zet animaties aan/uit
```

---


# 🚀 FUTURE FEATURES

- Plugin system
- Multi-user environment
- SSH remote administration
- AI assistant
- Local LLM support
- Ollama integration
- Raspberry Pi monitoring
- Remote device control
- Package repository
- Custom shell language
- Theme engine
- ASCII UI framework
- Terminal notifications
- API integrations

---

# 📂 PROJECT STRUCTURE

```text
Devcore-cli/
├── main.py
├── commands/
├── core/
├── system/
├── network/
├── security/
├── hardware/
├── packages/
├── themes/
├── plugins/
├── logs/
├── data/
├── config/
├── assets/
└── users/
```

---

# ⚡ DESIGN GOALS

- Fully CLI-based
- Linux-inspired architecture
- Lightweight
- SSH-first workflow
- Python-powered
- Raspberry Pi optimized
- Modular command system
- No duplicate command sections
- Clear command explanations
- Fast startup
- Low RAM usage
