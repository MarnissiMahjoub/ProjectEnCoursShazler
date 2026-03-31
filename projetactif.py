import sys
import os
import webbrowser
from datetime import datetime
import customtkinter as ctk
from CTkScrollableDropdown import CTkScrollableDropdown
from tkinter import messagebox, filedialog

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class OdooSwitchPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OdooSwitch Pro v2.8 - Auto-Load")
        self.geometry("1300x950")

        # Chemins par défaut
        self.token_file = "/home/mahjoub/Documents/local/shazler_token"
        self.roots = ["/home/mahjoub/Documents/local", "/home/mahjoub/Documents/local 2",
                      "/home/mahjoub/Documents/local 3"]
        self.ent_paths = {f"odoo_{v}": f"/opt/odoo/odoo_{v}/enterprise" for v in range(12, 21)}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main()

        # Initialisation
        self.refresh_roots()
        self.load_tokens_from_file()  # Charger les tokens au démarrage

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="SHAZLER", font=("Arial", 24, "bold"), text_color="#7C3AED").pack(pady=30)
        ctk.CTkButton(self.sidebar, text="+ Ajouter Racine", fg_color="#3B82F6", command=self.add_root).pack(pady=10,
                                                                                                             padx=20)
        ctk.CTkButton(self.sidebar, text="Quitter", fg_color="#E11D48", command=self.destroy).pack(side="bottom",
                                                                                                   pady=20, padx=20)

    def setup_main(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # --- SELECTION ---
        self.f_select = ctk.CTkFrame(self.scroll)
        self.f_select.pack(fill="x", pady=10)

        ctk.CTkLabel(self.f_select, text="1. Dossier Parent:").grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        self.combo_parent = ctk.CTkComboBox(self.f_select, width=250, command=self.sync_subs)
        self.combo_parent.grid(row=1, column=0, padx=20, pady=(0, 20))

        ctk.CTkLabel(self.f_select, text="2. Sous-Projet:").grid(row=0, column=1, padx=20, pady=(10, 0), sticky="w")
        self.combo_sub = ctk.CTkComboBox(self.f_select, width=300)
        self.combo_sub.grid(row=1, column=1, padx=20, pady=(0, 20))

        ctk.CTkLabel(self.f_select, text="3. Version Odoo:").grid(row=0, column=2, padx=20, pady=(10, 0), sticky="w")
        self.combo_ver = ctk.CTkOptionMenu(self.f_select, values=[f"odoo_{v}" for v in range(12, 21)])
        self.combo_ver.grid(row=1, column=2, padx=20, pady=(0, 20))

        # --- GITHUB (L'endroit où les tokens seront chargés) ---
        self.f_git = ctk.CTkFrame(self.scroll)
        self.f_git.pack(fill="x", pady=10)
        ctk.CTkLabel(self.f_git, text="GitHub Tokens (Chargés depuis fichier)", font=("Arial", 12, "bold")).pack(pady=5)

        self.token_entries = []  # Liste pour stocker les widgets d'entrée
        for i in range(5):
            r = ctk.CTkFrame(self.f_git, fg_color="transparent")
            r.pack(fill="x", padx=10, pady=2)
            e = ctk.CTkEntry(r)
            e.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkButton(r, text="📋", width=30, command=lambda x=e: self.copy(x.get())).pack(side="right")
            self.token_entries.append(e)

        # --- OUTPUTS ---
        self.f_out = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.f_out.pack(fill="x", pady=10)
        self.create_out("URL", "txt_url", "🌐 Chrome", self.open_chrome)
        self.create_out("Base de données", "txt_db", "📋 Copier",
                        lambda: self.copy(self.txt_db.get("0.0", "end").strip()))

        ctk.CTkLabel(self.f_out, text="Scaffold Command").pack(anchor="w")
        self.txt_scaf = ctk.CTkTextbox(self.f_out, height=60)
        self.txt_scaf.pack(fill="x", pady=5)

        # --- ACTIONS ---
        self.f_btn = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.f_btn.pack(fill="x", pady=20)
        ctk.CTkButton(self.f_btn, text="Générer Infos", fg_color="#8B5CF6", command=self.generate).pack(side="left",
                                                                                                        padx=5,
                                                                                                        expand=True,
                                                                                                        fill="x")
        ctk.CTkButton(self.f_btn, text="RUN CONFIG", fg_color="#10B981", command=self.run).pack(side="left", padx=5,
                                                                                                expand=True, fill="x")

    def create_out(self, label, name, btn_txt, cmd):
        row = ctk.CTkFrame(self.f_out, fg_color="transparent")
        row.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(row, text=label).pack(side="left")
        ctk.CTkButton(row, text=btn_txt, height=20, width=80, command=cmd).pack(side="right")
        setattr(self, name, ctk.CTkTextbox(self.f_out, height=40))
        getattr(self, name).pack(fill="x", pady=5)

    # --- LOGIQUE DE CHARGEMENT ---

    def load_tokens_from_file(self):
        """Lit le fichier shazler_token et remplit les champs GitHub"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as f:
                    lines = [line.strip() for line in f if line.strip()]  # Garde les lignes non-vides

                # On remplit les entries (limité à 5)
                for i in range(min(len(lines), 5)):
                    self.token_entries[i].delete(0, "end")
                    self.token_entries[i].insert(0, lines[i])
            except Exception as e:
                print(f"Erreur lors du chargement des tokens: {e}")

    # --- LOGIQUE FONCTIONNELLE ---

    def refresh_roots(self):
        valid_roots = [r for r in self.roots if os.path.exists(r)]
        self.combo_parent.configure(values=valid_roots)
        if valid_roots:
            self.combo_parent.set(valid_roots[0])
            self.sync_subs(valid_roots[0])

    def sync_subs(self, path):
        if os.path.exists(path):
            subs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d != ".idea"]
            subs.sort()
            self.combo_sub.configure(values=subs)
            if subs:
                self.combo_sub.set(subs[0])
            else:
                self.combo_sub.set("")
            try:
                self.drop.destroy()
            except:
                pass
            self.drop = CTkScrollableDropdown(self.combo_sub, values=subs, autocomplete=True)

    def add_root(self):
        d = filedialog.askdirectory()
        if d and d not in self.roots:
            self.roots.append(d)
            self.refresh_roots()

    def generate(self):
        p = self.combo_sub.get()
        if p:
            db = f"base_{p}_{datetime.now().strftime('%d_%m_%H_%M')}"
            self.txt_db.delete("0.0", "end")
            self.txt_db.insert("0.0", db)
            scaf = f"python3 odoo-bin scaffold custom_{p} ./addons"
            self.txt_scaf.delete("0.0", "end")
            self.txt_scaf.insert("0.0", scaf)
            self.txt_url.delete("0.0", "end")
            self.txt_url.insert("0.0", "localhost:8069")

    def run(self):
        v = self.combo_ver.get()
        messagebox.showinfo("Odoo", f"Lancement {v}\nEnterprise: {self.ent_paths.get(v)}")

    def open_chrome(self):
        webbrowser.open(f"http://{self.txt_url.get('0.0', 'end').strip()}")

    def copy(self, txt):
        """Logique d'extraction : si ':' existe, on prend ce qui est après"""
        text_to_copy = txt
        if ":" in txt:
            text_to_copy = txt.split(":")[-1].strip()
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        # On ne met pas de popup ici pour ne pas déranger pendant le travail,
        # mais le token est bien copié !


if __name__ == "__main__":
    app = OdooSwitchPro()
    app.mainloop()
