import json
from datetime import datetime

class VirtualFileSystem:
    def __init__(self):
        # 1. Initialiseer de harde schijf in het geheugen
        self.root = {"type": "dir", "content": {}}
        self.current_dir = self.root

    def create_file(self, name, data=""):
        # 2. Haal de huidige tijd op voor de metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Voeg het bestand toe aan de huidige map
        self.current_dir["content"][name] = {
            "type": "file",
            "data": data,
            "size": len(data),
            "created": timestamp
        }
        return f"Bestand '{name}' succesvol aangemaakt."

    def list_dir(self):
        # 4. Geef een lijst van alle namen in deze map
        return list(self.current_dir["content"].keys())
