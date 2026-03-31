import sys
import os
import random
import subprocess
import customtkinter as ctk
from CTkScrollableDropdown import CTkScrollableDropdown
from tkinter import messagebox
from datetime import datetime
import locale

# --- CONFIGURATION INITIALE ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class OdooSwitchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OdooSwitch")
        self.geometry("1200x850")

        # Configuration de la grille (2 colonnes : Sidebar et Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_content()
        self.load_projects()

    def setup_sidebar(self):
        """Barre latérale pour les actions et le branding"""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="SHAZLER", font=ctk.CTkFont(size=24, weight="bold"),
                                       text_color="#7C3AED")
        self.logo_label.pack(pady=30, padx=20)

        # Boutons d'actions secondaires
        self.btn_wallpaper = ctk.CTkButton(self.sidebar, text="Changer Wallpaper", fg_color="transparent",
                                           border_width=1, command=self.change_wallpaper)
        self.btn_wallpaper.pack(pady=10, padx=20)

        self.btn_close = ctk.CTkButton(self.sidebar, text="Quitter", fg_color="#E11D48", hover_color="#BE123C",
                                       command=self.destroy)
        self.btn_close.pack(side="bottom", pady=20, padx=20)

    def setup_main_content(self):
        """Zone principale avec les formulaires"""
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # --- SECTION : CONFIGURATION ODOO ---
        self.config_frame = ctk.CTkFrame(self.scrollable_frame)
        self.config_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(self.config_frame, text="Configuration du Projet", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=15)

        # Version
        ctk.CTkLabel(self.config_frame, text="Version Odoo:").grid(row=1, column=0, padx=20, sticky="w")
        self.version = ctk.CTkOptionMenu(self.config_frame,
                                         values=["odoo_14", "odoo_15", "odoo_16", "odoo_17", "odoo_18", "odoo_19"])
        self.version.grid(row=2, column=0, padx=20, pady=(0, 20))

        # Projet
        ctk.CTkLabel(self.config_frame, text="Projet Local:").grid(row=1, column=1, padx=20, sticky="w")
        self.project = ctk.CTkComboBox(self.config_frame, width=250)
        self.project.grid(row=2, column=1, padx=20, pady=(0, 20))

        # Base
        ctk.CTkLabel(self.config_frame, text="Base Cible:").grid(row=1, column=2, padx=20, sticky="w")
        self.base = ctk.CTkComboBox(self.config_frame, values=["ced", "giz", "stars", "siela", "bako"])
        self.base.grid(row=2, column=2, padx=20, pady=(0, 20))

        # --- SECTION : OPTIONS ---
        self.options_frame = ctk.CTkFrame(self.scrollable_frame)
        self.options_frame.pack(fill="x", pady=10)

        self.check_commu = ctk.CTkCheckBox(self.options_frame, text="Communautaire")
        self.check_commu.pack(side="left", padx=50, pady=20)
        self.check_enterprise = ctk.CTkCheckBox(self.options_frame, text="Enterprise")
        self.check_enterprise.pack(side="left", padx=50, pady=20)

        # --- SECTION : OUTPUTS (TEXTBOXES) ---
        self.output_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.output_frame.pack(fill="x", pady=10)

        # URL / IP
        self.label_ip = ctk.CTkLabel(self.output_frame, text="URL du Projet")
        self.label_ip.grid(row=0, column=0, sticky="w", pady=(10, 0))
        self.textbox_ip = ctk.CTkTextbox(self.output_frame, height=40, width=500)
        self.textbox_ip.grid(row=1, column=0, columnspan=2, pady=5, sticky="we")

        # Base de données
        self.label_db = ctk.CTkLabel(self.output_frame, text="Nouvelle Base")
        self.label_db.grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.textbox = ctk.CTkTextbox(self.output_frame, height=40, width=500)
        self.textbox.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")

        # Module
        self.label_mod = ctk.CTkLabel(self.output_frame, text="Commande Scaffold / Module")
        self.label_mod.grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.textbox_module = ctk.CTkTextbox(self.output_frame, height=80, width=500)
        self.textbox_module.grid(row=5, column=0, columnspan=2, pady=5, sticky="we")

        # --- BOUTONS ACTIONS ---
        self.action_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=20)

        self.btn_gen = ctk.CTkButton(self.action_frame, text="Générer Nom BD", command=self.on_generate_click)
        self.btn_gen.pack(side="left", padx=10, expand=True, fill="x")

        self.btn_run = ctk.CTkButton(self.action_frame, text="RUN (Update Conf)", fg_color="#10B981",
                                     hover_color="#059669", command=self.on_run_click)
        self.btn_run.pack(side="left", padx=10, expand=True, fill="x")

    def load_projects(self):
        """Logique de scan des dossiers"""
        path = "/home/mahjoub/Documents/local"
        if os.path.exists(path):
            liste = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d != ".idea"]
            liste_sorted = sorted(liste, key=lambda x: x.lower())
            self.project.configure(values=liste_sorted)
            # Liaison du Dropdown scrollable
            self.dropdown = CTkScrollableDropdown(self.project, values=liste_sorted, autocomplete=True)

    # --- TES FONCTIONS ORIGINALES (ADAPTÉES) ---
    def on_generate_click(self):
        # On appelle ta logique ici en passant les valeurs des widgets
        self.generer_nom_base_de_donnee(self.project.get(), self.version.get())

    def on_run_click(self):
        # On convertit "on/off" pour ton ancienne logique
        c_val = "on" if self.check_commu.get() else "off"
        e_val = "on" if self.check_enterprise.get() else "off"
        self.run_logic(self.project.get(), self.base.get(), self.version.get(), c_val, e_val)

    def change_wallpaper(self):
        # Ton code de changement de wallpaper ici
        pass

    def generer_nom_base_de_donnee(self, project, version):
        # Recopie ici le corps de ta fonction generer_nom_base_de_donnee
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF8')
        except:
            pass
        self.textbox.delete("0.0", "end")
        name = f"base_{project}_{datetime.now().strftime('%d_%B_%H_%M')}"
        self.textbox.insert("0.0", name)

    def run_logic(self, project, base, version, communautaire, enterprise):
        # Recopie ici le corps de ta fonction run
        # Note : Pense à bien utiliser self.textbox_ip, self.textbox etc.
        print(f"Exécution pour {project} en version {version}")
        self.textbox_ip.delete("0.0", "end")
        self.textbox_ip.insert("0.0", f"mahjoub:8069 (Simulation)")


if __name__ == "__main__":
    app = OdooSwitchApp()
    app.mainloop()
