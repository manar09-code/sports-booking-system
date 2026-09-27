from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from pymongo import MongoClient
import csv
class CsvReservationCollection:
    def __init__(self, filename):
        self.filename = filename
        self.fields = [
            "nom", "date", "heure", "terrain", "forfait", "abonnement",
            "equipment", "coaching", "user"
        ]

    def find(self, query=None):
        query = query or {}
        if not os.path.isfile(self.filename):
            return []
        with open(self.filename, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        return [
            row for row in rows
            if all(row.get(key, "") == ("" if value is None else str(value)) for key, value in query.items())
        ]

    def find_one(self, query):
        rows = self.find(query)
        return rows[0] if rows else None

    def insert_one(self, row):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            if not file_exists or os.path.getsize(self.filename) == 0:
                writer.writeheader()
            writer.writerow({field: row.get(field, "") for field in self.fields})

    def update_one(self, query, update):
        if not os.path.isfile(self.filename):
            return
        with open(self.filename, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        changes = update.get("$set", {})
        for row in rows:
            if all(row.get(key, "") == ("" if value is None else str(value)) for key, value in query.items()):
                row.update({key: str(value) if value is not None else "" for key, value in changes.items()})
                break
        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(rows)

    def delete_one(self, query):
        if not os.path.isfile(self.filename):
            return
        with open(self.filename, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        remaining = [
            row for row in rows
            if not all(row.get(key, "") == ("" if value is None else str(value)) for key, value in query.items())
        ]
        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(remaining)

def get_reservations_collection():
    uri = os.getenv("MONGODB_URI")
    if uri:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=1500)
            client.server_info()
            return client[os.getenv("MONGODB_DB", "sports_reservation")]["reservations"]
        except Exception:
            pass
    return CsvReservationCollection(os.path.join(os.path.dirname(__file__), "reservations.csv"))

reservations_collection = get_reservations_collection()

import home
import payment


def main(user=None):
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.configure(bg="#F4F7FB")
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    reservations_list = []

    # ---------------- BOUTON RETOUR ----------------
    def go_back():
        fenetre.destroy()
        home.main(user)

    header = Frame(fenetre, bg="#133A5C", height=72)
    header.pack(fill="x")
    header.pack_propagate(False)

    btn_retour = ctk.CTkButton(
        header,
        text="⟵ Retour",
        fg_color="#F77F00",
        text_color="white",
        hover_color="#E57100",
        corner_radius=12,
        width=120,
        height=36,
        font=("Arial", 13, "bold"),
        command=go_back
    )
    btn_retour.pack(side=LEFT, padx=24)

    ctk.CTkLabel(
        header, text="RESERVATION SPORTIVE", text_color="white",
        font=("Arial", 18, "bold")
    ).pack(side=LEFT, padx=12)

    ctk.CTkLabel(
        fenetre,
        text="1. Choisissez un terrain   2. Renseignez vos disponibilites   3. Confirmez",
        text_color="#133A5C", font=("Arial", 11)
    ).pack(anchor="w", padx=18, pady=(12, 0))

    # ---------------- FRAME 1 – Choix du terrain ----------------
    frame1_outer = LabelFrame(
        fenetre, text="Choisissez un terrain/salle",
        font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#133A5C"
    )
    frame1_outer.pack(pady=10, padx=10, fill="x")

    canvas = Canvas(frame1_outer, height=260, bg="white", highlightthickness=0)
    canvas.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(frame1_outer, orient=HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=BOTTOM, fill=X)
    canvas.configure(xscrollcommand=scrollbar.set)

    frame1 = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame1, anchor="nw")

    terrain = StringVar(value="")
    terrains = [
        ("Terrain de Football", "foot.jpg"),
        ("Terrain de Basketball", "basketball.jpg"),
        ("Terrain de Tennis", "tennis.jpg"),
        ("Salle de Handball", "handball.jpg"),
        ("Terrain de Padel", "padel.jpg")
    ]

    photo_refs = []  # garder les images en mémoire
    selected_frame = [None]  # référence pour surbrillance

    def select_terrain(name, frame_img):
        terrain.set(name)
        if selected_frame[0]:
            selected_frame[0].config(highlightthickness=0)
        frame_img.config(highlightbackground="green", highlightthickness=4)
        selected_frame[0] = frame_img

    for i, (name, filename) in enumerate(terrains):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "pictures", filename)
            img = Image.open(img_path).convert("RGBA").resize((220, 160), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None
        photo_refs.append(photo)

        frame_img = Frame(
            frame1, bg="#FFFFFF", padx=8, pady=8,
            highlightbackground="#D9E2EC", highlightthickness=1
        )
        frame_img.grid(row=0, column=i, padx=20, pady=10)

        if photo:
            lbl_img = Label(frame_img, image=photo, bg="#FFFFFF", cursor="hand2")
            lbl_img.image = photo
            lbl_img.pack()
        else:
            lbl_img = Label(frame_img, text="Image\nnon trouvée", bg="#FFFFFF", width=28, height=10)
            lbl_img.pack()

        rb = Radiobutton(
            frame_img, text=name, variable=terrain, value=name,
            bg="#FFFFFF", fg="#133A5C", activebackground="#FFFFFF",
            selectcolor="#ffffff", indicatoron=1,
            font=("Arial", 10, "bold"),
            command=lambda n=name, f=frame_img: select_terrain(n, f)
        )
        rb.pack(pady=(8, 6))

        def make_on_click(n=name, f=frame_img):
            return lambda e: select_terrain(n, f)

        lbl_img.bind("<Button-1>", make_on_click())
        frame_img.bind("<Button-1>", make_on_click())

    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # ---------------- CONTAINER FOR FRAME 2 AND BUTTONS ----------------
    container = Frame(fenetre, bg="#F4F7FB")
    container.pack(pady=10, padx=10, fill="both", expand=True)

    # ---------------- FRAME 2 – Formulaire (Inputs only) ----------------
    frame2 = LabelFrame(
        container, text="Formulaire de Réservation",
        font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#133A5C"
    )
    frame2.pack(side=LEFT, fill="both", expand=True, padx=(0, 8))
    frame2.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        frame2, text="Vos informations et le créneau souhaité",
        text_color="#133A5C", font=("Arial", 11)
    ).grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 4), sticky="w")

    Label(frame2, text="Nom complet :", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=4, sticky="w")
    nom_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#FFFFFF", text_color="#133A5C",
                             placeholder_text="Nom complet", font=("Arial", 12))
    nom_entry.grid(row=1, column=1, padx=10, pady=4, sticky="w")

    Label(frame2, text="Date de réservation :", font=("Arial", 11), bg="white").grid(row=2, column=0, padx=10, pady=4, sticky="w")
    date_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#FFFFFF", text_color="#133A5C",
                              placeholder_text="JJ/MM/AAAA", font=("Arial", 12))
    date_entry.grid(row=2, column=1, padx=10, pady=4, sticky="w")
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Créneau horaire :", font=("Arial", 11), bg="white").grid(row=3, column=0, padx=10, pady=4, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35, corner_radius=10, font=("Arial", 12))
    heure_combo.grid(row=3, column=1, padx=10, pady=4, sticky="w")

    Label(frame2, text="Forfait :", font=("Arial", 11), bg="white").grid(row=4, column=0, padx=10, pady=4, sticky="w")
    forfait_var = StringVar(value="Standard")
    forfait_combo = ctk.CTkComboBox(frame2, values=["Standard", "Premium", "VIP"], width=300, height=35,
                                     corner_radius=10, variable=forfait_var)
    forfait_combo.grid(row=4, column=1, padx=10, pady=4, sticky="w")

    # ---------------- FRAME 2 BUTTONS – Buttons and Options ----------------
    frame2_buttons = LabelFrame(
        container, text="Actions et Options",
        font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#133A5C"
    )
    frame2_buttons.pack(side=LEFT, fill="y", padx=8)

    # Frame boutons horizontaux
    buttons_frame = Frame(frame2_buttons, bg="white")
    buttons_frame.pack(pady=10)

    btn_ajouter = ctk.CTkButton(buttons_frame, text="Ajouter", fg_color="#F77F00", text_color="white",
                                corner_radius=20, height=40, font=("Arial", 12, "bold"))
    btn_ajouter.pack(fill="x", padx=10, pady=5)

    btn_modifier = ctk.CTkButton(buttons_frame, text="Modifier", fg_color="#133A5C", text_color="white",
                                 corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_modifier.pack(fill="x", padx=10, pady=5)

    btn_annuler = ctk.CTkButton(buttons_frame, text="Annuler la réservation", fg_color="#F77F00", text_color="white",
                                hover_color="#E57100", corner_radius=20, height=40,
                                font=("Arial", 12, "bold"), state="disabled")
    btn_annuler.pack(fill="x", padx=10, pady=5)

    btn_update = ctk.CTkButton(buttons_frame, text="Enregistrer les modifications", fg_color="#F77F00", text_color="white",
                               corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_update.pack(fill="x", padx=10, pady=5)

    btn_paiement = ctk.CTkButton(buttons_frame, text="Passer au Paiement", fg_color="#133A5C", text_color="white",
                                 corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_paiement.pack(fill="x", padx=10, pady=5)

    # Options supplémentaires
    options_container = Frame(frame2_buttons, bg="white")
    options_container.pack(pady=10)
    Label(options_container, text="Options supplémentaires :", font=("Arial", 11), bg="white",
          fg="#133A5C").pack(anchor="w")
    options_frame = Frame(options_container, bg="white")
    options_frame.pack(anchor="w")

    equipment_var = IntVar()
    coaching_var = IntVar()
    abonnement_var = IntVar(value=0)

    ctk.CTkCheckBox(options_frame, text="Location d'équipement (+5 TND)", variable=equipment_var, text_color="#133A5C").pack(anchor="w")
    ctk.CTkCheckBox(options_frame, text="Coaching personnel (+10 TND)", variable=coaching_var, text_color="#133A5C").pack(anchor="w")

    # ---------------- FONCTIONS CRUD ----------------
    def find_alternatives(date_r, heure, terr):
        alternatives = []
        current_index = hours.index(heure) if heure in hours else 0
        for i in range(current_index + 1, len(hours)):
            next_heure = hours[i]
            conflict = reservations_collection.find_one({"date": date_r, "heure": next_heure, "terrain": terr})
            if not conflict:
                alternatives.append(f"{terr} à {next_heure}")
                break
        terrains_list = [t[0] for t in terrains]
        for alt_terr in terrains_list:
            if alt_terr != terr:
                conflict = reservations_collection.find_one({"date": date_r, "heure": heure, "terrain": alt_terr})
                if not conflict:
                    alternatives.append(f"{alt_terr} à {heure}")
                    break
        return alternatives

    # ---------------- FRAME 3 – Liste des réservations ----------------
    frame3 = LabelFrame(
        container, text="Vos Réservations", font=("Arial", 12, "bold"),
        bg="#FFFFFF", fg="#133A5C"
    )
    frame3.pack(side=LEFT, fill="both", expand=True, padx=(8, 0))

    columns = ("Nom", "Date", "Heure", "Terrain", "Forfait", "Abonnement", "Équipement", "Coaching")
    tree = ttk.Treeview(frame3, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True, padx=8, pady=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=105, anchor="center", minwidth=85)

    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def update_reservations_table():
        for item in tree.get_children():
            tree.delete(item)
        query = {"user": user} if user else {}
        for index, row in enumerate(reservations_collection.find(query)):
            tree.insert("", "end", values=(
                row["nom"], row["date"], row["heure"], row["terrain"],
                row.get("forfait", "Standard"), "Oui" if row.get("abonnement", 0) else "Non",
                "Oui" if row.get("equipment", 0) else "Non",
                "Oui" if row.get("coaching", 0) else "Non"
            ), iid=str(index))

    selected_reservation = [None]

    def load_selected_reservation(event=None):
        selection = tree.selection()
        if not selection:
            selected_reservation[0] = None
            btn_modifier.configure(state="disabled")
            btn_update.configure(state="disabled")
            btn_paiement.configure(state="disabled")
            btn_annuler.configure(state="disabled")
            return

        query = {"user": user} if user else {}
        rows = list(reservations_collection.find(query))
        selected_reservation[0] = rows[int(selection[0])]
        row = selected_reservation[0]
        nom_entry.delete(0, END)
        nom_entry.insert(0, row.get("nom", ""))
        date_entry.delete(0, END)
        date_entry.insert(0, row.get("date", ""))
        heure_combo.set(row.get("heure", ""))
        terrain.set(row.get("terrain", ""))
        forfait_var.set(row.get("forfait", "Standard"))
        equipment_var.set(int(row.get("equipment", 0) or 0))
        coaching_var.set(int(row.get("coaching", 0) or 0))
        btn_modifier.configure(state="normal")
        btn_paiement.configure(state="normal")
        btn_annuler.configure(state="normal")

    tree.bind("<<TreeviewSelect>>", load_selected_reservation)

    def modifier_reservation():
        if selected_reservation[0] is None:
            messagebox.showwarning("Sélection requise", "Sélectionnez une réservation dans le tableau.")
            return
        btn_update.configure(state="normal")
        messagebox.showinfo("Modification", "Modifiez les champs à gauche, puis cliquez sur Enregistrer les modifications.")

    def update_reservation():
        original = selected_reservation[0]
        if original is None:
            messagebox.showwarning("Sélection requise", "Sélectionnez une réservation dans le tableau.")
            return

        updated = {
            "nom": nom_entry.get().strip(),
            "date": date_entry.get().strip(),
            "heure": heure_combo.get().strip(),
            "terrain": terrain.get().strip(),
            "forfait": forfait_var.get().strip(),
            "abonnement": abonnement_var.get(),
            "equipment": equipment_var.get(),
            "coaching": coaching_var.get(),
            "user": original.get("user", user)
        }
        if not all(updated[key] for key in ("nom", "date", "heure", "terrain")):
            messagebox.showwarning("Champs manquants", "Remplissez le nom, la date, le créneau et le terrain.")
            return

        query = {
            "nom": original.get("nom", ""),
            "date": original.get("date", ""),
            "heure": original.get("heure", ""),
            "terrain": original.get("terrain", ""),
            "user": original.get("user", user)
        }
        reservations_collection.update_one(query, {"$set": updated})
        selected_reservation[0] = updated
        update_reservations_table()
        btn_update.configure(state="disabled")
        messagebox.showinfo("Succès", "La réservation a été mise à jour.")

    def open_selected_payment():
        if selected_reservation[0] is None:
            messagebox.showwarning("Sélection requise", "Sélectionnez une réservation dans le tableau.")
            return
        fenetre.destroy()
        payment.main(selected_reservation[0])

    def annuler_reservation():
        original = selected_reservation[0]
        if original is None:
            messagebox.showwarning("Sélection requise", "Sélectionnez une réservation dans le tableau.")
            return
        if not messagebox.askyesno("Annuler la réservation", "Voulez-vous vraiment annuler cette réservation ?"):
            return
        query = {
            "nom": original.get("nom", ""),
            "date": original.get("date", ""),
            "heure": original.get("heure", ""),
            "terrain": original.get("terrain", ""),
            "user": original.get("user", user)
        }
        reservations_collection.delete_one(query)
        selected_reservation[0] = None
        update_reservations_table()
        btn_modifier.configure(state="disabled")
        btn_update.configure(state="disabled")
        btn_paiement.configure(state="disabled")
        btn_annuler.configure(state="disabled")
        messagebox.showinfo("Réservation annulée", "La réservation a été supprimée.")

    # ---------------- Ajouter réservation ----------------
    def ajouter_reservation():
        nom = nom_entry.get().strip()
        date_r = date_entry.get().strip()
        heure = heure_combo.get().strip()
        terr = terrain.get().strip()
        forfait = forfait_var.get().strip()
        abonnement = abonnement_var.get()
        equipment = equipment_var.get()
        coaching = coaching_var.get()

        if not nom or not date_r or not heure or not terr:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        conflict = reservations_collection.find_one({"date": date_r, "heure": heure, "terrain": terr})
        if conflict:
            alternatives = find_alternatives(date_r, heure, terr)
            msg = f"Le terrain {terr} est déjà réservé à {heure}.\n\nSuggestions AI :\n"
            if alternatives:
                msg += "\n".join(f"- {alt}" for alt in alternatives)
                msg += "\n\nVoulez-vous réessayer avec une alternative ?"
                retry = messagebox.askyesno("Conflit détecté", msg)
                if retry:
                    return
            else:
                msg += "Aucune alternative disponible pour cette date."
                messagebox.showerror("Indisponible", msg)
            return

        new_res = {
            "nom": nom, "date": date_r, "heure": heure, "terrain": terr,
            "forfait": forfait, "abonnement": abonnement,
            "equipment": equipment, "coaching": coaching, "user": user
        }
        reservations_collection.insert_one(new_res)
        messagebox.showinfo("Succès", "Réservation ajoutée !")
        update_reservations_table()

        nom_entry.delete(0, END)
        heure_combo.set("")
        terrain.set("")
        equipment_var.set(0)
        coaching_var.set(0)

        proceed = messagebox.askyesno("Paiement", "Voulez-vous procéder au paiement maintenant ?")
        if proceed:
            fenetre.destroy()
            payment.main(new_res)

    btn_ajouter.configure(command=ajouter_reservation)
    btn_modifier.configure(command=modifier_reservation)
    btn_annuler.configure(command=annuler_reservation)
    btn_update.configure(command=update_reservation)
    btn_paiement.configure(command=open_selected_payment)

    # Charger initialement
    update_reservations_table()
    fenetre.mainloop()


if __name__ == "__main__":
    main("TestUser")