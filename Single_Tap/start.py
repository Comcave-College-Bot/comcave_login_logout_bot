import os
import sys
import subprocess

def install_requirements():
    try:
        # Prüfe ob pip verfügbar ist
        subprocess.check_call([sys.executable, "-m", "pip", "--version"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

        # Installiere requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return True
    except:
        return False

if __name__ == "__main__":
    # Versuche requirements zu installieren
    if not install_requirements():
        # Wenn Installation fehlschlägt, zeige Fehlermeldung
        os.system('color')  # Aktiviere ANSI-Farben
        print("\033[91mFehler: Konnte requirements nicht installieren.\033[0m")
        print("\033[93mBitte führen Sie manuell aus:\033[0m")
        print("pip install -r requirements.txt")
        input("\nDrücken Sie eine Taste zum Beenden...")
        sys.exit(1)

    # Wenn Installation erfolgreich, starte GUI
    os.system("pythonw gui.py")