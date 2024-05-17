import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import requests
import csv

def get_cpu_usage(vps_ip):
    url = f'http://{vps_ip}:3001/cpu'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return float(response.text.strip())
        else:
            return None
    except requests.RequestException:
        return None

def update_cpu_usage():
    for vps in vps_list:
        cpu_usage = get_cpu_usage(vps['ip'])
        if cpu_usage is not None:
            usage_label = f"{cpu_usage}%"
            if cpu_usage <= 50:
                bg_color = "#ccffcc" 
                fg_color = "#00cc00" 
            elif cpu_usage <= 89:
                bg_color = "#ffffcc"  
                fg_color = "#cccc00" 
            else:
                bg_color = "#ffcccc" 
                fg_color = "#cc0000" 
        else:
            usage_label = "N/A"
            bg_color = "white"
            fg_color = "black"
        vps['label'].config(text=f"{vps['name']}\n{usage_label}", bg=bg_color, fg=fg_color)
    root.after(10000, update_cpu_usage)

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'name' not in reader.fieldnames or 'ip' not in reader.fieldnames:
            messagebox.showerror("Invalid CSV", "CSV file must contain 'name' and 'ip' columns.")
            return
        vps_list.clear()
        for row in reader:
            vps_list.append({'name': row['name'], 'ip': row['ip'], 'label': None})
        create_vps_labels()

def create_vps_labels():
    for widget in cpu_usage_tab.winfo_children():
        widget.destroy()
    label_font = font.Font(size=25, weight="bold")
    for vps in vps_list:
        label = tk.Label(cpu_usage_tab, text=f"{vps['name']}\nN/A", borderwidth=2, relief="groove", width=5, height=2, font=label_font)
        label.pack(pady=5, padx=5)
        vps['label'] = label
    update_cpu_usage()

root = tk.Tk()
root.title("VPS CPU Monitor")

tab_control = ttk.Notebook(root)
cpu_usage_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)
tab_control.add(cpu_usage_tab, text='CPU Usage')
tab_control.add(settings_tab, text='Settings')
tab_control.pack(expand=1, fill='both')

load_button = tk.Button(settings_tab, text="Load VPS from CSV", command=load_csv)
load_button.pack(pady=20)

vps_list = []

root.mainloop()
