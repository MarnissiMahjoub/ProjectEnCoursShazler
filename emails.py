import customtkinter as ctk
username_robo = "robokidsbizerte@gmail.com"
password_robo = "nwvv adkm htjf iygf"  # Mot de passe spécifique pour l'application
imap_server = "imap.gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
username_2 = "marnissimahjoub12@gmail.com"
password_2 = "tajw lkcy yiwf dkbw"
import imaplib
def actualisez (username,password):
    textbox_resultat.delete("0.0", "end")
    IMAP_SERVER = "imap.gmail.com"  # Exemple pour Gmail
    EMAIL = username
    PASSWORD = password  # Mot de passe spécifique généré
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        textbox_resultat.insert("0.0",f"Vous avez {len(email_ids)} e-mails non lus.")
        mail.logout()

    except Exception as e:
        print(f"Erreur: {e}")




ctk.set_appearance_mode("Dark")
# ctk.set_appearance_mode("Dark")
# ctk.set_appearance_mode("System")

frame = ctk.CTk()
frame.title('Emails')
# frame.geometry('1500x1200')
# frame.attributes("-fullscreen", True)
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

frame.geometry(f"{400}x{400}")


window_email = ctk.CTkFrame(frame)
window_email.grid(row=0, column=0, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_email, text="Les emails", font=("Arial", 20))
class_label.pack(pady=15, padx=15)

button = ctk.CTkButton(
    window_email,
    text='mahjoub 2',
    command=lambda: actualisez(username_2,password_2))
button.pack(pady=15, padx=15)

button = ctk.CTkButton(
    window_email,
    text='Robokids',
    command=lambda: actualisez(username_robo,password_robo))
button.pack(pady=15, padx=15)
def fermer_interface():
    frame.destroy()


window_fermer = ctk.CTkFrame(frame)
window_fermer.grid(row=1, column=0, ipadx=5, ipady=5, pady=0, padx=0)

class_label = ctk.CTkLabel(window_fermer, text="Fermer", font=("Arial", 20))
class_label.pack(pady=15, padx=15)


window_resultat = ctk.CTkFrame(frame)
window_resultat.grid(row=1, column=3, )

textbox_resultat = ctk.CTkTextbox(window_resultat, width=200, height=50, )
textbox_resultat.grid()


button_fermer = ctk.CTkButton(
    window_fermer,
    text='Fermer',
    command=fermer_interface)
button_fermer.pack(pady=15, padx=15)

frame.mainloop()
