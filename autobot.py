import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import time
import threading
import json
import os

# --- CONFIGURATION ---
CONFIG_FILE = "bot_config_dynamic.json"

# --- THEME: ENTERPRISE DARK ---
C_BG_MAIN = "#1E1E1E"
C_SIDEBAR = "#252526"
C_ACCENT = "#007ACC"
C_TEXT_MAIN = "#FFFFFF"
C_TEXT_SUB = "#CCCCCC"
C_SUCCESS = "#4CAF50"
C_DANGER = "#F44336"

class ROCDynamicBot:
    def __init__(self, root):
        self.root = root
        self.root.title("ROC Automation - Dynamic Channel Edition")
        self.root.geometry("1100x650")
        self.root.configure(bg=C_BG_MAIN)
        
        self.is_running = False
        self.coords = self.load_config()
        
        self.setup_styles()
        self.build_layout()
        self.show_dashboard()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=C_BG_MAIN)
        style.configure("Sidebar.TFrame", background=C_SIDEBAR)
        style.configure("Header.TLabel", background=C_BG_MAIN, foreground="white", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=C_BG_MAIN, foreground=C_TEXT_SUB, font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#333333", foreground="white", insertcolor="white", borderwidth=0)
        style.configure("Nav.TButton", background=C_SIDEBAR, foreground="white", font=("Segoe UI", 11), borderwidth=0, anchor="w", padding=15)
        style.map("Nav.TButton", background=[('active', '#37373D')])
        style.configure("Treeview", background="#2D2D30", foreground="white", fieldbackground="#2D2D30", rowheight=30)
        style.map("Treeview", background=[('selected', C_ACCENT)])

    def build_layout(self):
        sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="ROC\nDYNAMIC", bg=C_SIDEBAR, fg=C_ACCENT, font=("Segoe UI", 16, "bold"), pady=40, justify="left").pack(anchor="w", padx=20)
        ttk.Button(sidebar, text="  📊  Dashboard", style="Nav.TButton", command=self.show_dashboard).pack(fill="x")
        ttk.Button(sidebar, text="  🎯  Calibration Map", style="Nav.TButton", command=self.show_calibration).pack(fill="x")
        
        self.lbl_status = tk.Label(sidebar, text="● STOPPED", bg=C_SIDEBAR, fg=C_TEXT_SUB, font=("Consolas", 10, "bold"), pady=20)
        self.lbl_status.pack(side="bottom", fill="x")

        self.main_area = ttk.Frame(self.root, style="TFrame")
        self.main_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    def clear_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ================= DASHBOARD =================
    def show_dashboard(self):
        self.clear_area()
        ttk.Label(self.main_area, text="Mission Control", style="Header.TLabel").pack(anchor="w")
        ttk.Label(self.main_area, text="Set how many channels to cycle through.", style="Sub.TLabel").pack(anchor="w", pady=(0, 20))
        
        card = tk.Frame(self.main_area, bg="#252526", padx=20, pady=20)
        card.pack(fill="x", pady=(0, 20))
        
        self.create_input(card, "HOW MANY CHANNELS? (e.g., 2)", "2", "ent_channel_count")
        
        row = tk.Frame(card, bg="#252526")
        row.pack(fill="x", pady=10)
        self.create_input(row, "INTERVAL (Seconds)", "10", "ent_interval", width=20, side="left")
        
        self.create_input(card, "MESSAGE CONTENT", "Join our Alliance!", "txt_msg", is_text=True)

        btn_row = tk.Frame(self.main_area, bg=C_BG_MAIN)
        btn_row.pack(fill="x", pady=(0, 20))
        
        self.btn_run = tk.Button(btn_row, text="▶ START", bg=C_SUCCESS, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=10, command=self.start_bot)
        self.btn_run.pack(side="left")
        self.btn_stop = tk.Button(btn_row, text="⏹ TERMINATE", bg=C_DANGER, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=10, command=self.stop_bot, state="disabled")
        self.btn_stop.pack(side="left", padx=10)

    # ================= CALIBRATION =================
    def show_calibration(self):
        self.clear_area()
        ttk.Label(self.main_area, text="Target Calibration", style="Header.TLabel").pack(anchor="w")
        
        cols = ("Target Name", "Coordinates", "Status")
        self.tree = ttk.Treeview(self.main_area, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("Target Name", text="Target Function")
        self.tree.heading("Coordinates", text="X, Y Coordinates")
        self.tree.heading("Status", text="Status")
        self.tree.column("Target Name", width=220)
        self.tree.pack(fill="both", expand=True, pady=(0, 15))

        # DYNAMIC TARGET LIST
        self.targets_map = [
            ("open_chat", "1. Open Chat Button (Bottom)"),
            ("menu_btn", "2. Menu/List Button (Optional)"),
            ("tab_1", "3. Channel Tab 1 (Province)"),
            ("tab_2", "4. Channel Tab 2 (Language)"),
            ("tab_3", "5. Channel Tab 3 (Optional)"),
            ("tab_4", "6. Channel Tab 4 (Optional)"),
            ("text_area", "7. Message Text Box"),
            ("send_btn", "8. Send Message Button"),
            ("close_chat", "9. Close/Cut Chat (X Button)")
        ]
        self.refresh_table()

        action_frame = tk.Frame(self.main_area, bg=C_BG_MAIN)
        action_frame.pack(fill="x", pady=10)
        
        tk.Button(action_frame, text="📍 MAP TARGET", bg=C_ACCENT, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, command=self.map_selected).pack(side="left")
        tk.Button(action_frame, text="🖱 TEST", bg="#444", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, command=self.test_selected).pack(side="left", padx=10)
        tk.Button(action_frame, text="🗑 RESET", bg="#D32F2F", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8, command=self.reset_all_coords).pack(side="right")

    def create_input(self, parent, label, default, var, is_text=False, width=None, side="top", padx=0):
        f = tk.Frame(parent, bg="#252526")
        f.pack(side=side, fill="x" if not width else "none", expand=True if not width else False, padx=padx, pady=5)
        tk.Label(f, text=label, bg="#252526", fg="#888", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        if is_text:
            inp = scrolledtext.ScrolledText(f, height=4, bg="#333", fg="white", relief="flat", insertbackground="white")
            inp.insert("1.0", default)
            inp.pack(fill="x", pady=(5,0))
        else:
            inp = tk.Entry(f, bg="#333", fg="white", relief="flat", insertbackground="white", font=("Consolas", 11))
            inp.insert(0, default)
            if width: inp.config(width=width)
            inp.pack(fill="x", pady=(5,0), ipady=5)
        setattr(self, var, inp)

    def refresh_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for key, name in self.targets_map:
            coord = self.coords.get(key, None)
            display_coord = f"{coord[0]}, {coord[1]}" if coord else "---"
            status = "✅ READY" if coord else "❌ PENDING"
            self.tree.insert("", "end", iid=key, values=(name, display_coord, status))

    def reset_all_coords(self):
        if messagebox.askyesno("Reset", "Wipe all coordinates?"):
            self.coords = {}
            self.save_config()
            self.refresh_table()

    def map_selected(self):
        sel = self.tree.selection()
        if not sel: return
        key = sel[0]
        name = self.tree.item(key)['values'][0]
        messagebox.showinfo("Ready?", f"Click OK, then wait 3 seconds to map:\n\n{name}")
        time.sleep(1) 
        self.root.update()
        time.sleep(3) 
        x, y = pyautogui.position()
        self.coords[key] = (x, y)
        self.save_config()
        self.refresh_table()
        next_id = self.tree.next(key)
        if next_id: self.tree.selection_set(next_id)

    def test_selected(self):
        sel = self.tree.selection()
        if not sel: return
        key = sel[0]
        coord = self.coords.get(key)
        if coord: pyautogui.moveTo(coord[0], coord[1], duration=0.5)

    def start_bot(self):
        if self.is_running: return
        self.is_running = True
        self.lbl_status.config(text="● RUNNING", fg=C_SUCCESS)
        self.btn_run.config(state="disabled", bg="#333")
        self.btn_stop.config(state="normal", bg=C_DANGER)
        t = threading.Thread(target=self.run_logic)
        t.daemon = True
        t.start()

    def stop_bot(self):
        self.is_running = False
        self.lbl_status.config(text="● STOPPED", fg=C_TEXT_SUB)
        self.btn_run.config(state="normal", bg=C_SUCCESS)
        self.btn_stop.config(state="disabled", bg=C_DANGER)

    def sleep_safe(self, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            if not self.is_running: return False
            time.sleep(0.1)
        return True

    def run_logic(self):
        try:
            try:
                max_channels = int(self.ent_channel_count.get())
            except:
                max_channels = 2
            
            interval = float(self.ent_interval.get())
            msg = self.txt_msg.get("1.0", "end-1c")
            
            while self.is_running:
                # 1. Open Chat Window - INCREASED DELAY
                print("[BOT] Opening Chat (Waiting 4s)...")
                if not self.click_target("open_chat", 4): break 
                
                # 2. Loop through channels
                for i in range(1, max_channels + 1):
                    if not self.is_running: break
                    
                    tab_key = f"tab_{i}"
                    print(f"[BOT] Switching to Channel {i} (Waiting 3s)...")
                    
                    if "menu_btn" in self.coords:
                        self.click_target("menu_btn", 2) # Wait 2s for menu
                    
                    # Click Tab - INCREASED DELAY
                    if not self.click_target(tab_key, 3): # Wait 3s for chat to load
                         continue
                    
                    if not self.send_message(msg): break
                
                # 3. Close Chat - INCREASED DELAY
                print("[BOT] Closing Chat (Waiting 2s)...")
                if not self.click_target("close_chat", 2): break
                
                print(f"[BOT] Waiting {interval}s...")
                if not self.sleep_safe(interval): break

        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.stop_bot()

    def send_message(self, msg):
        # Click text box logic
        if not self.click_target("text_area", 0.5): return False
        if not self.click_target("text_area", 0.5): return False
        
        # SLOWER TYPING
        pyautogui.write(msg, interval=0.15) 
        if not self.sleep_safe(1.0): return False # Wait 1s after typing
        
        if not self.click_target("send_btn", 1.5): return False # Wait 1.5s after clicking send
        return True

    def click_target(self, key, delay):
        if not self.is_running: return False
        if key in self.coords:
            pyautogui.click(self.coords[key])
            return self.sleep_safe(delay)
        return True 

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f)
            except: pass
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f: json.dump(self.coords, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = ROCDynamicBot(root)
    root.mainloop()