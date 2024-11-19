import os
import sys
import subprocess

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return True
    except:
        return False

if __name__ == "__main__":
    if not install_requirements():
        os.system('color')
        print("\033[91mFehler: Konnte requirements nicht installieren.\033[0m")
        print("\033[93mBitte führen Sie manuell aus:\033[0m")
        print("pip install -r requirements.txt")
        input("\nDrücken Sie eine Taste zum Beenden...")
        sys.exit(1)

    os.system("pythonw gui.py")