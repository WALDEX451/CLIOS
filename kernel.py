# kernel.py
import os
import time
import sys
import hashlib
import subprocess
import urllib.request
import re
import getpass

class Kernel:
    def __init__(self, config, version):
        # 1. EERST de basisgegevens uit de config inladen
        self.config   = config
        self.version  = version
        self.username = config["username"]
        self.hostname = config["hostname"]
        self.user_id  = config["user_id"]
        self.users    = []
        self.running  = False
        self.devices  = {}
        print(f"[KERNEL] Geïnitialiseerd voor {self.username}@{self.hostname}")
        
        # 2. PAS DAARNA de UI en Thema Instellingen
        self.animations_enabled = True
        self.current_theme = "standard"
        
        # ANSI Kleurcodes database
        self.colors_dict = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "green": "\033[32m",
            "dark_green": "\033[2;32m",
            "black_bg": "\033[40m",
            "white": "\033[37m",
            "cyan": "\033[36m",
            "red": "\033[31m",
            "purple": "\033[35m",
            "yellow": "\033[33m"
        }
        
        # De standaard opstartprompt
        self.custom_prompt = f"{self.username}@{self.hostname}> "

    # 3. INTERNE UTILITIES
    def loading_bar(self, total=20):
        """Toont een visuele laadbalk in de CLI."""
        if not self.animations_enabled:
            return
        for i in range(total + 1):
            done = "#" * i
            left = "." * (total - i)
            percent = int((i / total) * 100)
            print(f"\rLoading: [{done}{left}] {percent}%", end="", flush=True)
            time.sleep(0.1)
        print()

    def is_raspberry_pi(self):
        """Controleert of het besturingssysteem op een echte Raspberry Pi draait."""
        try:
            if os.path.exists("/proc/device-tree/model"):
                with open("/proc/device-tree/model", "r") as f:
                    return "Raspberry Pi" in f.read()
        except Exception:
            pass
        return False

    # 4. DRIVER COMMUNICATIE
    def register_device(self, name, device_object):
        """Registreert een hardware driver bij de kernel."""
        self.devices[name] = device_object
        print(f"[KERNEL] Driver '{name}' succesvol geladen.")

    def execute_print(self, filename):
        """Stuurt de printopdracht door naar de geladen driver."""
        if "printer" not in self.devices:
            print("Fout: Geen printerdriver geladen in het systeem!")
            return
        try:
            with open(filename, 'r') as f:
                content = f.read()
            printer = self.devices["printer"]
            printer.connect()
            printer.print_text(content)
        except FileNotFoundError:
            print(f"Fout: Bestand '{filename}' niet gevonden.")

    # 5. DE CORE RUN LOOP
    def run(self):
        self.running = True
        
        # Nu mét self. en de laadbalk-functie bestaat hierboven weer!
        self.loading_bar()
        print(f"[KERNEL] CLIOS v{self.version} actief")

        while self.running:
            # Nu mét de dynamische custom_prompt zodat thema's werken!
            command = input(self.custom_prompt).strip()
            
            if not command:
                continue
                
            # --- Vanaf hier lopen al jouw eigen elif-commando's (cp, mv, browse, etc.) verder ---


            # ─────────────── BASIC COMMANDS ───────────────
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

Type:
man <command>

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

STATUS

