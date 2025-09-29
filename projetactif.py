# ProjetActif
import sys

from CTkScrollableDropdown import CTkScrollableDropdown
import customtkinter as ctk

import tkinter as tk
from tkinter import ttk
import re


def fonction(filename, projet, base_name):
    with open(filename, 'r') as file:
        lines = file.readlines()
    file.close()

    with open(filename, 'w') as file:
        for line in lines:
            if "addons_path" in line:
                test = line.split("/")
                pp = line.replace(test[-1], projet + "\n")
                file.write(pp)
            elif "dbfilter" in line:
                test = line.split(".*")
                pp = line.replace(test[-2], projet)
                file.write(pp)
            else:
                file.write(line)

        file.close()


ctk.set_appearance_mode("Dark")
# ctk.set_appearance_mode("Dark")
# ctk.set_appearance_mode("System")

frame = ctk.CTk()
frame.title('Shazler Projet En Cours')
# frame.geometry('1500x1200')
# frame.attributes("-fullscreen", True)
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

# Définir la taille de la fenêtre à la taille maximale de l'écran
frame.geometry(f"{screen_width}x{screen_height}")

window_14 = ctk.CTkFrame(frame)
window_14.grid(row=0, column=0, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_14, text="Odoo 14", font=("Arial", 20))
class_label.pack(pady=15, padx=15)

window_15 = ctk.CTkFrame(frame)
window_15.grid(row=0, column=1, ipadx=5, ipady=5, pady=10, padx=0)

class_label = ctk.CTkLabel(window_15, text="Odoo 15", font=("Arial", 20))
class_label.pack(pady=5, padx=5)

window_16 = ctk.CTkFrame(frame)
window_16.grid(row=0, column=2, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_16, text="Odoo 16", font=("Arial", 20))
class_label.pack(pady=15, padx=15)

window_17 = ctk.CTkFrame(frame)
window_17.grid(row=0, column=3, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_17, text="Odoo 17", font=("Arial", 20))
class_label.pack(pady=15, padx=15)

window_fermer = ctk.CTkFrame(frame)
window_fermer.grid(row=0, column=4, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_fermer, text="Fermer", font=("Arial", 20))
class_label.pack(pady=15, padx=15)
shazler_label = ctk.CTkLabel(frame, text="Shazler", font=("Arial", 80), text_color="#7C3AED")
shazler_label.grid(row=1, column=2, ipadx=0, ipady=0, pady=0, padx=0)
# odoo14
path_odoo_14 = '/home/mahjoub/Documents/odoo_source/odoo_14'
path_odoo_15 = '/home/mahjoub/Documents/odoo_source/odoo_15'
path_odoo_16 = '/home/mahjoub/Documents/odoo_source/odoo_16'
path_odoo_16_4 = '/home/mahjoub/Documents/odoo_source/odoo16_4'
path_odoo_17 = '/home/mahjoub/Documents/odoo_source/odoo_17'

# button = ctk.CTkButton(
#     window_14,
#     text='ahts',
#     command=lambda: fonction(path_odoo_14 + '/odoo.conf', "ahts", "ahts"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_14,
#     text='curachap',
#     command=lambda: fonction(path_odoo_14 + '/odoo.conf', "curachap", "curachap"))
# button.pack(pady=15, padx=15)
#
# # odoo15
#
# button = ctk.CTkButton(
#     window_15,
#     text='CED',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "ced", "ced"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_15,
#     text='Giz',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "giz", "giz"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_15,
#     text='Stars Airlines',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "Stars-Airlines", "Stars-Airlines"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_15,
#     text='darellamma',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "darellamma", "darellamma"))
# button.pack(pady=15, padx=15)
# button = ctk.CTkButton(
#     window_15,
#     text='Siala',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "siela", "siela"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_15,
#     text='ced',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "ced_v15_new", "ced"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_15,
#     text='silosun',
#     command=lambda: fonction(path_odoo_15 + '/odoo.conf', "silosun", "silosun"))
# button.pack(pady=15, padx=15)
#
# # odoo16
# button = ctk.CTkButton(
#     window_16,
#     text='Bako',
#     command=lambda: fonction(path_odoo_16 + '/odoo.conf', "bkov7", "bako"))
# button.pack(pady=15, padx=15)
#
# # odoo17
# button = ctk.CTkButton(
#     window_17,
#     text='IMC',
#     command=lambda: fonction(path_odoo_17 + '/odoo.conf', "imc", "imc"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_17,
#     text='VBIndustrie',
#     command=lambda: fonction(path_odoo_17 + '/odoo.conf', "vbinsdutrie_V_17", "vbinsdutrie_V_17"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_17,
#     text='Tritux',
#     command=lambda: fonction(path_odoo_17 + '/odoo.conf', "tritux-v17", "tritux-v17"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_17,
#     text='Inspark',
#     command=lambda: fonction(path_odoo_17 + '/odoo.conf', "inspark_v_17", "inspark_v_17"))
# button.pack(pady=15, padx=15)
#
# button = ctk.CTkButton(
#     window_17,
#     text='Convergen',
#     command=lambda: fonction(path_odoo_17 + '/odoo.conf', "convergen_agency_v17", "convergen_agency_v17"))
# button.pack(pady=15, padx=15)


