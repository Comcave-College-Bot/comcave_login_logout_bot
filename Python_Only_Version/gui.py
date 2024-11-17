import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import configparser
import os
import threading
import queue
import io

class TimeEntry(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.hour_var = tk.StringVar()
        self.hour_entry = ttk.Entry(self, textvariable=self.hour_var, width=2)
        self.hour_entry.pack(side='left')
        self.hour_entry.bind('<KeyRelease>', self.validate_hour)
        ttk.Label(self, text=":").pack(side='left', padx=2)
        self.minute_var = tk.StringVar()
        self.minute_entry = ttk.Entry(self, textvariable=self.minute_var, width=2)
        self.minute_entry.pack(side='left')
        self.minute_entry.bind('<KeyRelease>', self.validate_minute)
        self.hour_entry.bind('<KeyRelease>', lambda e: self._check_hour_complete(e))

    def validate_hour(self, event=None):
        val = self.hour_var.get()
        if val.isdigit():
            if len(val) > 2: self.hour_var.set(val[:2])
            if len(val) == 2 and int(val) > 23: self.hour_var.set('23')
        else:
            self.hour_var.set(''.join(c for c in val if c.isdigit()))

    def validate_minute(self, event=None):
        val = self.minute_var.get()
        if val.isdigit():
            if len(val) > 2: self.minute_var.set(val[:2])
            if len(val) == 2 and int(val) > 59: self.minute_var.set('59')
        else:
            self.minute_var.set(''.join(c for c in val if c.isdigit()))

    def _check_hour_complete(self, event):
        if len(self.hour_var.get()) == 2:
            self.minute_entry.focus()

    def get(self):
        hour = self.hour_var.get().zfill(2)
        minute = self.minute_var.get().zfill(2)
        return f"{hour}:{minute}"

    def set(self, time_str):
        if ':' in time_str:
            hour, minute = time_str.split(':')
            self.hour_var.set(hour)
            self.minute_var.set(minute)

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

    def flush(self): pass

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
        self.root.title("ComCave Login - Python Only")
        self.root.geometry("400x600")
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
            if os.path.exists(icon_path): self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warnung: Icon konnte nicht geladen werden: {e}")
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TCheckbutton', font=('Arial', 10))
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.create_input_frame(main_frame)
        self.create_output_frame(main_frame)
        self.bot_running = False
        self.current_process = None
        sys.stdout = RedirectText(self.output_text)
        sys.stderr = RedirectText(self.output_text)
        self.set_light_mode()
        self.load_saved_data()

    def create_input_frame(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Einstellungen")
        input_frame.pack(fill='x', padx=5, pady=5)
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        ttk.Label(input_frame, text="Benutzername:").pack(anchor='w', padx=5, pady=2)
        ttk.Entry(input_frame, textvariable=self.username_var).pack(fill='x', padx=5, pady=2)
        ttk.Label(input_frame, text="Passwort:").pack(anchor='w', padx=5, pady=2)
        ttk.Entry(input_frame, textvariable=self.password_var, show="*").pack(fill='x', padx=5, pady=2)
        times_frame = ttk.Frame(input_frame)
        times_frame.pack(fill='x', padx=5, pady=5)
        login_frame = ttk.Frame(times_frame)
        login_frame.pack(fill='x', pady=2)
        ttk.Label(login_frame, text="Login-Zeit:").pack(side='left')
        self.login_time_entry = TimeEntry(login_frame)
        self.login_time_entry.pack(side='left', padx=5)
        logout_frame = ttk.Frame(times_frame)
        logout_frame.pack(fill='x', pady=2)
        ttk.Label(logout_frame, text="Logout-Zeit:").pack(side='left')
        self.logout_time_entry = TimeEntry(logout_frame)
        self.logout_time_entry.pack(side='left', padx=5)
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill='x', padx=5, pady=5)
        self.save_credentials_var = tk.BooleanVar(value=True)
        self.save_times_var = tk.BooleanVar(value=True)
        self.random_time_var = tk.BooleanVar(value=False)
        self.exit_after_logout_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Anmeldedaten speichern",
                       variable=self.save_credentials_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Zeiten speichern",
                       variable=self.save_times_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Zufällige Zeitvariation (±5 Min)",
                       variable=self.random_time_var).pack(anchor='w')
        ttk.Label(options_frame, text="Programm wird nach dem Logout beendet",
                 font=('Arial', 9, 'italic')).pack(anchor='w', pady=(5,0))
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', pady=10, padx=5)
        self.automation_button = ttk.Button(button_frame, text="Automatisierung starten",
                                          command=self.toggle_automation)
        self.automation_button.pack(side='left')
        self.theme_button = ttk.Button(button_frame, text="🌙",
                                     command=self.toggle_theme, width=3)
        self.theme_button.pack(side='right')

    def create_output_frame(self, parent):
        output_frame = ttk.LabelFrame(parent, text="Ausgabe")
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.output_text = tk.Text(output_frame, height=10, wrap='word', state='disabled')
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(output_frame, orient='vertical',
                                command=self.output_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.output_text['yscrollcommand'] = scrollbar.set

    def load_saved_data(self):
        if os.path.exists('setup.ini'):
            config = configparser.ConfigParser()
            config.read('setup.ini')
            if 'Benutzerdaten' in config:
                self.username_var.set(config.get('Benutzerdaten', 'username', fallback=''))
                self.password_var.set(config.get('Benutzerdaten', 'password', fallback=''))
            if 'Zeiten' in config:
                self.login_time_entry.set(config.get('Zeiten', 'login_time', fallback=''))
                self.logout_time_entry.set(config.get('Zeiten', 'logout_time', fallback=''))
                self.random_time_var.set(config.getboolean('Zeiten', 'random_time', fallback=False))
                self.exit_after_logout_var.set(config.getboolean('Zeiten', 'exit_after_logout', fallback=True))
            if 'Einstellungen' in config:
                if config.getboolean('Einstellungen', 'dark_mode', fallback=False):
                    self.set_dark_mode()
                else:
                    self.set_light_mode()

    def save_config(self):
        config = configparser.ConfigParser()
        if self.save_credentials_var.get():
            config['Benutzerdaten'] = {
                'username': self.username_var.get(),
                'password': self.password_var.get()
            }
        if self.save_times_var.get():
            config['Zeiten'] = {
                'login_time': self.login_time_entry.get(),
                'logout_time': self.logout_time_entry.get(),
                'random_time': str(self.random_time_var.get()),
                'exit_after_logout': str(self.exit_after_logout_var.get())
            }
        config['Einstellungen'] = {
            'dark_mode': str(self.theme_button.cget('text') == "☀️")
        }
        with open('setup.ini', 'w') as configfile:
            config.write(configfile)

    def toggle_automation(self):
        if not self.bot_running:
            if not all([self.username_var.get(), self.password_var.get(),
                       self.login_time_entry.get(), self.logout_time_entry.get()]):
                messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus!")
                return
            self.save_config()
            self.automation_button.config(text="Automatisierung stoppen")
            self.bot_running = True
            self.start_automation()
        else:
            if self.current_process:
                self.current_process.terminate()
                self.current_process = None
            self.automation_button.config(text="Automatisierung starten")
            self.bot_running = False
            print("Automatisierung gestoppt.")

    def start_automation(self):
        def run_bot():
            try:
                my_env = os.environ.copy()
                my_env["PYTHONIOENCODING"] = "utf-8"
                command = [
                    "python",
                    "-u",
                    "main.py",
                    "schedule",
                    self.username_var.get(),
                    self.password_var.get(),
                    self.login_time_entry.get(),
                    self.logout_time_entry.get(),
                    str(self.random_time_var.get())
                ]
                self.current_process = subprocess.Popen(
                    command,
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
                if self.bot_running:
                    self.root.after(0, self.stop_automation)
            except Exception as e:
                print(f"Fehler: {str(e)}")
                self.root.after(0, self.stop_automation)
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()

    def stop_automation(self):
        self.automation_button.config(text="Automatisierung starten")
        self.bot_running = False
        self.current_process = None

    def set_light_mode(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', background='#f0f0f0', foreground='black')
        self.root.configure(bg='#f0f0f0')
        self.output_text.configure(bg='white', fg='black')
        self.theme_button.config(text="🌙")

    def set_dark_mode(self):
        style = ttk.Style()
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabelframe', background='#2b2b2b')
        style.configure('TLabelframe.Label', background='#2b2b2b', foreground='white')
        self.root.configure(bg='#2b2b2b')
        self.output_text.configure(bg='#3b3b3b', fg='white')
        self.theme_button.config(text="☀️")

    def toggle_theme(self):
        if self.theme_button.cget('text') == "🌙":
            self.set_dark_mode()
        else:
            self.set_light_mode()
        self.save_config()

if __name__ == "__main__":
    app = LoginGUI()
    app.root.mainloop()