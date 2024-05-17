import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import csv
import threading
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

class CPUUsageMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPS CPU Monitor")
        self.root.geometry("1575x1200")
        
        self.vps_list = []
        self.labels = {}
        self.sender_email = ""
        self.sender_password = ""
        self.recipient_email = ""
        self.temp_email = None
        self.temp_sid_token = None

        self.tab_control = ttk.Notebook(root)

        self.cpu_usage_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.cpu_usage_tab, text='CPU Usage')

        self.canvas = tk.Canvas(self.cpu_usage_tab)
        self.scrollbar = ttk.Scrollbar(self.cpu_usage_tab, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.logs_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.logs_tab, text='Logs')

        self.logs_canvas = tk.Canvas(self.logs_tab)
        self.logs_scrollbar = ttk.Scrollbar(self.logs_tab, orient="vertical", command=self.logs_canvas.yview)
        self.logs_frame = ttk.Frame(self.logs_canvas)

        self.logs_frame.bind(
            "<Configure>",
            lambda e: self.logs_canvas.configure(
                scrollregion=self.logs_canvas.bbox("all")
            )
        )

        self.logs_canvas.create_window((0, 0), window=self.logs_frame, anchor="nw")
        self.logs_canvas.configure(yscrollcommand=self.logs_scrollbar.set)

        self.logs_canvas.pack(side="left", fill="both", expand=True)
        self.logs_scrollbar.pack(side="right", fill="y")

        self.settings_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.settings_tab, text='Settings')

        self.email_setting_label = ttk.Label(self.settings_tab, text="Linking Devices Settings", font=("Helvetica", 31, "bold"))
        self.email_setting_label.pack(pady=20)

        self.import_button = ttk.Button(self.settings_tab, text="Import CSV", command=self.import_csv)
        self.import_button.pack(pady=40)

        self.email_setting_label = ttk.Label(self.settings_tab, text="Notification Email Setting", font=("Helvetica", 30, "bold"))
        self.email_setting_label.pack(pady=40)

        self.sender_email_label = ttk.Label(self.settings_tab, text="Sender Email Address (Outlook only):")
        self.sender_email_label.pack(pady=5)
        self.sender_email_entry = ttk.Entry(self.settings_tab, width=40)
        self.sender_email_entry.pack(pady=5)

        self.sender_password_label = ttk.Label(self.settings_tab, text="Sender Email Password:")
        self.sender_password_label.pack(pady=5)
        self.sender_password_entry = ttk.Entry(self.settings_tab, show="*", width=40)
        self.sender_password_entry.pack(pady=5)

        self.recipient_email_label = ttk.Label(self.settings_tab, text="Recipient Email Address:")
        self.recipient_email_label.pack(pady=5)
        self.recipient_email_entry = ttk.Entry(self.settings_tab, width=40)
        self.recipient_email_entry.pack(pady=5)

        self.save_email_button = ttk.Button(self.settings_tab, text="Save Email", command=self.save_email)
        self.save_email_button.pack(pady=20)

        self.tab_control.pack(expand=1, fill="both")

        self.vps_status = {}

    def save_email(self):
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        recipient_email = self.recipient_email_entry.get()

        if not sender_email or not sender_password or not recipient_email:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        messagebox.showinfo("Email Saved", "Email settings have been saved.")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            self.vps_list = [(row['name'], row['ip']) for row in csv_reader]
        
        self.create_labels()
        self.start_threads()

    def create_labels(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.labels.clear()

        max_columns = 25
        for i, (name, ip) in enumerate(self.vps_list):
            frame = ttk.Frame(self.scrollable_frame, borderwidth=1, relief="solid")
            frame.grid(row=i//max_columns, column=i%max_columns, padx=5, pady=5, sticky="nsew")
            label = tk.Label(frame, text=name, font=("Helvetica", 12, "bold"), bg="lightgreen", width=6, height=3)
            label.pack(fill="both", expand=True)
            self.labels[ip] = label
            self.vps_status[ip] = {'cpu_usage': 0, 'overload_start': None}

    def start_threads(self):
        for name, ip in self.vps_list:
            thread = threading.Thread(target=self.update_label, args=(name, ip))
            thread.daemon = True
            thread.start()

    def update_label(self, name, ip):
        while True:
            cpu_usage = self.fetch_cpu_usage(ip)
            if cpu_usage is not None:
                self.vps_status[ip]['cpu_usage'] = cpu_usage
                color, text_color = self.get_color_and_text(cpu_usage)
                self.labels[ip].config(text=f'{name}\n{cpu_usage:.1f}%', bg=color, fg=text_color)
                self.check_overload(name, ip, cpu_usage)
            time.sleep(1)

    def fetch_cpu_usage(self, ip):
        url = f'http://{ip}:3001/cpu'
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return float(response.text.strip())
        except requests.RequestException:
            return None

    def get_color_and_text(self, cpu_usage):
        if cpu_usage <= 50:
            return "lightgreen", "green"
        elif cpu_usage <= 89:
            return "lightyellow", "yellow"
        else:
            return "lightcoral", "red"

    def check_overload(self, name, ip, cpu_usage):
        if cpu_usage >= 90:
            if self.vps_status[ip]['overload_start'] is None:
                self.vps_status[ip]['overload_start'] = time.time()
            elif time.time() - self.vps_status[ip]['overload_start'] >= 60:
                self.log_overload(name)
                if self.recipient_email:
                    self.send_email(name, ip)
                self.vps_status[ip]['overload_start'] = None
        else:
            self.vps_status[ip]['overload_start'] = None

    def send_email(self, name, ip):
        if not self.sender_email or not self.sender_password or not self.recipient_email:
            print("Email settings are incomplete.")
            return
        
        subject = f'{name} is overloaded'
        body = f'The VPS {name} with IP {ip} has been overloaded (CPU usage >= 90%) for more than 1 minute.'

        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
        smtp_user = self.sender_email
        smtp_password = self.sender_password

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(self.sender_email, [self.recipient_email], msg.as_string())
            server.quit()
            print(f'Email sent to {self.recipient_email}')
        except Exception as e:
            print(f'Failed to send email: {e}')

    def log_overload(self, name):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {name} is overloaded.'
        log_label = ttk.Label(self.logs_frame, text=log_message, anchor="w")
        log_label.pack(fill='x')

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUUsageMonitorApp(root)
    root.mainloop()