def fermer_interface():
    frame.destroy()


button_fermer = ctk.CTkButton(
    window_fermer,
    text='Fermer',
    command=fermer_interface)
button_fermer.pack(pady=15, padx=15)

IMAGE_FOLDER = "/home/mahjoub/Bureau/Mahjoub/écran"

def change_wallpaper():
    if not os.path.isdir(IMAGE_FOLDER):
        messagebox.showerror("Erreur", f"Dossier non trouvé : {IMAGE_FOLDER}")
        return

    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        messagebox.showinfo("Aucune image", "Aucune image trouvée dans le dossier.")
        return

    random_image = random.choice(images)
    image_path = os.path.join(IMAGE_FOLDER, random_image)
    uri = f"file://{image_path}"

    # Changer le fond d'écran avec gsettings
    subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri])
    subprocess.run(["gsettings", "set", "org.gnome.desktop.screensaver", "picture-uri", uri])
    messagebox.showinfo("Succès", f"Fond d'écran changé : {random_image}")






# version

window_dif = ctk.CTkFrame(frame)
window_dif.grid(row=2, column=1, ipadx=50, ipady=30, pady=50, padx=50)

class_label = ctk.CTkLabel(window_dif, text="Version", font=("Arial", 20))
class_label.pack(pady=15, padx=15)

version = ctk.CTkOptionMenu(master=window_dif,
                          values=["odoo_14", "odoo_15", "odoo_16", "odoo_16_4", "odoo_17","odoo17_","odoo_18"])
version.pack(padx=20, pady=10)

# Project

import os

path = "/home/mahjoub/Documents/local"

liste_dossiers = []

for nom_dossier in os.listdir(path):
    if os.path.isdir(os.path.join(path, nom_dossier)) and nom_dossier != ".idea":
        liste_dossiers.append(nom_dossier)

liste_dossiers_sorted = sorted(liste_dossiers, key=lambda x: x[0].lower())
window_dif = ctk.CTkFrame(frame)
window_dif.grid(row=2, column=2, ipadx=50, ipady=30, pady=50, padx=50)
class_label = ctk.CTkLabel(window_dif, text="Project", font=("Arial", 20))
class_label.pack(pady=15, padx=15)
project = ctk.CTkComboBox(master=window_dif,
                          values=liste_dossiers_sorted, )
project.pack(padx=20, pady=10)

# Base
liste_base = [
    "",
    "ced",
    "giz",
    "stars",
    "siela",
    "ced",
    "silosun",
    "bako",
    "nawel",
    "imc",
    "vbind",
    "tritux",
    "inspark",
    "converge", "api"
]
window_dif = ctk.CTkFrame(frame)
window_dif.grid(row=2, column=3, ipadx=50, ipady=30, pady=50, padx=50)
class_label = ctk.CTkLabel(window_dif, text="Base", font=("Arial", 20))
class_label.pack(pady=15, padx=15)
base = ctk.CTkComboBox(master=window_dif, values=liste_base)
base.pack(padx=20, pady=10)

# Entreprise
window_dif = ctk.CTkFrame(frame)
window_dif.grid(row=2, column=0, ipadx=30, ipady=30, pady=30, padx=30)

checkbox_communautaire = ctk.CTkCheckBox(master=window_dif, text="Communautaire",
                           onvalue="on", offvalue="off")
checkbox_communautaire.pack(padx=10, pady=20)

checkbox_enterprise = ctk.CTkCheckBox(master=window_dif, text="enterprise",
                           onvalue="on", offvalue="off")
checkbox_enterprise.pack(padx=10, pady=20)


def generer_nom_base_de_donnee(project, base, version, communautaire,enterprise):
    from datetime import datetime
    file_num_port = "/home/mahjoub/Documents/local"
    liste_project = [item for item in os.listdir(file_num_port) if os.path.isdir(os.path.join(file_num_port, item))]
    filename = "/home/mahjoub/Documents/odoo_source/" + str(version) + "/odoo.conf"

    textbox_module.delete("0.0", "end")
    textbox.delete("0.0", "end")
    textbox_ip.delete("0.0", "end")
    import locale
    locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
    # delete all text
    textbox.insert("0.0",
                   "base_" + project + "_" + datetime.now().strftime('%d_%B_%H_%M'))  # insert at line 0 character 0


