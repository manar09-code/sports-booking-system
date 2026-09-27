from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import customtkinter as ctk
import home
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Taux de conversion Euro -> TND
EURO_TO_TND = 3.3  # 1€ = 3.3 TND

def main(reservation_info=None):
    if reservation_info is None:
        messagebox.showerror("Erreur", "Aucune réservation sélectionnée !")
        return

    fenetre = Tk()
    fenetre.title("Paiement - Système de Réservation Sportive")
    fenetre.state("zoomed")
    fenetre.configure(bg="#F4F7FB")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    # --- Background image ---
    try:
        img_path = os.path.join(os.path.dirname(__file__), "pictures", "image.jpg")
        bg_image = Image.open(img_path)
        bg_image = bg_image.resize((fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(fenetre, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        fenetre.configure(bg="white")

    # --- Retour Button ---
    header = Frame(fenetre, bg="#133A5C", height=72)
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkButton(
        header,
        text="⟵ Retour",
        width=120,
        height=36,
        fg_color="#F77F00",
        hover_color="#E57100",
        font=("Arial", 13, "bold"),
        command=lambda: back_home(fenetre)
    ).pack(side=LEFT, padx=24)

    ctk.CTkLabel(
        header, text="PAIEMENT", text_color="white",
        font=("Arial", 18, "bold")
    ).pack(side=LEFT, padx=12)

    ctk.CTkLabel(
        fenetre, text="Choisissez une formule, puis sélectionnez votre mode de paiement",
        text_color="#133A5C", font=("Arial", 11)
    ).pack(anchor="w", padx=80, pady=(12, 0))

    # --- Résumé de la réservation ---
    frame_summary = Frame(
        fenetre, bg="white", width=760, height=180,
        highlightbackground="#133A5C", highlightthickness=2
    )
    frame_summary.pack(pady=(28, 18))
    frame_summary.pack_propagate(False)

    nom = reservation_info.get("nom", "Non spécifié")
    terrain = reservation_info.get("terrain", "Non spécifié")
    date_r = reservation_info.get("date", "Non spécifié")
    heure = reservation_info.get("heure", "Non spécifié")
    summary_text = (
        f"Résumé de votre réservation :\n\n"
        f"Nom : {nom}\n"
        f"Terrain : {terrain}\n"
        f"Date : {date_r}\n"
        f"Créneau : {heure}"
    )

    # Détecter weekend
    try:
        day_of_week = datetime.strptime(date_r, "%d/%m/%Y").weekday()
        is_weekend = day_of_week >= 5
    except:
        is_weekend = False

    ctk.CTkLabel(
        frame_summary, text=summary_text, font=("Arial", 15),
        text_color="#133A5C", justify="left"
    ).pack(anchor="center", expand=True)

    # --- Choix du plan ---
    ctk.CTkLabel(
        fenetre, text="Choisissez votre forfait", text_color="#133A5C",
        font=("Arial", 18, "bold")
    ).pack(pady=(4, 8))

    frame_plans = Frame(fenetre, bg="#F4F7FB")
    frame_plans.pack(pady=8)

    plans = [
        {"nom": "Forfait Standard", "prix": 10, "details": "1h de réservation, 2 joueurs inclus", "color": "#F77F00"},
        {"nom": "Forfait Premium", "prix": 20, "details": "2h de réservation, 4 joueurs inclus", "color": "#133A5C"},
        {"nom": "Forfait VIP", "prix": 30, "details": "3h de réservation, 6 joueurs inclus", "color": "#1F5061"}
    ]

    abonnement_var = IntVar(value=0)
    ctk.CTkCheckBox(
        fenetre,
        text="Abonnement mensuel (-10%)",
        variable=abonnement_var,
        onvalue=1,
        offvalue=0,
        font=("Arial", 12, "bold"), text_color="#133A5C",
        fg_color="#F77F00", hover_color="#E57100", border_color="#133A5C",
        border_width=1
    ).pack(pady=10)

    for i, plan in enumerate(plans):
        ctk.CTkButton(
            frame_plans,
            text=f"{plan['nom']} - {plan['prix']*EURO_TO_TND:.2f} TND\n{plan['details']}",
            width=260,
            height=120,
            fg_color=plan["color"],
            hover_color="#E57100",
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=lambda p=plan: pay(fenetre, p, reservation_info, abonnement_var.get(), is_weekend)
        ).grid(row=i, column=0, padx=10, pady=8)

    fenetre.mainloop()


def pay(parent, plan, reservation_info, abonnement, is_weekend):
    """Fenêtre de paiement qui s'ouvre correctement"""
    if reservation_info is None:
        messagebox.showerror("Erreur", "Aucune réservation sélectionnée !")
        return

    pay_win = Toplevel(parent)
    pay_win.title("Paiement")
    pay_win.geometry("500x450")
    pay_win.configure(bg="#F4F7FB")
    pay_win.grab_set()  # modal
    pay_win.transient(parent)  # focus on top

    nom = reservation_info.get("nom", "Non spécifié")
    terrain = reservation_info.get("terrain", "Non spécifié")
    date_r = reservation_info.get("date", "Non spécifié")
    heure = reservation_info.get("heure", "Non spécifié")

    prix = plan["prix"] * EURO_TO_TND
    reductions = []

    if is_weekend:
        prix *= 0.9
        reductions.append("Réduction weekend (-10%)")
    if abonnement:
        prix *= 0.9
        reductions.append("Réduction abonnement (-10%)")

    summary_text = (
        f"Plan choisi : {plan['nom']} - {plan['prix']*EURO_TO_TND:.2f} TND\n\n"
        f"Nom : {nom}\nTerrain : {terrain}\nDate : {date_r}\nCréneau : {heure}\n\n"
        f"Prix final : {prix:.2f} TND"
    )
    if reductions:
        summary_text += "\n" + "\n".join(reductions)

    ctk.CTkLabel(
        pay_win, text="Confirmation du paiement", font=("Arial", 18, "bold"),
        text_color="#133A5C"
    ).pack(pady=(20, 8))
    ctk.CTkLabel(
        pay_win, text=summary_text, font=("Arial", 14),
        text_color="#133A5C", justify="left"
    ).pack(pady=10, padx=20)

    frame_buttons = Frame(pay_win, bg="white")
    frame_buttons.pack(pady=10)

    def select_payment_type(payment_type):
        # Hide buttons and show card number entry
        frame_buttons.pack_forget()
        ctk.CTkLabel(pay_win, text=f"Entrez le numéro de votre {payment_type} :", font=("Arial", 12)).pack(pady=10)
        card_entry = ctk.CTkEntry(pay_win, placeholder_text="Numéro de carte", width=300, height=35, corner_radius=10)
        card_entry.pack(pady=10)
        ctk.CTkButton(
            pay_win,
            text="Confirmer Paiement",
            fg_color="#133A5C",
            hover_color="#14625C",
            font=("Arial", 12, "bold"),
            width=200,
            height=40,
            command=lambda: confirm_payment(payment_type, card_entry.get(), prix, summary_text)
        ).pack(pady=10)
        ctk.CTkButton(
            pay_win,
            text="Exporter PDF",
            fg_color="#D90429",
            hover_color="#B5001F",
            font=("Arial", 12, "bold"),
            width=200,
            height=40,
            command=lambda: export_to_pdf(summary_text, prix, card_entry.get())
        ).pack(pady=10)

    ctk.CTkButton(
        frame_buttons,
        text="Payer par Carte e-Dinar",
        fg_color="#F77F00",
        hover_color="#E57100",
        font=("Arial", 12, "bold"),
        width=200,
        height=40,
        command=lambda: select_payment_type("Carte e-Dinar")
    ).pack(pady=10)

    ctk.CTkButton(
        frame_buttons,
        text="Payer par Carte Bancaire",
        fg_color="#133A5C",
        hover_color="#14625C",
        font=("Arial", 12, "bold"),
        width=200,
        height=40,
        command=lambda: select_payment_type("Carte Bancaire")
    ).pack(pady=10)

    def confirm_payment(payment_type, card_number, prix, summary_text):
        if not card_number.strip():
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de carte valide.")
            return
        messagebox.showinfo("Paiement Réussi", f"Paiement de {prix:.2f} TND réussi par {payment_type} !")
        export_to_pdf(summary_text, prix, card_number)
        pay_win.destroy()


def export_to_pdf(summary_text, prix, card_number):
    """Export the payment summary to a PDF file and open it for printing"""
    filename = "recu_paiement.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Reçu de Paiement - Système de Réservation Sportive")
    # Summary text
    c.setFont("Helvetica", 12)
    lines = summary_text.split('\n')
    y = height - 150
    for line in lines:
        c.drawString(100, y, line)
        y -= 20

    # Price
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y - 20, f"Montant payé : {prix:.2f} TND")

    # Card number (masked)
    if card_number:
        masked_card = "**** **** **** " + card_number[-4:] if len(card_number) >= 4 else card_number
        c.drawString(100, y - 40, f"Carte utilisée : {masked_card}")

    c.save()
    messagebox.showinfo("PDF Exporté", f"Le reçu a été exporté vers {filename}. Ouvrez-le pour imprimer.")
    # Open the PDF file
    import subprocess
    import platform
    if platform.system() == "Windows":
        subprocess.run(["start", filename], shell=True)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", filename])
    else:  # Linux
        subprocess.run(["xdg-open", filename])


def back_home(win):
    win.destroy()
    home.main()


if __name__ == "__main__":
    main({
        "nom": "Test User",
        "terrain": "Terrain de Football",
        "date": "25/11/2025",
        "heure": "10:00-12:00"
    })
