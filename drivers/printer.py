# printer.py
import sys
import argparse

class PrinterDriver:
    def __init__(self, port="/dev/lp0"):
        # Slaat de poort op en geeft een melding bij initialisatie
        self.port = port
        print(f"[DRIVER] Printer geïnitialiseerd op poort {self.port}")

    def connect(self):
        # Logica om te verbinden met de poort
        print(f"[INFO] Verbinden met printer op {self.port}...")
        return True

    def send_raw_data(self, data):
        # Stuur bytes direct naar de hardware
        print(f"[SEND] Data verzonden: {data[:20]}...")

    def print_text(self, text):
        # Voeg printer-specifieke initialisatiecodes toe (ESC/POS)
        init_command = b'\x1b\x40' # ESC @ (Reset printer)
        cut_command = b'\x1d\x56\x41\x00' # GS V A 0 (Snijd papier)
        
        payload = init_command + text.encode('utf-8') + cut_command
        self.send_raw_data(payload)

# Deze code wordt ALLEEN uitgevoerd als je 'python3 printer.py' los aanroept in de terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Python Printer Driver")
    parser.add_argument("-p", "--port", default="/dev/lp0", help="Printer poort (bijv. /dev/usb/lp0 of COM3)")
    parser.add_argument("-f", "--file", required=True, help="Bestand om te printen")
    
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            content = f.read()
            
        driver = PrinterDriver(args.port)
        if driver.connect():
            driver.print_text(content)
            print("[SUCCESS] Printtaak voltooid.")
            
    except Exception as e:
        print(f"[FOUT] Printen mislukt: {e}", file=sys.stderr)