def run(project, base, version, communautaire,enterprise):
    from datetime import datetime
    file_num_port = "/home/mahjoub/Documents/local"
    liste_project = [item for item in os.listdir(file_num_port) if os.path.isdir(os.path.join(file_num_port, item))]
    port = 8060

    # textbox_module.delete("0.0", "end")
    textbox.delete("0.0", "end")
    textbox_ip.delete("0.0", "end")

    filename = "/home/mahjoub/Documents/odoo_source/" + str(version) + "/odoo.conf"
    with open(filename, 'r') as file:
        lines = file.readlines()
    file.close()
    http_port = ""
    with open(filename, 'w') as file:
        for line in lines:
            if "addons_path" in line:
                if communautaire == "on":
                    if "addons_path" in line:
                        test = line.split("/")
                        for rex in test:
                            if rex == "enterprise," :
                                    pp = line.replace("enterprise,", "odoo/addons,")
                                    pp = pp.replace(test[-1], project + "\n")
                                    file.write(pp)
                                    break
                elif enterprise == "on":
                    test = line.split("/")
                    for rex in test:
                        if rex == "addons,":
                            pp = line.replace("odoo/addons,", "enterprise,")
                            pp = pp.replace(test[-1], project + "\n")
                            file.write(pp)
                            break
                else :
                    test = line.split("/")
                    pp = line.replace(test[-1], project + "\n")
                    file.write(pp)



            # if "addons_path" in line:
            # 	test = line.split("/")
            # 	pp = line.replace(test[-1], project + "\n")
            # 	file.write(pp)
            elif "dbfilter" in line:
                test = line.split(".*")
                if base == "":
                    base = project.split("/")[-1]
                pp = line.replace(test[-2], base)
                file.write(pp)
            elif "http_port" in line:
                test = line.split("=")
                try:
                    http_port = port + liste_project.index(project)
                except:
                    http_port = 8069
                pp = line.replace(test[-1], str(http_port) + "\n")
                file.write(pp)
            else:
                file.write(line)

        file.close()
    import locale
    locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
    # delete all text
    textbox.insert("0.0",
                   "base_" + project + "_" + datetime.now().strftime('%d_%B_%H_%M'))  # insert at line 0 character 0
    path_scafold = "/home/mahjoub/Documents/odoo_source/" + str(version) + "/odoo/odoo-bin scaffold " + \
                   textbox_module.get("0.0", "end").split("\n")[0] + " /home/mahjoub/Documents/local/" + str(project)
    textbox_module.delete("0.0", "end")
    # print(path_scafold)
    # if textbox_module.get("0.0", "end").split("\n")[0] != "":
    textbox_module.insert("0.0", path_scafold)  # insert at line 0 character 0

    textbox_ip.insert("0.0", "mahjoub:" + str(http_port))


button = ctk.CTkButton(
    window_dif,
    text='Run',
    command=lambda: run(project.get(), base.get(), version.get(),checkbox_communautaire.get(),checkbox_enterprise.get()
                        ))
button.pack(pady=10, padx=10)

button = ctk.CTkButton(
    window_dif,
    text='Generer Nom BD',
    command=lambda: generer_nom_base_de_donnee(project.get(), base.get(), version.get()
                                               , checkbox_enterprise.get(),checkbox_communautaire.get(),
                                               ))
button.pack(pady=40, padx=10)
window_dif = ctk.CTkFrame(frame)
window_dif.grid(row=3, column=2, ipadx=5, ipady=5, pady=5, padx=5, )

window_dif_module = ctk.CTkFrame(frame)
window_dif_module.grid(row=3, column=3, ipadx=5, ipady=5, pady=5, padx=5, )

window_dif_ip = ctk.CTkFrame(frame)
window_dif_ip.grid(row=3, column=1, ipadx=5, ipady=5, pady=5, padx=5, )

class_label = ctk.CTkLabel(window_dif, text="Nom de nouvelle base", font=("Arial", 13), corner_radius=10)
class_label.pack(pady=5, padx=5)

class_label_module = ctk.CTkLabel(window_dif_module, text="Nom de nouvelle module", font=("Arial", 13),
                                  corner_radius=10)
class_label_module.pack(pady=5, padx=5)

class_label_ip = ctk.CTkLabel(window_dif_ip, text="URL de projet", font=("Arial", 13), corner_radius=10)
class_label_ip.pack(pady=5, padx=5)

textbox_module = ctk.CTkTextbox(class_label_module, width=400, height=100, )
textbox_module.grid()
textbox = ctk.CTkTextbox(class_label, width=400, height=50, )
textbox.grid()
textbox_ip = ctk.CTkTextbox(class_label_ip, width=400, height=50, )
textbox_ip.grid()
CTkScrollableDropdown(project, values=liste_dossiers_sorted, height=270, width=240, resize=False,
                      justify="left", button_color="transparent", autocomplete=True)

frame.mainloop()
