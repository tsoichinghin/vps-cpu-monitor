import tkinter as tk
from tkinter import ttk, filedialog
import requests
import csv
import threading

class CPUUsageMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPS CPU Monitor")

        self.vps_list = []
        self.labels = {}

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

        # Settings Tab
        self.settings_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.settings_tab, text='Settings')

        # CSV Import Button
        self.import_button = ttk.Button(self.settings_tab, text="Import CSV", command=self.import_csv)
        self.import_button.pack(pady=20)

        self.tab_control.pack(expand=1, fill="both")

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

        max_columns = 10
        for i, (name, ip) in enumerate(self.vps_list):
            frame = ttk.Frame(self.scrollable_frame, borderwidth=1, relief="solid")
            frame.grid(row=i//max_columns, column=i%max_columns, padx=5, pady=5, sticky="nsew")
            label = tk.Label(frame, text=name, font=("Helvetica", 28, "bold"), bg="lightgreen", width=8, height=4)
            label.pack(fill="both", expand=True)
            self.labels[ip] = label

    def start_threads(self):
        for name, ip in self.vps_list:
            thread = threading.Thread(target=self.update_label, args=(name, ip))
            thread.daemon = True
            thread.start()

    def update_label(self, name, ip):
        while True:
            cpu_usage = self.fetch_cpu_usage(ip)
            if cpu_usage is not None:
                color, text_color = self.get_color_and_text(cpu_usage)
                self.labels[ip].config(text=f'{name}\n{cpu_usage:.1f}%', bg=color, fg=text_color)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUUsageMonitorApp(root)
    root.mainloop()
