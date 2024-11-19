import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import configparser
import os
import threading
import queue
import io

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class RedirectText(io.TextIOBase):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.queue = queue.Queue()
        self.update_thread()

    def write(self, string):
        try:
            self.queue.put(string)
            return len(string)
        except Exception:
            safe_string = string.encode('ascii', 'replace').decode('ascii')
            self.queue.put(safe_string)
            return len(safe_string)

    def flush(self):
        pass

    def update_thread(self):
        try:
            while True:
                text = self.queue.get_nowait()
                self.text_widget.config(state='normal')
                self.text_widget.insert('end', text)
                self.text_widget.see('end')
                self.text_widget.config(state='disabled')
                self.text_widget.update_idletasks()
        except queue.Empty:
            self.text_widget.after(100, self.update_thread)

class LoginGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ComCave Login - Firefox Single Tap")
        self.root.geometry("400x400")

        # Icon setzen
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warnung: Icon konnte nicht geladen werden: {e}")

        # Styling
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Settings.TButton', font=('Segoe UI Symbol', 12))

        # Hauptframe
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Logo Frame (oben)
        logo_frame = ttk.Frame(self.main_frame)
        logo_frame.pack(fill='x', pady=10)

        # Logo laden und anzeigen
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_college.png")
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                basewidth = 250
                wpercent = (basewidth/float(logo.size[0]))
                hsize = int((float(logo.size[1])*float(wpercent)))
                logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(logo)
                logo_label = ttk.Label(logo_frame, image=photo)
                logo_label.image = photo
                logo_label.pack()
            else:
                print(f"logo_college.png nicht gefunden in: {logo_path}")
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {str(e)}")

        # Terminal Frame (anfangs versteckt)
        self.terminal_frame = ttk.Frame(self.main_frame)
        self.output_text = tk.Text(self.terminal_frame, height=12, wrap='word',
                                 state='disabled')
        self.output_text.pack(fill='both', expand=True, pady=(10, 5))  # 10px oben, 5px unten

        # Zurück Button im Terminal
        self.back_button = ttk.Button(self.terminal_frame, text="Zurück",
                                    command=self.show_buttons)
        self.back_button.pack(pady=(0, 10))  # Nur unten Abstand

        # Button Frame mit Login/Logout und Settings (unten)
        button_container = ttk.Frame(self.main_frame)
        button_container.pack(fill='x', side='bottom', pady=(0, 10))

        # Button Frame für Login/Logout
        self.button_frame = ttk.Frame(button_container)
        self.button_frame.pack(fill='x')

        # Button Frame für die Zeile
        button_row = ttk.Frame(self.button_frame)
        button_row.pack(fill='x')

        # Container für die Buttons (für gleichmäßige Verteilung)
        left_frame = ttk.Frame(button_row)
        left_frame.pack(side='left', expand=True)

        middle_frame = ttk.Frame(button_row)
        middle_frame.pack(side='left')

        right_frame = ttk.Frame(button_row)
        right_frame.pack(side='left', expand=True)

        # Buttons mit exakt gleicher Größe
        button_width = 12
        self.login_button = ttk.Button(left_frame, text="Login",
                                     command=self.start_login, width=button_width)
        self.login_button.pack(side='right', padx=10)

        # Settings Button in der Mitte
        self.settings_button = ttk.Button(middle_frame, text="⚙", style='Settings.TButton',
                                        command=self.show_settings, width=3)
        self.settings_button.pack(padx=5)

        self.logout_button = ttk.Button(right_frame, text="Logout",
                                      command=self.start_logout, width=button_width)
        self.logout_button.pack(side='left', padx=10)

        # Settings Frame (anfangs versteckt)
        self.settings_frame = ttk.Frame(self.main_frame)
        ttk.Label(self.settings_frame, text="Benutzername:").pack(pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.settings_frame, textvariable=self.username_var).pack(pady=5)
        ttk.Label(self.settings_frame, text="Passwort:").pack(pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.settings_frame, textvariable=self.password_var, show="*").pack(pady=5)

        # Install Button hinzufügen
        ttk.Button(self.settings_frame, text="Benötigte Module installieren",
                  command=self.install_requirements).pack(pady=10)

        ttk.Button(self.settings_frame, text="Speichern",
                  command=self.save_settings).pack(pady=10)
        ttk.Button(self.settings_frame, text="Zurück",
                  command=self.show_buttons).pack(pady=5)

        # Rest der Initialisierung
        self.bot_running = False
        self.current_process = None
        sys.stdout = RedirectText(self.output_text)
        sys.stderr = RedirectText(self.output_text)
        self.load_settings()

    def show_terminal(self):
        self.button_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.terminal_frame.pack(fill='both', expand=True)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')

    def show_settings(self):
        self.button_frame.pack_forget()
        self.terminal_frame.pack_forget()
        self.settings_frame.pack(fill='both', expand=True)

    def show_buttons(self):
        self.terminal_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.button_frame.pack(fill='x', pady=20)
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
        self.bot_running = False

    def save_settings(self):
        config = configparser.ConfigParser()
        config['Credentials'] = {
            'username': self.username_var.get(),
            'password': self.password_var.get()
        }
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        self.show_buttons()

    def load_settings(self):
        if os.path.exists('settings.ini'):
            config = configparser.ConfigParser()
            config.read('settings.ini')
            if 'Credentials' in config:
                self.username_var.set(config.get('Credentials', 'username', fallback=''))
                self.password_var.set(config.get('Credentials', 'password', fallback=''))

    def start_login(self):
        if not self.username_var.get() or not self.password_var.get():
            messagebox.showerror("Fehler", "Bitte geben Sie Benutzername und Passwort ein!")
            return
        self.show_terminal()
        self.run_command("login", self.username_var.get(), self.password_var.get())

    def start_logout(self):
        if not self.username_var.get() or not self.password_var.get():
            messagebox.showerror("Fehler", "Bitte geben Sie Benutzername und Passwort ein!")
            return
        self.show_terminal()
        self.run_command("logout", self.username_var.get(), self.password_var.get())

    def run_command(self, command, username, password):
        def run_bot():
            try:
                my_env = os.environ.copy()
                my_env["PYTHONIOENCODING"] = "utf-8"

                self.current_process = subprocess.Popen(
                    ["python", "-u", "main.py", command, username, password],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    universal_newlines=True,
                    bufsize=1,
                    env=my_env,
                    encoding='utf-8'
                )

                while self.current_process and self.current_process.poll() is None:
                    output = self.current_process.stdout.readline()
                    if output:
                        print(output.strip())

            except Exception as e:
                print(f"Fehler: {str(e)}")

        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()

    def install_requirements(self):
        try:
            # Zeige Terminal für die Installation
            self.show_terminal()

            # Prüfe ob pip installiert ist
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "--version"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("pip ist bereits installiert.")
            except:
                print("pip wird installiert...")
                try:
                    # Lade get-pip.py herunter
                    import urllib.request
                    print("Lade pip Installer herunter...")
                    urllib.request.urlretrieve(
                        "https://bootstrap.pypa.io/get-pip.py",
                        "get-pip.py"
                    )

                    # Installiere pip
                    subprocess.check_call(
                        [sys.executable, "get-pip.py"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )

                    # Lösche get-pip.py
                    os.remove("get-pip.py")
                    print("pip wurde erfolgreich installiert!")
                except Exception as e:
                    print("Fehler bei der pip Installation!")
                    raise e

            # Installiere jedes Modul einzeln mit pip
            modules = {
                'selenium': 'selenium>=4.0.0',
                'webdriver-manager': 'webdriver-manager',
                'pillow': 'pillow'
            }

            for name, module in modules.items():
                print(f"{name} wird installiert...")
                try:
                    # Führe pip install aus
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", module],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"{name} wurde erfolgreich installiert!")
                except subprocess.CalledProcessError as e:
                    print(f"Fehler beim Installieren von {name}!")
                    raise e

            print("\nAlle Module wurden erfolgreich installiert!")

        except Exception as e:
            print(f"Fehler bei der Installation: {str(e)}")
            print("Bitte versuchen Sie die Installation manuell:")
            print("1. Python neu installieren mit pip")
            print("2. pip install -r requirements.txt")

if __name__ == "__main__":
    app = LoginGUI()
    app.root.mainloop()