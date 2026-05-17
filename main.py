# main.py
from bootstrap import boot
from drivers.printer import PrinterDriver       # <--- Aangepast naar drivers.printer
from drivers.filesystem import VirtualFileSystem # <--- Aangepast naar drivers.filesystem

if __name__ == "__main__":
    kernel = boot()
    
    # 2. Registreer de printer driver
    kernel.register_device("printer", PrinterDriver(port="/dev/lp0"))
    
    # 3. Registreer de filesystem driver (bijvoorbeeld op het koppelpunt '/')
    kernel.register_device("filesystem", VirtualFileSystem())
    
    # 4. Start het OS (de kernel runt nu met beide drivers actief)
    kernel.run()