Devcore CLI OS environment initialized successfully.
System ready.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif command == "exit":
                print("CLIOS is closed")
                self.running = False

            elif command == "version":
                print(f"CLIOS version {self.version}")

            elif command == "about":
                print("""
╔══════════════════════════════════════════════════════╗
║                    ABOUT DEVCORE                    ║
╚══════════════════════════════════════════════════════╝

Devcore CLI OS is a custom Python-powered
terminal operating environment inspired by Linux systems.

Devcore CLI OS
Python Powered Terminal Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

            # ─────────────── ECHO / CALC / RANDOM / UUID ───────────────
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
                    print("Fout in som. Gebruik bijvoorbeeld: calc 10*5 of calc 10+5")

            elif command == "random":
                getal = random.randint(1, 100)
                print(getal)

            elif command == "uuid":
                unieke_id = uuid.uuid4()
                print(unieke_id)

            elif command == "calc":
                print("""calc <expression> # evaluates a mathematical expression

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
()  grouping expressions""")

            # ─────────────── USER & SESSION ───────────────
            elif command == "whoami":
                print(self.username)

            elif command == "id":
                print(self.user_id)

            elif command == "adduser":
                nuser_name  = input("name: ")
                nuser_age   = input("age: ")
                nuser_job   = input("job (optional): ")
                nuser_phone = input("phone_number (optional): ")

                self.users.append({
                    "name":  nuser_name,
                    "age":   nuser_age,
                    "job":   nuser_job,
                    "phone": nuser_phone,
                })
                print("User added:", nuser_name)

            elif command == "users":
                print("Main user:", self.username)
                if len(self.users) == 0:
                    print("No extra users added yet.")
                else:
                    print("Extra users:")
                    for user in self.users:
                        print("-", user["name"], "| age:", user["age"],
                              "| job:", user["job"], "| phone:", user["phone"])

            elif command == "hostname edit":
                new_hostname = input("Enter your new hostname: ")
                self.hostname = new_hostname
                self.config["hostname"] = new_hostname

                with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                    json.dump(self.config, file, indent=4)
                print("Hostname changed to:", new_hostname)

            elif command == "hostname":
                print(self.hostname)

            # ─────────────── DATE / TIME ───────────────
            elif command == "time" or command == "clock":
                print(datetime.now().strftime("%H:%M:%S"))

            elif command == "date":
                print(datetime.now().strftime("%Y-%m-%d"))

            elif command == "calender":
                today = datetime.now()
                date_format = today.strftime("%d-%m-%Y")
                print(date_format)

            # ─────────────── SYSTEM ───────────────
            elif command == "sysinfo":
                print("╔════════════════════════════╗")
                print("║        SYSTEM INFO         ║")
                print("╚════════════════════════════╝")
                print("Hostname:", self.hostname)
                print("Username:", self.username)
                print("User ID:", self.user_id)

                print("\nSYSTEM")
                print("OS:", platform.system())
                print("OS Version:", platform.version())
                print("Architecture:", platform.machine())
                print("Python Version:", platform.python_version())

                print("\nHARDWARE")
                print("CPU Cores:", psutil.cpu_count())
                print("CPU Usage:", str(psutil.cpu_percent(interval=1)) + "%")

                ram = psutil.virtual_memory()
                print("RAM Usage:",
                      round(ram.used / 1024 / 1024 / 1024, 2), "GB /",
                      round(ram.total / 1024 / 1024 / 1024, 2), "GB")

                disk = psutil.disk_usage("/")
                print("Disk Usage:",
                      round(disk.used / 1024 / 1024 / 1024, 2), "GB /",
                      round(disk.total / 1024 / 1024 / 1024, 2), "GB")

            elif command == "temp":
                if platform.system() == "Linux":
                    subprocess.run(["vcgencmd", "measure_temp"])
                else:
                    print("Temperature command is only available on Raspberry Pi.")

            # ─────────────── FILES ───────────────
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

            elif command.startswith("cat "):
                file = command.replace("cat ", "", 1)
                subprocess.run(["cat", file])

            elif command.startswith("nano "):
                file = command.replace("nano ", "", 1)   # ← bug fix: spatie toegevoegd
                subprocess.run(["nano", file])
                    
            
            if command.startswith("cp "):
                # 1. Haal "cp " weg aan het begin en splits de rest op de spatie
                parts = command[3:].strip().split(" ")
                
                # 2. Controleer of de gebruiker wel een bron én bestemming heeft ingevuld
                if len(parts) < 2:
                    print("Error: use 'cp <file> <destination>'")
                else:
                    rfile = parts[0]        # Het eerste woord is het bronbestand
                    destination = parts[1]  # Het tweede woord is de bestemming
                    
                    # 3. Voer het echte Mac/Linux cp commando uit via subprocess
                    subprocess.run(["cp", rfile, destination])
                    
            elif command.startswith("cp -r "):
                # 1. Snijd de eerste 6 tekens ("cp -r ") eraf en splits op de spatie
                parts = command[6:].strip().split(" ")
                
                # 2. Controleer of de gebruiker bron én bestemming heeft ingevuld
                if len(parts) < 2:
                    print("Error: use 'cp -r <folder> <destination>'")
                else:
                    folder = parts[0]       # De bronmap
                    destination = parts[1]  # De bestemmingsmap
                    
                    # 3. Voeg "-r" toe aan de subprocess lijst voor recursief kopiëren
                    subprocess.run(["cp", "-r", folder, destination])

                    
            elif command == "cp":
                print("     you can use CP for copy a folder or file")
                print("     example:")
                print("     cp <file> <destination> for a file")
                print("     and")
                print("     cp -r <folder> <destination> for a folder.")
                
            elif command == "cd":
                print("""cd stands for: "change directory" """)
                print("example:")
                print("cd yourfolder")
                print("""now the directory was changed to: "yourfolder" """)
                
                        # --- MV (Verplaatsen of Hernoemen) ---
            elif command.startswith("mv "):
                # Snijd "mv " (3 tekens) eraf en splits op spatie
                parts = command[3:].strip().split(" ")
                
                if len(parts) < 2:
                    print("Error: use 'mv <source> <destination>'")
                else:
                    source = parts[0]
                    destination = parts[1]
                    # Voert het Mac mv commando uit
                    subprocess.run(["mv", source, destination])

            # --- RM -R (Map verwijderen) ---
            elif command.startswith("rm -r "):
                # Snijd "rm -r " (6 tekens) eraf
                target_folder = command[6:].strip()
                
                if not target_folder:
                    print("Error: use 'rm -r <folder>'")
                else:
                    # Voert rm -r uit voor mappen
                    subprocess.run(["rm", "-r", target_folder])

            # --- RM (Bestand verwijderen) ---
            elif command.startswith("rm "):
                # Snijd "rm " (3 tekens) eraf
                target_file = command[3:].strip()
                
                if not target_file:
                    print("Error: use 'rm <file>'")
                else:
                    # Voert rm uit voor losse bestanden
                    subprocess.run(["rm", target_file])
                    
                        # --- RENAME (Bestand of map hernoemen) ---
            elif command.startswith("rename "):
                # Snijd "rename " (7 tekens) eraf en splits op de spatie
                parts = command[7:].strip().split(" ")
                
                if len(parts) < 2:
                    print("Error: use 'rename <old_name> <new_name>'")
                else:
                    old_name = parts[0]
                    new_name = parts[1]
                    
                    # Mac gebruikt 'mv' om bestanden te hernoemen
                    subprocess.run(["mv", old_name, new_name])
                    
            elif command.startswith("find "):
                found = command.replace("find ", "", 1).strip()
                
                if not found:
                    print("Error: use 'find <filename>'")
                else:
                    # Zoekt vanaf de huidige map (.) naar de ingevulde naam
                    subprocess.run(["find", ".", "-name", found])
                    
                        # --- SIZE (Toont bestandsgrootte in bytes) ---
            elif command.startswith("size "):
                target = command[5:].strip()
                
                if not target:
                    print("Error: use 'size <file_or_folder>'")
                else:
                    # -s = Geef 1 totaalbedrag voor mappen
                    # -h = Automatisch in KB, MB, GB tonen
                    subprocess.run(["du", "-sh", target])
                    
            elif command == "size":
                print("type size <file/folder> to see the size of the folder/file")
                    
            # --- DF (Toont beschikbare schijfruimte) ---
            elif command.startswith("df"):
                # Haal "df" eraf (2 tekens). Als er een map achter staat, pakken we die mee.
                target_path = command[2:].strip()
                
                if not target_path:
                    # Als de gebruiker puur 'df' typt, toon alle gekoppelde schijven
                    subprocess.run(["df", "-h"])
                else:
                    # Als de gebruiker 'df drivers' typt, toon de schijfruimte van die specifieke map
                    subprocess.run(["df", "-h", target_path])
                    
            elif command == "df -help":
                print("""if you type "df" in the console you see a the space you have fee to use """)
                
                        # --- ZIP (Maakt een zipbestand van een bestand) ---
            elif command.startswith("zip "):
                # Snijd "zip " (4 tekens) eraf
                target_file = command[4:].strip()
                
                if not target_file:
                    print("Error: use 'zip <filename>'")
                else:
                    # Maak automatisch de naam van het zipbestand (bijv. main.py.zip)
                    zip_name = f"{target_file}.zip"
                    
                    # Voer het Mac zip-commando uit
                    # Het argument "-q" (quiet) zorgt ervoor dat je Mac geen rommelige logs print
                    subprocess.run(["zip", "-q", zip_name, target_file])
                    print(f"Success: Created {zip_name}")
                    
                        # --- UNZIP (Pakt een zipbestand uit) ---
            elif command.startswith("unzip "):
                target_file = command[6:].strip()
                if not target_file:
                    print("Error: use 'unzip <filename.zip>'")
                else:
                    # -q zorgt voor een stille modus zonder overbodige tekst op je scherm
                    subprocess.run(["unzip", "-q", target_file])
                    print(f"Success: Extracted {target_file}")

            # --- TAR (Maakt een gecomprimeerd tar-archief van een bestand of map) ---
            elif command.startswith("tar "):
                target = command[4:].strip()
                if not target:
                    print("Error: use 'tar <file_or_folder>'")
                else:
                    tar_name = f"{target}.tar.gz"
                    # -c = create, -z = gzip compressie, -f = bestandnaam opgeven
                    subprocess.run(["tar", "-czf", tar_name, target])
                    print(f"Success: Created {tar_name}")

            # --- EXTRACT (Universeel uitpakken van .tar, .tgz of .gz bestanden) ---
            elif command.startswith("extract "):
                target_file = command[8:].strip()
                if not target_file:
                    print("Error: use 'extract <archive.tar.gz>'")
                else:
                    # -x = extract, -z = gzip decompressie, -f = bestandnaam opgeven
                    subprocess.run(["tar", "-xzf", target_file])
                    print(f"Success: Extracted {target_file}")

            # --- CHECKSUM (Maakt een standaard SHA1 controlecode van een bestand) ---
            elif command.startswith("checksum "):
                target_file = command[9:].strip()
                if not target_file:
                    print("Error: use 'checksum <filename>'")
                else:
                    try:
                        with open(target_file, "rb") as f:
                            # SHA1 wordt traditioneel veel gebruikt voor snelle bestand-checks
                            file_hash = hashlib.sha1(f.read()).hexdigest()
                        print(f"SHA1 Checksum: {file_hash}")
                    except FileNotFoundError:
                        print(f"Error: File '{target_file}' not found.")

            # --- MD5 (Maakt een MD5-hash van een bestand) ---
            elif command.startswith("md5 "):
                target_file = command[4:].strip()
                if not target_file:
                    print("Error: use 'md5 <filename>'")
                else:
                    try:
                        with open(target_file, "rb") as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        print(f"MD5 Hash: {file_hash}")
                    except FileNotFoundError:
                        print(f"Error: File '{target_file}' not found.")

            # --- SHA256 (Maakt een sterke SHA256-hash van een bestand) ---
            elif command.startswith("sha256 "):
                target_file = command[7:].strip()
                if not target_file:
                    print("Error: use 'sha256 <filename>'")
                else:
                    try:
                        with open(target_file, "rb") as f:
                            file_hash = hashlib.sha256(f.read()).hexdigest()
                        print(f"SHA256 Hash: {file_hash}")
                    except FileNotFoundError:
                        print(f"Error: File '{target_file}' not found.")

            # --- FILEINFO (Toont gedetailleerde systeeminformatie van een bestand) ---
            elif command.startswith("fileinfo "):
                target_file = command[9:].strip()
                if not target_file:
                    print("Error: use 'fileinfo <filename>'")
                else:
                    try:
                        info = os.stat(target_file)
                        print(f"--- File Information for '{target_file}' ---")
                        print(f"Size: {info.st_size} bytes")
                        print(f"Permissions (Mode): {oct(info.st_mode)}")
                        print(f"Last Modified: {time.ctime(info.st_mtime)}")
                        print(f"Last Accessed: {time.ctime(info.st_atime)}")
                    except FileNotFoundError:
                        print(f"Error: File '{target_file}' not found.")

            # --- FILETYPE (Toont wat voor soort bestand het echt is via de Mac) ---
            elif command.startswith("filetype "):
                target_file = command[9:].strip()
                if not target_file:
                    print("Error: use 'filetype <filename>'")
                else:
                    # Maakt gebruik van de ingebouwde Mac-intelligentie 'file'
                    subprocess.run(["file", target_file])

            # --- BACKUP (Kopieert een map direct naar je interne 'backup' map) ---
            elif command.startswith("backup "):
                target_folder = command[7:].strip()
                if not target_folder:
                    print("Error: use 'backup <folder_name>'")
                else:
                    # De bestemming wordt de backup-map die je al in je CLIOS-lijst had staan
                    destination = f"backup/{target_folder}_backup"
                    # -r zorgt dat alle submappen en bestanden meegaan
                    subprocess.run(["cp", "-r", target_folder, destination])
                    print(f"Success: Backup created at '{destination}'")

            # --- RESTORE (Zet een map vanuit de backup-map weer terug naar de hoofdmap) ---
            elif command.startswith("restore "):
                target_backup = command[8:].strip()
                if not target_backup:
                    print("Error: use 'restore <backup_folder_name>'")
                else:
                    # Zoekt de map op in je backup directory
                    source = f"backup/{target_backup}"
                    # Haalt de extensie '_backup' van de naam af voor de herstelplek
                    original_name = target_backup.replace("_backup", "")
                    
                    subprocess.run(["cp", "-r", source, original_name])
                    print(f"Success: Restored '{target_backup}' to '{original_name}'")
                    
                        # --- IP (Toont het lokale en externe IP-adres) ---
            elif command == "ip":
                print("--- Local IP Addresses ---")
                # Toont lokale IP's via ifconfig (filtert op 'inet ')
                subprocess.run(["sh", "-c", "ifconfig | grep 'inet ' | grep -v 127.0.0.1"])
                print("\n--- Public IP Address ---")
                # Haalt het externe IP op via een snelle web-api
                subprocess.run(["curl", "-s", "ifconfig.me"])
                print()

            # --- WIFI SCAN (Moet BOVEN wifi staan om conflicten te voorkomen) ---
            elif command.startswith("wifi scan"):
                print("[WIFI] Zoeken naar netwerken...")
                # macOS specifieke airport tool locatie voor scannen
                airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
                subprocess.run([airport_path, "-s"])

            # --- WIFI CONNECT ---
            elif command.startswith("wifi connect "):
                parts = command[13:].strip().split(" ")
                if not parts[0]:
                    print("Error: use 'wifi connect <network_name>'")
                else:
                    ssid = parts[0]
                    # Vraagt veilig het wifi-wachtwoord in de terminal
                    password = getpass.getpass(f"Wachtwoord voor {ssid}: ")
                    print(f"[WIFI] Verbinden met {ssid}...")
                    subprocess.run(["networksetup", "-settransparentwirelessnetworkbyname", "en0", ssid, password])

            # --- WIFI DISCONNECT ---
            elif command == "wifi disconnect":
                print("[WIFI] Verbinding verbreken...")
                # macOS truc: zet de wifi-interface even uit en aan om te verbreken
                subprocess.run(["networksetup", "-setairportpower", "en0", "off"])
                subprocess.run(["networksetup", "-setairportpower", "en0", "on"])

            # --- WIFI STATUS ---
            elif command == "wifi":
                # Toont de huidige wifi-naam (SSID) op macOS
                subprocess.run(["networksetup", "-getairportnetwork", "en0"])

            # --- PING ---
            elif command.startswith("ping "):
                host = command[5:].strip()
                if not host:
                    print("Error: use 'ping <host>'")
                else:
                    # '-c 4' stopt automatisch na 4 pakketjes (net als in Windows)
                    subprocess.run(["ping", "-c", "4", host])

            # --- TRACEROUTE ---
            elif command.startswith("traceroute "):
                host = command[11:].strip()
                if not host:
                    print("Error: use 'traceroute <host>'")
                else:
                    subprocess.run(["traceroute", host])

            # --- DNS (Zoekt DNS-info via 'nslookup') ---
            elif command.startswith("dns "):
                host = command[4:].strip()
                if not host:
                    print("Error: use 'dns <host>'")
                else:
                    subprocess.run(["nslookup", host])

            # --- PORTS (Toont open poorten waar je Mac nu naar luistert) ---
            elif command == "ports":
                print("[INFO] Open poorten controleren...")
                # Toont actieve luisterende internetverbindingen
                subprocess.run(["lsof", "-i", "-P", "-n", "|", "grep", "LISTEN"], shell=True)

            # --- SCAN (Scant je lokale netwerk op actieve IP-adressen) ---
            elif command == "scan":
                print("[INFO] Lokale netwerkscan starten (ping sweep)...")
                # Haalt je eigen netwerkrang op en scant de eerste 10 IP's als snelle test
                # Voor een volledige scan is 'nmap' nodig, dit is de ingebouwde lichte variant:
                subprocess.run(["arp", "-a"])

            # --- ARP (Toont de ARP-tabel van apparaten in je netwerk) ---
            elif command == "arp":
                subprocess.run(["arp", "-a"])

            # --- ROUTE (Toont de huidige routing-tabel) ---
            elif command == "route":
                # 'netstat -nr' toont de routing tabellen op macOS
                subprocess.run(["netstat", "-nr"])

            # --- GATEWAY (Toont het IP-adres van je router) ---
            elif command == "gateway":
                # Vraagt de default gateway op via de macOS systeemconfiguratie
                subprocess.run(["sh", "-c", "route -n get default | grep gateway"])

            # --- MAC (Toont het fysieke MAC-adres van je wifi-kaart) ---
            elif command == "mac":
                # Filtert het hardwareadres uit de en0 (wifi) interface
                subprocess.run(["sh", "-c", "ifconfig en0 | grep ether"])

            # --- NETSTAT ---
            elif command == "netstat":
                subprocess.run(["netstat", "-at"])

            # --- SPEEDTEST (Simuleert of gebruikt de ingebouwde macOS netwerk kwaliteitstest) ---
            elif command == "speedtest":
                print("[INFO] Internetsnelheid testen via macOS NetworkQuality...")
                # 'networkquality' is sinds macOS Monterey standaard ingebouwd!
                subprocess.run(["networkquality"])

            # --- SSH ---
            elif command.startswith("ssh "):
                target = command[4:].strip()
                if not target:
                    print("Error: use 'ssh <user@host>'")
                else:
                    # Dit opent een live interactieve SSH-sessie in je eigen CLI
                    subprocess.run(["ssh", target])

            # --- SCP ---
            elif command.startswith("scp "):
                parts = command[4:].strip().split(" ")
                if len(parts) < 2:
                    print("Error: use 'scp <local_file> <user@host:/path>'")
                else:
                    subprocess.run(["scp", parts[0], parts[1]])

            # --- RSYNC ---
            elif command.startswith("rsync "):
                parts = command[6:].strip().split(" ")
                if len(parts) < 2:
                    print("Error: use 'rsync <source> <target>'")
                else:
                    # '-avz' staat for archive mode, verbose, compressed
                    subprocess.run(["rsync", "-avz", parts[0], parts[1]])

            # --- CURL ---
            elif command.startswith("curl "):
                url = command[5:].strip()
                if not url:
                    print("Error: use 'curl <url>'")
                else:
                    subprocess.run(["curl", url])

            # --- WGET ---
            elif command.startswith("wget "):
                url = command[5:].strip()
                if not url:
                    print("Error: use 'wget <url>'")
                else:
                    # Omdat macOS standaard geen 'wget' heeft, gebruiken we curl als slimme vervanger (-O downloadt het bestand)
                    print(f"[DOWNLOAD] Bestand downloaden van {url}...")
                    subprocess.run(["curl", "-O", url])
                    
                        # --- PS (Toont actieve processen van de huidige gebruiker) ---
            elif command == "ps":
                # -f toont volledige details zoals PID, starttijd en het commando
                subprocess.run(["ps", "-f"])

            # --- TOP (Toont live proces- en geheugengebruik) ---
            elif command == "top":
                # Start de interactieve live monitor direct in je CLI
                subprocess.run(["top"])

            # --- HTOP (Opent de geavanceerde taakmonitor als deze is geïnstalleerd) ---
            elif command == "htop":
                try:
                    subprocess.run(["htop"])
                except FileNotFoundError:
                    print("Error: 'htop' is niet geïnstalleerd op je Mac. Gebruik 'top'.")

            # --- KILLALL (Moet BOVEN kill staan om conflicten te voorkomen) ---
            elif command.startswith("killall "):
                proc_name = command[8:].strip()
                if not proc_name:
                    print("Error: use 'killall <process_name>'")
                else:
                    subprocess.run(["killall", proc_name])

            # --- KILL (Beëindigt een proces op basis van het Process ID) ---
            elif command.startswith("kill "):
                pid = command[5:].strip()
                if not pid:
                    print("Error: use 'kill <pid>'")
                else:
                    subprocess.run(["kill", pid])

            # --- JOBS (Toont achtergrondtaken van deze Python-sessie) ---
            elif command == "jobs":
                print("[INFO] Let op: Python subprocesses draaien synchroon.")
                subprocess.run(["jobs"], shell=True)

            # --- BG (Zet een gepauzeerde taak op de achtergrond) ---
            elif command == "bg":
                subprocess.run(["bg"], shell=True)

            # --- FG (Haalt een achtergrondtaak naar de voorgrond) ---
            elif command == "fg":
                subprocess.run(["fg"], shell=True)

            # --- SERVICES (Toont alle actieve achtergrondservices op macOS) ---
            elif command == "services":
                print("--- Active macOS Launch Agents & Daemons ---")
                # 'launchctl list' is de macOS tegenhanger van service-lijsten [1, 2]
                subprocess.run(["launchctl", "list"])

            # --- SERVICE (Toont statusinformatie van een specifieke service) ---
            elif command.startswith("service "):
                service_name = command[8:].strip()
                if not service_name:
                    print("Error: use 'service <service_name>'")
                else:
                    subprocess.run(["launchctl", "list", service_name])

            # --- SYSTEMCTL (Simuleert systemd beheer via macOS launchctl) ---
            elif command.startswith("systemctl "):
                parts = command[10:].strip().split(" ")
                if len(parts) < 2:
                    print("Error: use 'systemctl <start|stop|status> <service_name>'")
                else:
                    action = parts[0]
                    service_name = parts[1]
                    
                    # Vertaal Linux systemctl commando's naar macOS launchctl [1, 2]
                    if action == "start":
                        subprocess.run(["launchctl", "start", service_name])
                    elif action == "stop":
                        subprocess.run(["launchctl", "stop", service_name])
                    elif action in ["status", "show"]:
                        subprocess.run(["launchctl", "list", service_name])
                    else:
                        print(f"Error: Action '{action}' not supported on macOS.")

            # --- JOURNAL (Toont live het macOS systeemlogboek) ---
            elif command == "journal":
                print("[INFO] Druk op CTRL+C om het logboek te stoppen...\n")
                # Maakt gebruik van de macOS log stream tool [3]
                subprocess.run(["log", "stream"])

            # --- LOGS (Toont de laatste regels van een specifiek logbestand) ---
            elif command.startswith("logs "):
                log_name = command[5:].strip()
                if not log_name:
                    print("Error: use 'logs <name>' (e.g., system, wifi, install)")
                else:
                    # Kijkt standaard in de macOS log-map
                    log_path = f"/var/log/{log_name}.log"
                    # -n 20 toont de laatste 20 regels
                    subprocess.run(["tail", "-n", "20", log_path])

            # --- WATCH (Herhaalt een commando live elke 2 seconden) ---
            elif command.startswith("watch "):
                sub_command = command[6:].strip()
                if not sub_command:
                    print("Error: use 'watch <command>' (e.g., watch ps)")
                else:
                    print(f"[WATCH] Voert '{sub_command}' uit. Druk op CTRL+C om te stoppen.")
                    time.sleep(1)
                    try:
                        while True:
                            # Maakt het scherm leeg voor de nieuwe update
                            subprocess.run(["clear"])
                            print(f"Every 2.0s: {sub_command}\n")
                            
                            # Voer het commando uit dat de gebruiker heeft opgegeven
                            # shell=True is nodig omdat de gebruiker meerdere argumenten kan typen
                            subprocess.run(sub_command, shell=True)
                            time.sleep(2)
                    except KeyboardInterrupt:
                        print("\n[WATCH] Gestopt.")
                        
                        # --- APT UPDATE (Vertaald naar Homebrew update op Mac) ---
            elif command == "apt update":
                print("[APT] Pakketlijsten vernieuwen via Homebrew...")
                subprocess.run(["brew", "update"])

            # --- APT UPGRADE (Vertaald naar Homebrew upgrade op Mac) ---
            elif command == "apt upgrade":
                print("[APT] Pakketten upgraden via Homebrew...")
                subprocess.run(["brew", "upgrade"])

            # --- APT INSTALL (Vertaald naar Homebrew install op Mac) ---
            elif command.startswith("apt install "):
                package = command[12:].strip()
                if not package:
                    print("Error: use 'apt install <package>'")
                else:
                    print(f"[APT] Installeren van pakket '{package}'...")
                    subprocess.run(["brew", "install", package])

            # --- APT REMOVE (Vertaald naar Homebrew uninstall op Mac) ---
            elif command.startswith("apt remove "):
                package = command[11:].strip()
                if not package:
                    print("Error: use 'apt remove <package>'")
                else:
                    print(f"[APT] Verwijderen van pakket '{package}'...")
                    subprocess.run(["brew", "uninstall", package])

            # --- APT SEARCH (Vertaald naar Homebrew search op Mac) ---
            elif command.startswith("apt search "):
                query = command[11:].strip()
                if not query:
                    print("Error: use 'apt search <name>'")
                else:
                    subprocess.run(["brew", "search", query])

            # --- APT LIST (Vertaald naar Homebrew list op Mac) ---
            elif command == "apt list":
                print("--- Geïnstalleerde Homebrew Pakketten ---")
                subprocess.run(["brew", "list"])

            # --- PIP INSTALL ---
            elif command.startswith("pip install "):
                package = command[12:].strip()
                if not package:
                    print("Error: use 'pip install <package>'")
                else:
                    # 'sys.executable -m pip' is veiliger dan los 'pip' op macOS
                    subprocess.run([sys.executable, "-m", "pip", "install", package])

            # --- PIP REMOVE (Vertaald naar pip uninstall) ---
            elif command.startswith("pip remove "):
                package = command[11:].strip()
                if not package:
                    print("Error: use 'pip remove <package>'")
                else:
                    # '-y' zorgt ervoor dat de uninstallation automatisch wordt goedgekeurd zonder prompt
                    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package])

            # --- PIP LIST ---
            elif command == "pip list":
                subprocess.run([sys.executable, "-m", "pip", "list"])

            # --- VENV (Toont virtual environment-info) ---
            elif command == "venv":
                # Checkt of de omgevingsvariabele VIRTUAL_ENV bestaat
                import os
                venv_path = os.environ.get("VIRTUAL_ENV")
                if venv_path:
                    print(f"[VENV] Actieve virtuele omgeving: {venv_path}")
                else:
                    print("[VENV] Geen actieve Python Virtual Environment gedetecteerd (Global scope).")

            # --- REQUIREMENTS (Genereert of installeert requirements.txt) ---
            elif command.startswith("requirements"):
                arg = command[12:].strip()
                if arg == "make":
                    print("[PIP] requirements.txt genereren...")
                    with open("requirements.txt", "w") as f:
                        # Vangt de output van pip freeze op en schrijft het weg
                        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f)
                    print("Success: requirements.txt succesvol aangemaakt.")
                elif arg == "read" or arg == "install":
                    print("[PIP] Installeren van pakketten uit requirements.txt...")
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                else:
                    print("Error: use 'requirements make' or 'requirements install'")
                    
                        # --- PYTHON / PYTHON3 (Opent de interactieve Python shell) ---
            elif command == "python" or command == "python3":
                print(f"[CLIOS] Schakelen naar Python interpreter...")
                # sys.executable opent exact de Python-versie waarmee CLIOS draait
                subprocess.run([sys.executable])
                print(f"\n[CLIOS] Teruggekeerd naar CLIOS prompt.")

            # --- PYVER (Toont de exacte Python-versie van je systeem) ---
            elif command == "pyver":
                subprocess.run([sys.executable, "--version"])

            # --- RUN (Start een los Python-bestand op) ---
            elif command.startswith("run "):
                target_file = command[4:].strip()
                if not target_file:
                    print("Error: use 'run <filename.py>'")
                else:
                    # Voert het opgegeven script uit binnen deze terminal
                    subprocess.run([sys.executable, target_file])

            # --- COMPILE (Compileert een Python-bestand naar een .pyc byte-code bestand) ---
            elif command.startswith("compile "):
                target_file = command[8:].strip()
                if not target_file:
                    print("Error: use 'compile <filename.py>'")
                else:
                    print(f"[PYTHON] Compileren van '{target_file}'...")
                    # Maakt gebruik van de ingebouwde py_compile module
                    subprocess.run([sys.executable, "-m", "py_compile", target_file])

            # --- DEBUG (Start het script met de ingebouwde Python debugger PDB) ---
            elif command.startswith("debug "):
                target_file = command[6:].strip()
                if not target_file:
                    print("Error: use 'debug <filename.py>'")
                else:
                    print(f"[DEBUG] Starten van '{target_file}' in PDB mode (typ 'q' om te stoppen)...")
                    # Start de interactieve command-line debugger
                    subprocess.run([sys.executable, "-m", "pdb", target_file])

            # --- GIT BASE (Toont de algemene Git handleiding) ---
            elif command == "git":
                subprocess.run(["git", "--help"])

            # --- GIT CLONE ---
            elif command.startswith("git clone "):
                url = command[10:].strip()
                if not url:
                    print("Error: use 'git clone <repository_url>'")
                else:
                    subprocess.run(["git", "clone", url])

            # --- GIT PULL ---
            elif command == "git pull":
                subprocess.run(["git", "pull"])

            # --- GIT PUSH ---
            elif command == "git push":
                subprocess.run(["git", "push"])

            # --- GIT STATUS ---
            elif command == "git status":
                subprocess.run(["git", "status"])

            # --- GIT COMMIT ---
            elif command.startswith("git commit"):
                # Controleer of er een bericht is meegegeven (bijv: git commit "Mijn update")
                message = command[10:].strip()
                if not message:
                    # Als er geen bericht is, openen we de standaard Git editor
                    subprocess.run(["git", "commit"])
                else:
                    # Anders voeren we het direct uit met het bericht
                    subprocess.run(["git", "commit", "-m", message])

            # --- PROJECT (Toont projectmappen in je huidige directory) ---
            elif command == "project":
                print("--- Beschikbare Projecten / Mappen ---")
                # Toont alleen mappen (-d */) in de huidige directory
                subprocess.run(["sh", "-c", "ls -d */ 2>/dev/null || echo 'Geen projectmappen gevonden.'"])

            # --- WORKSPACE (Opent de huidige map in de Finder van je iMac) ---
            elif command == "workspace":
                print("[INFO] Werkruimte openen in Finder...")
                # Het macOS commando 'open .' opent de huidige map visueel op je scherm
                subprocess.run(["open", "."])
                
                        # --- FIREWALL (Toont de status van de macOS Application Firewall) ---
            elif command == "firewall":
                print("[SECURITY] macOS Firewall status controleren...")
                subprocess.run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])

            # --- UFW (Simuleert Linux UFW firewallbeheer via macOS socketfilterfw) ---
            elif command.startswith("ufw "):
                action = command[4:].strip()
                if action == "enable":
                    print("[SECURITY] Firewall inschakelen...")
                    subprocess.run(["sudo", "/usr/libexec/ApplicationFirewall/socketfilterfw", "--setglobalstate", "on"])
                elif action == "disable":
                    print("[SECURITY] Firewall uitschakelen...")
                    subprocess.run(["sudo", "/usr/libexec/ApplicationFirewall/socketfilterfw", "--setglobalstate", "off"])
                elif action == "status":
                    subprocess.run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])
                else:
                    print("Error: use 'ufw enable', 'ufw disable' or 'ufw status'")

            # --- SCANPORTS (Scant de meest voorkomende netwerkpoorten van je eigen Mac) ---
            elif command == "scanports":
                print("[SECURITY] Lokale poortscan starten op localhost...")
                # Scant poorten 21, 22, 80, 443 en 8080 via de ingebouwde netcat (nc) tool
                for port in ["21", "22", "80", "443", "8080"]:
                    result = subprocess.run(["nc", "-zv", "-w", "1", "127.0.0.1", port], capture_output=True, text=True)
                    if "succeeded" in result.stderr or "succeeded" in result.stdout:
                        print(f"-> Poort {port}: OPEN")
                    else:
                        print(f"-> Poort {port}: Gesloten")

            # --- HASH (Maakt direct een SHA256-hash van een ingevoerde tekst) ---
            elif command.startswith("hash "):
                text = command[5:].strip()
                if not text:
                    print("Error: use 'hash <text>'")
                else:
                    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
                    print(f"SHA256 Hash van tekst: {text_hash}")

            # --- ENCRYPT (Versleutelt een bestand veilig met AES-256 via OpenSSL) ---
            elif command.startswith("encrypt "):
                target_file = command[8:].strip()
                if not target_file:
                    print("Error: use 'encrypt <filename>'")
                else:
                    output_file = f"{target_file}.enc"
                    print(f"[CRYPTO] Wachtwoord opgeven voor het versleutelen van '{target_file}':")
                    # OpenSSL vraagt de gebruiker nu veilig interactief om een encryptie-wachtwoord
                    subprocess.run(["openssl", "aes-256-cbc", "-salt", "-in", target_file, "-out", output_file])
                    print(f"Success: Gecodeerd bestand opgeslagen als '{output_file}'")

            # --- DECRYPT (Ontsleutelt een via CLIOS versleuteld bestand) ---
            elif command.startswith("decrypt "):
                target_file = command[8:].strip()
                if not target_file:
                    print("Error: use 'decrypt <filename.enc>'")
                else:
                    # Haalt de .enc extensie eraf voor het originele bestand
                    output_file = target_file.replace(".enc", ".decrypted")
                    print(f"[CRYPTO] Voer het wachtwoord in om '{target_file}' te ontsleutelen:")
                    subprocess.run(["openssl", "aes-256-cbc", "-d", "-salt", "-in", target_file, "-out", output_file])
                    print(f"Success: Ontsleuteld bestand opgeslagen als '{output_file}'")

            # --- KEYS (Toont je bestaande SSH sleutels op je Mac) ---
            elif command == "keys":
                print("--- Beschikbare SSH Sleutels (.pub) ---")
                subprocess.run(["sh", "-c", "ls -l ~/.ssh/*.pub 2>/dev/null || echo 'Geen SSH-sleutels gevonden.'"])

            # --- SSH-KEYGEN (Genereert een gloednieuw veilig RSA SSH-sleutelpaar) ---
            elif command == "ssh-keygen":
                print("[SECURITY] Nieuw SSH sleutelpaar genereren...")
                # Genereert een sleutel zonder moeilijke extra parameters te hoeven onthouden
                subprocess.run(["ssh-keygen"])

            # --- AUTH (Toont informatie over de huidige actieve CLIOS-sessie) ---
            elif command == "auth":
                print(f"--- CLIOS Authentication Session Info ---")
                print(f"Current User : {self.username}")
                print(f"User UUID    : {self.user_id}")
                print(f"Hostname     : {self.hostname}")
                print(f"Security Ring: Level 0 (Root/Kernel space)")

            # --- SAFE-MODE (Herstart CLIOS in een minimalistische veilige modus) ---
            elif command == "safe-mode":
                print("[SYSTEM] CLIOS wordt herstart in Safe Mode...")
                time.sleep(1)
                print("[SAFE-MODE] Drivers worden overgeslagen. Alleen core kernel is actief.")
                # We legen de geladen devices dictionary tijdelijk ter simulatie
                self.devices = {}
                print("[SAFE-MODE] Systeem is nu minimalistisch operationeel.")

            # --- LOCKDOWN (Schakelt de macOS Stealth modus in voor maximale netwerkbeveiliging) ---
            elif command == "lockdown":
                print("[SECURITY] LOCKDOWN-MODUS ACTIVEREN...")
                print("[SECURITY] Mac onzichtbaar maken in het netwerk (Stealth Mode)...")
                # Schakelt stealth mode in zodat je Mac niet reageert op pings van hackers
                subprocess.run(["sudo", "/usr/libexec/ApplicationFirewall/socketfilterfw", "--setstealthmode", "on"])
                print("[SUCCESS] CLIOS Lockdown actief. Netwerk-stealthmodus is ingeschakeld.")

            # --- AUDIT (Controleert basale veiligheidsinstellingen van je Mac-omgeving) ---
            elif command == "audit":
                print("--- CLIOS Security System Audit ---")
                # 1. Check de status van de SIP (System Integrity Protection) op je Mac
                print("[AUDIT 1/2] macOS System Integrity Protection controleren:")
                subprocess.run(["csrutil", "status"])
                # 2. Check of updates automatisch aanstaan
                print("\n[AUDIT 2/2] Automatische software-updates controleren:")
                subprocess.run(["softwareupdate", "--schedule"])
                
                        # --- BASE GPIO COMMANDO'S ---
            elif command.startswith("gpio"):
                if not self.is_raspberry_pi():
                    print("Error: GPIO-commando's zijn alleen beschikbaar op een Raspberry Pi (niet op macOS).")
                else:
                    parts = command.strip().split(" ")
                    
                    # gpio (zonder argumenten) -> Toon status van alle pinnen
                    if len(parts) == 1:
                        print("[HARDWARE] Raspberry Pi GPIO Status opvragen...")
                        subprocess.run(["raspi-gpio", "get"])
                        
                    # gpio read <pin>
                    elif parts[1] == "read" and len(parts) == 3:
                        pin = parts[2]
                        subprocess.run(["raspi-gpio", "get", pin])
                        
                    # gpio write <pin> <value>
                    elif parts[1] == "write" and len(parts) == 4:
                        pin = parts[2]
                        value = parts[3] # 0 of 1
                        subprocess.run(["raspi-gpio", "set", pin, "op", "dh" if value == "1" else "dl"])
                        print(f"[GPIO] Pin {pin} gezet op {value}")
                        
                    # gpio mode <pin> <mode>
                    elif parts[1] == "mode" and len(parts) == 4:
                        pin = parts[2]
                        mode = parts[3] # in of out
                        subprocess.run(["raspi-gpio", "set", pin, "op", mode])
                        print(f"[GPIO] Modus van pin {pin} veranderd naar {mode}")
                    else:
                        print("Error: use 'gpio', 'gpio read <pin>', 'gpio write <pin> <value>' or 'gpio mode <pin> <mode>'")

            # --- I2C (Toont actieve apparaten op de I2C bus) ---
            elif command == "i2c":
                if not self.is_raspberry_pi():
                    print("Error: I2C-scans zijn alleen beschikbaar op een Raspberry Pi.")
                else:
                    print("[HARDWARE] I2C Bus scannen...")
                    # -y 1 scant de standaard I2C bus 1 op de Pi
                    subprocess.run(["i2cdetect", "-y", "1"])

            # --- SPI (Controleert of de SPI interface aanstaat) ---
            elif command == "spi":
                if not self.is_raspberry_pi():
                    print("Error: SPI-status is alleen beschikbaar op een Raspberry Pi.")
                else:
                    import os
                    if os.path.exists("/dev/spidev0.0"):
                        print("[SPI] Interface is ACTIEF (/dev/spidev0.0 gevonden).")
                    else:
                        print("[SPI] Interface is INACTIEF. Schakel het in via raspi-config.")

            # --- USB (Toont aangesloten USB-apparaten, werkt op Pi én Mac!) ---
            elif command == "usb":
                print("--- Aangesloten USB Apparaten ---")
                if self.is_raspberry_pi():
                    subprocess.run(["lsusb"])
                else:
                    # macOS alternatief voor lsusb
                    subprocess.run(["system_profiler", "SPUSBDataType"])

            # --- BLUETOOTH (Toont bluetooth-status) ---
            elif command == "bluetooth":
                print("--- Bluetooth Status ---")
                if self.is_raspberry_pi():
                    subprocess.run(["hciconfig", "-a"])
                else:
                    subprocess.run(["system_profiler", "SPBluetoothDataType"])

            # --- AUDIO (Toont actieve audio-apparaten) ---
            elif command == "audio":
                print("--- Audio Apparaten ---")
                if self.is_raspberry_pi():
                    subprocess.run(["aplay", "-l"])
                else:
                    subprocess.run(["system_profiler", "SPAudioDataType"])

            # --- CAMERA ---
            elif command == "camera":
                if not self.is_raspberry_pi():
                    print("Error: Camera-hardware check is ontworpen voor de Raspberry Pi Camera Module.")
                else:
                    print("[HARDWARE] Raspberry Pi Camera Module controleren...")
                    subprocess.run(["vcgencmd", "get_camera"])

            # --- SCREEN (Toont scherm/resolutie informatie) ---
            elif command == "screen":
                print("--- Display Information ---")
                if self.is_raspberry_pi():
                    subprocess.run(["tvservice", "-s"])
                else:
                    subprocess.run(["system_profiler", "SPDisplaysDataType"])

            # --- HDMI ---
            elif command == "hdmi":
                if not self.is_raspberry_pi():
                    print("Error: HDMI diepgaande status is alleen beschikbaar op Raspberry Pi via tvservice.")
                else:
                    print("--- HDMI Status ---")
                    subprocess.run(["tvservice", "-n"]) # Toont de naam van de aangesloten monitor/TV

            # --- FAN (Toont de temperatuur van de CPU om te zien of de fan aan moet) ---
            elif command == "fan":
                if not self.is_raspberry_pi():
                    print("Error: Ventilator- en CPU-temperatuurmetingen zijn geoptimaliseerd voor de Pi.")
                else:
                    print("[HARDWARE] Raspberry Pi CPU Temperatuur:")
                    subprocess.run(["vcgencmd", "measure_temp"])

            # --- LED (Bestuurt de ingebouwde ACT of PWR led van de Pi) ---
            elif command.startswith("led "):
                if not self.is_raspberry_pi():
                    print("Error: On-board LED-besturing werkt alleen op een Raspberry Pi.")
                else:
                    action = command[4:].strip() # on of off
                    # Bestuurt de groene activity LED via het Linux sysfs systeem
                    trigger_path = "/sys/class/leds/led0/trigger"
                    brightness_path = "/sys/class/leds/led0/brightness"
                    try:
                        if action == "on":
                            subprocess.run(f"echo none > {trigger_path} && echo 1 > {brightness_path}", shell=True)
                            print("[LED] On-board LED ingeschakeld.")
                        elif action == "off":
                            subprocess.run(f"echo none > {trigger_path} && echo 0 > {brightness_path}", shell=True)
                            print("[LED] On-board LED uitgeschakeld.")
                        else:
                            print("Error: use 'led on' or 'led off'")
                    except Exception as e:
                        print(f"Error: Geen schrijfrechten op LED sysfs ({e}). Start CLIOS met sudo.")

            # --- SENSOR (Simuleert of leest een aangesloten sensor uit via sysfs) ---
            elif command == "sensor":
                if not self.is_raspberry_pi():
                    print("Error: Sensor-uitlezing is ontworpen voor de Raspberry Pi I/O-poorten.")
                else:
                    print("[HARDWARE] Controleren op aangesloten 1-Wire sensoren (/sys/bus/w1/devices/)...")
                    import os
                    if os.path.exists("/sys/bus/w1/devices/"):
                        subprocess.run(["ls", "/sys/bus/w1/devices/"])
                    else:
                        print("[SENSOR] Geen 1-Wire bus actief. Schakel w1-gpio in via config.txt.")
                        
                        # --- SERVER START (Simuleert of start een achtergrondservice via macOS launchctl) ---
            elif command == "server start":
                print("[SERVER] Starten van lokale webserver service...")
                subprocess.run(["sudo", "launchctl", "load", "-w", "/System/Library/LaunchDaemons/org.apache.httpd.plist"])

            # --- SERVER STOP ---
            elif command == "server stop":
                print("[SERVER] Stoppen van lokale webserver service...")
                subprocess.run(["sudo", "launchctl", "unload", "-w", "/System/Library/LaunchDaemons/org.apache.httpd.plist"])

            # --- SERVER RESTART ---
            elif command == "server restart":
                print("[SERVER] Herstarten van lokale webserver service...")
                subprocess.run(["sudo", "launchctl", "unload", "-w", "/System/Library/LaunchDaemons/org.apache.httpd.plist"])
                subprocess.run(["sudo", "launchctl", "load", "-w", "/System/Library/LaunchDaemons/org.apache.httpd.plist"])

            # --- SERVER STATUS ---
            elif command == "server status":
                print("[SERVER] Status controleren van actieve poorten (80/443/8080)...")
                subprocess.run("lsof -i :80 -i :443 -i :8080 | grep LISTEN", shell=True)

            # --- HOST (Toont gedetailleerde klantinformatie en netwerknaam) ---
            elif command == "host":
                print("--- CLIOS Host Information ---")
                subprocess.run(["hostname"])
                subprocess.run(["scutil", "--get", "ComputerName"])

            # --- WEBSERVER (Start een DIRECT werkende HTTP-server in de huidige map via Python) ---
            elif command == "webserver":
                print("[WEBSERVER] Lokale HTTP server starten op http://localhost:8000")
                print("[WEBSERVER] Druk op CTRL+C om de server te stoppen...\n")
                try:
                    # Start de ingebouwde Python HTTP server module
                    subprocess.run([sys.executable, "-m", "http.server", "8000"])
                except KeyboardInterrupt:
                    print("\n[WEBSERVER] Server gestopt.")

            # --- FLASK (Start een Flask-app als 'app.py' bestaat) ---
            elif command == "flask":
                import os
                if not os.path.exists("app.py"):
                    print("Error: Geen 'app.py' gevonden in deze map. Maak eerst een Flask-applicatie aan.")
                else:
                    print("[FLASK] Flask-server opstarten...")
                    subprocess.run([sys.executable, "-m", "flask", "run"])

            # --- FASTAPI (Start een FastAPI-app via uvicorn als 'main.py' een app bevat) ---
            elif command == "fastapi":
                print("[FASTAPI] FastAPI server opstarten via Uvicorn (zoekt naar main:app)...")
                subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload"])

            # --- SOCKET (Test een socketverbinding naar een opgegeven host en poort) ---
            elif command.startswith("socket "):
                parts = command[7:].strip().split(" ")
                if len(parts) < 2:
                    print("Error: use 'socket <host> <port>' (e.g., socket google.com 80)")
                else:
                    import socket
                    host, port = parts[0], int(parts[1])
                    print(f"[SOCKET] Verbinding testen met {host} op poort {port}...")
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(3.0)
                        s.connect((host, port))
                        print(f"[SUCCESS] Socket succesvol verbonden met {host}:{port}!")
                        s.close()
                    except Exception as e:
                        print(f"[FAILED] Verbinding mislukt: {e}")

            # --- API (Toont API-info of test een publieke JSON API via curl) ---
            elif command == "api":
                print("[API] Testen van een openbare API (HTTP GET naar ipify.org)...")
                subprocess.run(["curl", "https://ipify.org"])
                print()

            # --- SQLITE (Opent de interactieve SQLite3 console voor een databasebestand) ---
            elif command.startswith("sqlite "):
                db_file = command[7:].strip()
                if not db_file:
                    print("Error: use 'sqlite <database_name.db>'")
                else:
                    print(f"[SQLITE] Openen van {db_file} (typ '.exit' om te stoppen)...")
                    # Start de native sqlite3 cli terminal
                    subprocess.run(["sqlite3", db_file])

            # --- DATABASE (Toont ingebouwde statistieken van een lokaal SQLite bestand via Python) ---
            elif command.startswith("database "):
                db_file = command[9:].strip()
                if not db_file:
                    print("Error: use 'database <database_name.db>'")
                else:
                    import sqlite3
                    try:
                        conn = sqlite3.connect(db_file)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = cursor.fetchall()
                        print(f"--- Database info voor '{db_file}' ---")
                        print(f"Gevonden tabellen ({len(tables)}):")
                        for table in tables:
                            print(f" -> {table[0]}")
                        conn.close()
                    except Exception as e:
                        print(f"Error bij uitlezen database: {e}")

            # --- REMOTE (Toont informatie over verbonden netwerk-remotes via Git of SSH) ---
            elif command == "remote":
                print("--- Git Remote Repositories ---")
                subprocess.run(["git", "remote", "-v"])

            # --- SYNC (Synchroniseert de huidige map met een backup of externe map via rsync) ---
            elif command.startswith("sync "):
                target = command[5:].strip()
                if not target:
                    print("Error: use 'sync <target_directory>'")
                else:
                    print(f"[SYNC] Synchroniseren van huidige map met '{target}'...")
                    # --delete zorgt ervoor dat verwijderde bestanden ook aan de overkant verdwijnen
                    subprocess.run(["rsync", "-avz", "--delete", ".", target])

            # --- UPLOAD (Simuleert of voert een FTP/SFTP upload uit via curl) ---
            elif command.startswith("upload "):
                parts = command[7:].strip().split(" ")
                if len(parts) < 2:
                    print("Error: use 'upload <local_file> <server_url>'")
                else:
                    local_file, url = parts[0], parts[1]
                    print(f"[NETWORK] Uploaden van {local_file} naar {url}...")
                    subprocess.run(["curl", "-T", local_file, url])

            # --- DOWNLOAD (Downloadt een bestand van het internet met een voortgangsbalk) ---
            elif command.startswith("download "):
                url = command[9:].strip()
                if not url:
                    print("Error: use 'download <url>'")
                else:
                    print(f"[NETWORK] Bestand downloaden van {url}...")
                    # -O bewaart de originele bestandsnaam, -# toont een nette laadbalk van curl zelf
                    subprocess.run(["curl", "-O", "-#", url])
                    
                        # --- REBOOT (Herstart je fysieke iMac via AppleScript) ---
            elif command == "reboot":
                print("[SYSTEM] iMac wordt nu herstart...")
                time.sleep(1)
                # Vertelt macOS vriendelijk om te herstarten via de Finder
                subprocess.run(["osascript", "-e", "tell app \"System Events\" to restart"])

            # --- SHUTDOWN (Sluit je fysieke iMac af met 1 minuut vertraging) ---
            elif command == "shutdown":
                print("[SYSTEM] Systeemafsluiting ingepland...")
                # macOS shutdown vereist sudo en telt standaard af vanaf 1 minuut
                subprocess.run(["sudo", "shutdown", "-h", "+1"])

            # --- POWEROFF (Zet je fysieke iMac DIRECT en onmiddellijk uit) ---
            elif command == "poweroff":
                print("[SYSTEM] iMac wordt direct uitgeschakeld...")
                # -h now zorgt voor een onmiddellijke shutdown
                subprocess.run(["sudo", "shutdown", "-h", "now"])

            # --- SLEEP (Zet je iMac direct in de sluimer/slaapstand) ---
            elif command == "sleep":
                print("[SYSTEM] iMac gaat in slaapstand...")
                time.sleep(0.5)
                # Dit activeert direct de officiële macOS slaapstand
                subprocess.run(["pmset", "displaysleepnow"])

            # --- RESTART-NETWORK (Herstart de wifi-kaart van je Mac) ---
            elif command == "restart-network":
                print("[NETWORK] Netwerkinterface (en0) herstarten...")
                # Zet de wifi uit en direct weer aan om de connectie te resetten
                subprocess.run(["networksetup", "-setairportpower", "en0", "off"])
                time.sleep(1)
                subprocess.run(["networksetup", "-setairportpower", "en0", "on"])
                print("[SUCCESS] Netwerk succesvol herstart.")

            # --- SAFE-REBOOT (Sluit CLIOS af en start het direct weer op) ---
            elif command == "safe-reboot":
                print("[SYSTEM] CLIOS softwarematige herstart uitvoeren...")
                self.loading_bar(total=10)
                print("[SUCCESS] CLIOS succesvol herstart. Geheugen is opgeschoond.\n")
                # Dit herstart niet je Mac, maar ververst de status van je eigen OS loop
                self.devices = {}
                self.running = True

            # --- RECOVERY (Herstelmodus: Simuleert een systeemcontrole van CLIOS) ---
            elif command == "recovery":
                print("--- CLIOS Recovery Environment ---")
                print("[RECOVERY] Systeembestanden scannen...")
                time.sleep(1)
                print("[RECOVERY] Controleren van config.json... OK")
                print("[RECOVERY] Controleren van kernel.py... OK")
                print("[SUCCESS] Geen fouten gevonden. CLIOS is stabiel.")

            # --- SNAPSHOT (Maakt een back-up momentopname van je hele CLIOS-map) ---
            elif command == "snapshot":
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot_name = f"backup/clios_snapshot_{timestamp}.tar.gz"
                print(f"[SYSTEM] Systeemmomentopname maken: {snapshot_name}...")
                
                # Zorgt dat de backup-map bestaat en tapt de hele huidige map erin
                subprocess.run(["mkdir", "-p", "backup"])
                # We excluderen de backup map zelf om een oneindige lus te voorkomen
                subprocess.run(["tar", "--exclude=backup", "-czf", snapshot_name, "."])
                print(f"[SUCCESS] Snapshot succesvol opgeslagen!")
                
                        # --- THEME (Themabeheer) ---
            elif command.startswith("theme"):
                parts = command.strip().split(" ")
                
                # theme (zonder argumenten) -> Toon huidige thema
                if len(parts) == 1:
                    print(f"Huidig thema: {self.current_theme}")
                    print("Beschikbare thema's: dark, hacker, matrix, minimal")
                
                elif len(parts) == 2:
                    sub_theme = parts[1]
                    
                    if sub_theme == "dark":
                        self.current_theme = "dark"
                        # Reset naar standaard terminalkleuren (meestal wit op donker)
                        print(f"{self.colors_dict['reset']}Thema aangepast naar DARK.")
                        
                    elif sub_theme == "hacker":
                        self.current_theme = "hacker"
                        # Felgroene tekst
                        print(f"{self.colors_dict['green']}Thema aangepast naar HACKER mode.")
                        
                    elif sub_theme == "matrix":
                        self.current_theme = "matrix"
                        # Donkergroene tekst op een zwarte achtergrond
                        print(f"{self.colors_dict['black_bg']}{self.colors_dict['dark_green']}Thema aangepast naar MATRIX. Wake up, Neo...")
                        
                    elif sub_theme == "minimal":
                        self.current_theme = "minimal"
                        # Strakke witte tekst, alle dikgedrukte functies uit
                        print(f"{self.colors_dict['reset']}{self.colors_dict['white']}Thema aangepast naar MINIMAL.")
                    else:
                        print(f"Error: Thema '{sub_theme}' bestaat niet. Kies uit: dark, hacker, matrix, minimal")

            # --- COLORS (Handmatige kleuraanpassing) ---
            elif command.startswith("colors "):
                color_choice = command[7:].strip()
                if color_choice in self.colors_dict:
                    print(self.colors_dict[color_choice] + f"Tekstkleur aangepast naar {color_choice}.")
                else:
                    print(f"Error: Kleur niet herkend. Kies uit: green, cyan, red, purple, yellow, white")

            # --- FONT (Past de tekststijl aan via ANSI, bijv. Vetgedrukt) ---
            elif command.startswith("font "):
                style = command[5:].strip()
                if style == "bold":
                    print(self.colors_dict["bold"] + "Lettertype stijl: VETGEDRUKT")
                elif style == "reset" or style == "normal":
                    print(self.colors_dict["reset"] + "Lettertype stijl: NORMAAL")
                else:
                    print("Error: use 'font bold' or 'font reset'")

            # --- PROMPT (Past de CLI prompt live aan naar eigen tekst) ---
            elif command.startswith("prompt "):
                new_prompt = command[7:].strip()
                if not new_prompt:
                    print("Error: use 'prompt <jouw_tekst>'")
                else:
                    # Voegt een spatie toe aan het einde voor de netheid
                    self.custom_prompt = f"{new_prompt} "
                    print(f"Prompt succesvol veranderd!")

            # --- ANIMATIONS (Zet de opstart-laadbalk aan of uit) ---
            elif command.startswith("animations "):
                status = command[11:].strip()
                if status == "on":
                    self.animations_enabled = True
                    print("[UI] Opstartanimaties ingeschakeld.")
                elif status == "off":
                    self.animations_enabled = False
                    print("[UI] Opstartanimaties uitgeschakeld voor maximale snelheid.")
                else:
                    print("Error: use 'animations on' or 'animations off'")
                    
                        # --- INTERACTIEVE CLI BROWSER ---
            elif command == "browse":
                print("\n--- CLIOS WEB ENGINE ---")
                print(" [1] Direct URL read")
                print(" [2] Product search with price scan")
                print(" [3] Wikipedia search")

                keuze = input("Choose 1-3: ").strip()

                import urllib.parse
                import ssl
                import os
                import re
                import time
                from urllib.parse import urlparse, parse_qs, unquote

                url_to_fetch = ""
                target_name = "browse_result"
                product_mode = False
                product = ""

                if keuze == "1":
                    target_url = input("Enter URL, example google.com: ").strip()

                    if not target_url:
                        print("No URL entered. Back to CLIOS.")
                        continue

                    if not target_url.startswith(("http://", "https://")):
                        target_url = "https://" + target_url

                    url_to_fetch = target_url
                    target_name = target_url

                elif keuze == "2":
                    product = input("Product search: ").strip()

                    if not product:
                        print("No product entered. Back to CLIOS.")
                        continue

                    query = f"{product} kopen Nederland prijs site:.nl -amazon -temu -aliexpress -marktplaats -ebay -refurbished -tweedehands"
                    safe_query = urllib.parse.quote(query)
                    url_to_fetch = f"https://duckduckgo.com/html/?q={safe_query}"
                    target_name = f"product_{product}"
                    product_mode = True

                elif keuze == "3":
                    info = input("Wikipedia topic: ").strip()

                    if not info:
                        print("No topic entered. Back to CLIOS.")
                        continue

                    safe_topic = urllib.parse.quote(info.replace(" ", "_"))
                    url_to_fetch = f"https://nl.wikipedia.org/wiki/{safe_topic}"
                    target_name = f"wikipedia_{info}"

                else:
                    print("Invalid choice. Back to CLIOS.")
                    continue

                print(f"[BROWSER] Loading: {url_to_fetch}")

                try:
                    context = ssl._create_unverified_context()

                    headers = {
                        "User-Agent": "Mozilla/5.0 CLIOS Browser"
                    }

                    def fetch_html(url):
                        req = urllib.request.Request(url, headers=headers)
                        with urllib.request.urlopen(req, timeout=12, context=context) as response:
                            return response.read().decode("utf-8", errors="ignore")

                    def find_price(page_html):
                        return None

                        prices = []

                        for pattern in price_patterns:
                            matches = re.findall(pattern, page_text)
                            for match in matches:
                                try:
                                    price = float(match.replace(".", "").replace(",", "."))
                                    if 5 <= price <= 10000:
                                        prices.append(price)
                                except:
                                    pass

                        if prices:
                            return min(prices)

                        return None

                    html = fetch_html(url_to_fetch)

                    if product_mode:
                        raw_links = re.findall(r'href="([^"]+)"', html)

                        blocked = [
                            "amazon", "temu", "aliexpress", "marktplaats",
                            "ebay", "refurbished", "tweedehands",
                            "duckduckgo.com/y.js", "duckduckgo.com/feedback",
                            "duckduckgo.com/duckduckgo-help"
                        ]

                        products = []
                        seen = set()

                        for link in raw_links:
                            if "uddg=" not in link:
                                continue

                            real_url = parse_qs(urlparse(link).query).get("uddg", [""])[0]
                            real_url = unquote(real_url)

                            if not real_url.startswith("http"):
                                continue

                            lower_url = real_url.lower()

                            if any(bad in lower_url for bad in blocked):
                                continue

                            if real_url in seen:
                                continue

                            seen.add(real_url)

                            shop = urlparse(real_url).netloc.replace("www.", "")

                            print(f"[PRICE SCAN] Checking {shop}...")

                            price = None

                            try:
                                product_html = fetch_html(real_url)
                                price = find_price(product_html)
                            except:
                                price = None

                            products.append({
                                "shop": shop,
                                "url": real_url,
                                "price": price
                            })

                        products.sort(key=lambda x: x["price"] if x["price"] is not None else 999999)

                        clean_text = "CLIOS PRODUCT SEARCH RESULTS\n"
                        clean_text += f"Search: {product}\n"
                        clean_text += "Prices: not reliable yet, showing clean product links only\n"
                        clean_text += "=" * 60 + "\n\n"

                        if not products:
                            clean_text += "No clean product links found.\n"
                        else:
                            for index, item in enumerate(products, start=1):
                                price_text = "open link to check price"

                                clean_text += f"[{index}] {item['shop']}\n"
                                clean_text += f"    Price: {price_text}\n"
                                clean_text += f"    Link: {item['url']}\n"
                                clean_text += "-" * 60 + "\n"

                    else:
                        html = re.sub(r"<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>", "", html, flags=re.I)
                        html = re.sub(r"<style\b[^<]*(?:(?!</style>)<[^<]*)*</style>", "", html, flags=re.I)
                        text = re.sub(r"<[^>]+>", " ", html)
                        text = re.sub(r"\s+", " ", text).strip()
                        clean_text = text if text else "No readable text found on this page."

                    safe_filename = re.sub(r"[^\w\-_.]", "_", target_name) + ".txt"

                    storage_folder = os.path.expanduser("~/CLIOS_STORAGE")
                    os.makedirs(storage_folder, exist_ok=True)

                    backend_path = os.path.join(storage_folder, safe_filename)

                    with open(backend_path, "w", encoding="utf-8") as f:
                        f.write("CLIOS BROWSE RESULT\n")
                        f.write(f"URL: {url_to_fetch}\n")
                        f.write(f"DATE: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(clean_text)

                    print("\n" + "=" * 60)
                    print("LIVE PREVIEW")
                    print("=" * 60)
                    print(clean_text[:4000])
                    print("=" * 60)
                    print(f"[SAVED] Result saved to: {backend_path}")

                except Exception as error:
                    print("[BROWSER] Could not load this page.")
                    print("Reason:", error)
                    print("Back to CLIOS.")

            elif command == "trade":
                import json
                import os
                import random

                config_file = "config.json"

                GREEN = "\033[92m"
                RED = "\033[91m"
                YELLOW = "\033[93m"
                CYAN = "\033[96m"
                RESET = "\033[0m"

                # 1. LAAD CENTRALE CONFIG
                config_data = {}
                if os.path.exists(config_file):
                    try:
                        with open(config_file, "r") as f:
                            config_data = json.load(f)
                    except json.JSONDecodeError:
                        config_data = {}

                if "trade_accounts" not in config_data:
                    config_data["trade_accounts"] = {}

                # 2. AUTOMATISCH INLOGGEN LOGICA
                iban = config_data.get("last_logged_iban", "")

                # Als er nog geen actieve sessie bekend is, vragen we er éénmalig om
                if not iban:
                    print(f"\n{CYAN}=== CLIOS ASSET MANAGEMENT | REKENING KOPPELEN ==={RESET}")
                    invoer = input("Voer je IBAN in (bijv. NL74TRIO): ").strip().upper().replace(" ", "")
                    if len(invoer) < 4:
                        print(f"{RED}[ERROR] Ongeldige invoer.{RESET}")
                        continue
                    
                    if len(invoer) < 18:
                        hash_cijfers = str(abs(hash(invoer)))[:10].zfill(10)
                        iban = invoer + hash_cijfers
                    else:
                        iban = invoer

                # 3. MAAK ACCOUNT AAN ALS DEZE NOG NIET BESTAAT IN CONFIG
                if iban not in config_data["trade_accounts"]:
                    print(f"{YELLOW}[CLIOS LEDGER] Rekening {iban} configureren...{RESET}")
                    voornaam = input("Voornaam: ").strip()
                    achternaam = input("Achternaam: ").strip()
                    
                    if not voornaam or not achternaam:
                        print(f"{RED}[ERROR] Naam verplicht.{RESET}")
                        continue

                    config_data["trade_accounts"][iban] = {
                        "voornaam": voornaam,
                        "achternaam": achternaam,
                        "iban": iban,
                        "totaal_gestort": 0.00,
                        "vrij_saldo": 0.00,
                        "spaarvarken": 0.00,
                        "portfolio": {},
                        "transacties": [],
                        "budgetten": {},
                        "taken": [
                            {"id": 1, "taak": "Kamer opruimen en stoffen", "beloning": 2.50, "status": "Open"},
                            {"id": 2, "taak": "De vaatwasser in- of uitruimen", "beloning": 1.50, "status": "Open"},
                            {"id": 3, "taak": "Huiswerk maken of lezen (30 min)", "beloning": 5.00, "status": "Open"}
                        ]
                    }

                # Onthoud deze IBAN als de laatst succesvolle login
                config_data["last_logged_iban"] = iban
                with open(config_file, "w") as f:
                    json.dump(config_data, f, indent=4)

                print(f"{GREEN}[SUCCESS] Automatisch ingelogd op rekening {iban}!{RESET}")

                # 4. INTERFACE HOOFDMENU
                while True:
                    with open(config_file, "r") as f:
                        config_data = json.load(f)
                    
                    data = config_data["trade_accounts"][iban]

                    current_stock_price = round(random.uniform(535.00, 555.00), 2)
                    spy_stats = data["portfolio"].get("S&P 500 ETF (SPY)", {"aantal": 0, "aankoopprijs": 0.0})
                    aantal_stuks = spy_stats["aantal"]
                    totale_aankoopwaarde = aantal_stuks * spy_stats["aankoopprijs"]
                    actuele_beleggingswaarde = aantal_stuks * current_stock_price
                    
                    geinvesteerd_display = actuele_beleggingswaarde
                    totale_waarde = data["vrij_saldo"] + data["spaarvarken"] + geinvesteerd_display
                    
                    klusjes_inkomsten = sum([tx["bedrag"] for tx in data["transacties"] if "Taak voltooid" in tx["omschrijving"]])
                    bonus_inkomsten = data["totaal_gestort"] - klusjes_inkomsten

                    print("\n" + "═"*55)
                    print(f"  CLIOS PORTFOLIO MANAGER | {data['voornaam'].upper()} {data['achternaam'].upper()}")
                    print("═"*55)
                    print(f"  Rekeningnummer : {GREEN}{data['iban']}{RESET} 💳")
                    print(f"  Totaal Waarde  : {CYAN}€{totale_waarde:.2f}{RESET}")
                    print(f"  ├─ Vrij Saldo  : €{data['vrij_saldo']:.2f}")
                    print(f"  ├─ Spaarvarken : 🐷 €{data['spaarvarken']:.2f}")
                    print(f"  └─ Geïnvesteerd: €{geinvesteerd_display:.2f}")
                    print("─"*55)
                    print(f"  📊 BRON VAN JOUW INKOMSTEN:")
                    print(f"  ├─ Totaal Gestort   : €{data['totaal_gestort']:.2f}")
                    print(f"  │  ├─ Via Klusjes   : €{klusjes_inkomsten:.2f}")
                    print(f"  │  └─ Via Zakgeld   : €{bonus_inkomsten:.2f}")
                    print(f"  └─ Gereserveerd voor budgetten:")
                    if not data.get("budgetten"):
                        print("     └─ (Nog geen budgetpotjes aangemaakt)")
                    else:
                        for cat, info in data["budgetten"].items():
                            print(f"     ├─ 📂 {cat}: €{info['huidig']:.2f} (Doel: €{info['doel']:.2f})")
                    print("─"*55)
                    print("  1. Transactiehistorie & Rendement Details")
                    print("  2. Geld Verdienen (Klusjes & Taken)")
                    print("  3. Beurs & Marktsimulatie (Live Koersen & Traden)")
                    print("  4. Budgetten & Spaarpotten Beheren (Geld verdelen)")
                    print("  5. Ouder & Beheerder Instellingen 🔓")
                    print("  6. Wisselen van Rekening (Inloggen met andere IBAN)")
                    print("  7. Afsluiten (Terug naar CLIOS Terminal)")
                    print("═"*55)
                    
                    keuze = input("CLIOS[portfolio] > ").strip()

                    if keuze == "1":
                        print(f"\n{CYAN}--- RECENTE REKENINGMUTATIES ---{RESET}")
                        if not data["transacties"]:
                            print("  Nog geen transacties uitgevoerd.")
                        for tx in data["transacties"][-5:]:
                            kleur = GREEN if tx["type"] == "credit" else RED
                            teken = "+" if tx["type"] == "credit" else "-"
                            print(f"  • {tx['omschrijving']}: {kleur}{teken}€{abs(tx['bedrag']):.2f}{RESET}")
                        
                        print(f"\n{CYAN}--- TRANSACTIE DETAILS & RENDEMENT ---{RESET}")
                        if aantal_stuks == 0:
                            print("  Je bezit nog geen indexfondsen.")
                        else:
                            winst_verlies = actuele_beleggingswaarde - totale_aankoopwaarde
                            procent = (winst_verlies / totale_aankoopwaarde) * 100 if totale_aankoopwaarde > 0 else 0
                            p_kleur = GREEN if winst_verlies >= 0 else RED
                            p_teken = "+" if winst_verlies >= 0 else ""
                            print(f"  📈 Fonds: S&P 500 ETF (SPY)")
                            print(f"     Aantal in bezit : {aantal_stuks} stuks")
                            print(f"     Beurs Resultaat     : {p_kleur}{p_teken}€{winst_verlies:.2f} ({p_teken}{procent:.2f}%){RESET}")

                    elif keuze == "2":
                        print(f"\n{CYAN}--- BESCHIKBARE APPLICATIE TAKEN ---{RESET}")
                        open_taken = [t for t in data["taken"] if t["status"] == "Open"]
                        if not open_taken:
                            print("  Er zijn op dit moment geen openstaande klusjes.")
                        else:
                            for t in open_taken:
                                print(f"  [{t['id']}] {t['taak']} -> {GREEN}€{t['beloning']:.2f}{RESET}")
                        try:
                            klaar_id = input("\nVoer het nummer in van de voltooide taak: ").strip()
                            if klaar_id:
                                kid = int(klaar_id)
                                for t in data["taken"]:
                                    if t["id"] == kid and t["status"] == "Open":
                                        t["status"] = "Uitbetaald"
                                        data["vrij_saldo"] += t["beloning"]
                                        data["totaal_gestort"] += t["beloning"]
                                        data["transacties"].append({"omschrijving": f"Taak voltooid: {t['taak']}", "bedrag": t["beloning"], "type": "credit"})
                                        config_data["trade_accounts"][iban] = data
                                        with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                        print(f"{GREEN}[SUCCESS] €{t['beloning']:.2f} gestort!{RESET}")
                        except (ValueError, IndexError): pass

                    elif keuze == "3":
                        print(f"\n{CYAN}--- LIVE MARKT INDEX ---{RESET}")
                        stock_name = "S&P 500 ETF (SPY)"
                        print(f"  Actuele Prijs  : {GREEN}€{current_stock_price:.2f}{RESET}")
                        print("  1. Aandeel Kopen\n  2. Aandeel Verkopen")
                        sub_keuze = input("Keuze > ").strip()
                        if sub_keuze == "1":
                            if data["vrij_saldo"] < current_stock_price:
                                print(f"{RED}[ERROR] Te weinig saldo!{RESET}")
                            else:
                                data["vrij_saldo"] -= current_stock_price
                                data["portfolio"][stock_name] = {"aantal": aantal_stuks + 1, "aankoopprijs": current_stock_price}
                                data["transacties"].append({"omschrijving": f"Aankoop {stock_name}", "bedrag": current_stock_price, "type": "debit"})
                                config_data["trade_accounts"][iban] = data
                                with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                print(f"{GREEN}[SUCCESS] Gekocht!{RESET}")
                        elif sub_keuze == "2":
                            if aantal_stuks > 0:
                                data["portfolio"][stock_name]["aantal"] -= 1
                                data["portfolio"][stock_name]["waarde"] -= current_stock_price
                                data["vrij_saldo"] += current_stock_price
                                if data["portfolio"][stock_name]["aantal"] == 0: del data["portfolio"][stock_name]
                                data["transacties"].append({"omschrijving": f"Verkoop {stock_name}", "bedrag": current_stock_price, "type": "credit"})
                                config_data["trade_accounts"][iban] = data
                                with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                print(f"{YELLOW}[INFO] Verkocht!{RESET}")

                    elif keuze == "4":
                        print(f"\n{CYAN}--- ⚙️ BEHEER POTJES ---{RESET}")
                        print("  1. Geld in/uit Spaarvarken\n  2. Nieuw Budget\n  3. Geld verdelen")
                        b_keuze = input("Keuze > ").strip()
                        if b_keuze == "1":
                            actie = input("storten/opnemen: ").strip().lower()
                            try:
                                bedrag = float(input("Bedrag: €"))
                                if actie == "storten" and bedrag <= data["vrij_saldo"]:
                                    data["vrij_saldo"] -= bedrag
                                    data["spaarvarken"] += bedrag
                                    data["transacties"].append({"omschrijving": "Naar spaarvarken", "bedrag": bedrag, "type": "debit"})
                                elif actie == "opnemen" and bedrag <= data["spaarvarken"]:
                                    data["spaarvarken"] -= bedrag
                                    data["vrij_saldo"] += bedrag
                                    data["transacties"].append({"omschrijving": "Uit spaarvarken", "bedrag": bedrag, "type": "credit"})
                                config_data["trade_accounts"][iban] = data
                                with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                            except ValueError: pass
                        elif b_keuze == "2":
                            cat_naam = input("Naam budget: ").strip()
                            if cat_naam:
                                try:
                                    doel_bedrag = float(input("Doel: €"))
                                    if "budgetten" not in data: data["budgetten"] = {}
                                    data["budgetten"][cat_naam] = {"huidig": 0.0, "doel": doel_bedrag}
                                    config_data["trade_accounts"][iban] = data
                                    with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                except ValueError: pass
                        elif b_keuze == "3":
                            for c in data.get("budgetten", {}): print(f"  - {c}")
                            naar_cat = input("Welke categorie?: ").strip()
                            if naar_cat in data.get("budgetten", {}):
                                try:
                                    bdr = float(input("Bedrag: €"))
                                    if bdr <= data["vrij_saldo"]:
                                        data["vrij_saldo"] -= bdr
                                        data["budgetten"][naar_cat]["huidig"] += bdr
                                        data["transacties"].append({"omschrijving": f"Naar budget {naar_cat}", "bedrag": bdr, "type": "debit"} )
                                        config_data["trade_accounts"][iban] = data
                                        with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                except ValueError: pass

                    elif keuze == "5":
                        while True:
                            print(f"\n{YELLOW}--- OUDER CONFIGURATIE ---{RESET}")
                            print("  1. Nieuw klusje\n  2. Klusje wissen\n  3. Bonus storten\n  4. Terug")
                            admin_keuze = input("CLIOS[admin] > ").strip()
                            if admin_keuze == "1":
                                taak_naam = input("Klusje: ").strip()
                                if taak_naam:
                                    beloning = float(input("Beloning: €"))
                                    nieuw_id = max([t["id"] for t in data["taken"]], default=0) + 1
                                    data["taken"].append({"id": nieuw_id, "taak": taak_naam, "beloning": beloning, "status": "Open"})
                                    config_data["trade_accounts"][iban] = data
                                    with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                            elif admin_keuze == "2":
                                try:
                                    del_id = int(input("Verwijder ID: "))
                                    data["taken"] = [t for t in data["taken"] if t["id"] != del_id]
                                    config_data["trade_accounts"][iban] = data
                                    with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                                except ValueError: pass
                            elif admin_keuze == "3":
                                bonus = float(input("Bonus: €"))
                                data["vrij_saldo"] += bonus
                                data["totaal_gestort"] += bonus
                                data["transacties"].append({"omschrijving": "Bonus van ouders", "bedrag": bonus, "type": "credit"})
                                config_data["trade_accounts"][iban] = data
                                with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                            elif admin_keuze == "4": break

                    # KEUZE 6: REKENING WISSELEN (Reset 'last_logged_iban')
                    elif keuze == "6":
                        config_data["last_logged_iban"] = ""
                        with open(config_file, "w") as f: json.dump(config_data, f, indent=4)
                        print(f"{YELLOW}[SYSTEM] Uitgelogd. Start 'trade' opnieuw op om een andere IBAN te kiezen!{RESET}")
                        break

                    elif keuze == "7":
                        print("[SYSTEM] Terug naar CLIOS Terminal...")
                        break



            # === PAS ALS ALLERLAATSTE HET GENERIEKE COMMANDO ===
            elif command:
                clean_command = command.strip()
                print(f"[SYSTEM] Uitvoeren van Linux commando: {clean_command}...")
                try:
                    import shlex
                    parsed_args = shlex.split(clean_command)
                    subprocess.run(parsed_args)
                except FileNotFoundError:
                    print(f"[ERROR] Commando '{clean_command}' bestaat niet.")
                except Exception as e:
                    print(f"[ERROR] Fout tijdens uitvoering: {e}")
