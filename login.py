import os
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageTk

import home


def main():
    window = tk.Tk()
    window.title("Connexion - Reservation sportive")
    window.state("zoomed")

    try:
        image_path = os.path.join(os.path.dirname(__file__), "pictures", "background.jpg")
        image = Image.open(image_path).resize(
            (window.winfo_screenwidth(), window.winfo_screenheight())
        )
        background = ImageTk.PhotoImage(image)
        background_label = tk.Label(window, image=background)
        background_label.image = background
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except (OSError, tk.TclError):
        window.configure(bg="white")

    frame = ctk.CTkFrame(
        window, width=300, height=350, fg_color="white",
        border_width=1, border_color="lightgray"
    )
    frame.place(relx=0.5, rely=0.5, anchor="center")

    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def add_eye(entry):
        def toggle():
            entry.configure(show="" if entry.cget("show") == "*" else "*")

        button = ctk.CTkButton(
            entry.master, text="*", width=30, height=38,
            fg_color="transparent", hover_color="#e0e0e0", command=toggle
        )
        button.pack(side=tk.LEFT)

    def clean_username(value):
        username = value.strip()
        return username.split("@", 1)[0] if "@" in username else username

    def open_home(username, is_new_user=False):
        window.destroy()
        home.main(username, is_new_user=is_new_user)

    def show_login():
        clear_frame()
        username_entry = ctk.CTkEntry(
            frame, width=220, height=38, placeholder_text="Nom d'utilisateur"
        )
        username_entry.place(relx=0.5, y=65, anchor="center")

        password_frame = tk.Frame(frame, bg="white")
        password_frame.place(relx=0.5, y=115, anchor="center")
        password_entry = ctk.CTkEntry(
            password_frame, width=180, height=38,
            placeholder_text="Mot de passe", show="*"
        )
        password_entry.pack(side=tk.LEFT)
        add_eye(password_entry)

        ctk.CTkLabel(
            frame, text="Connexion", text_color="#133A5C",
            font=("Arial", 16, "bold")
        ).place(relx=0.5, y=25, anchor="center")

        def login_action():
            username = clean_username(username_entry.get())
            if not username or not password_entry.get().strip():
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return
            messagebox.showinfo("Connexion reussie", f"Bienvenue {username} !")
            window.after(200, lambda: open_home(username, is_new_user=False))

        ctk.CTkButton(
            frame, text="Se connecter", width=160, height=38,
            fg_color="#F77F00", hover_color="#E57100", command=login_action
        ).place(relx=0.5, y=170, anchor="center")
        ctk.CTkButton(
            frame, text="Mot de passe oublie ?", fg_color="transparent",
            text_color="#CC0000", hover_color="#e0e0e0", command=show_forgot
        ).place(relx=0.5, y=210, anchor="center")
        ctk.CTkButton(
            frame, text="Creer un compte", fg_color="transparent",
            text_color="#0077CC", hover_color="#e0e0e0", command=show_register
        ).place(relx=0.5, y=250, anchor="center")
        window.bind("<Return>", lambda event: login_action())

    def show_register():
        clear_frame()
        fields = {}
        labels = [
            ("name", "Nom complet", 65),
            ("email", "Email", 105),
            ("username", "Nom d'utilisateur", 145),
            ("password", "Mot de passe", 185),
            ("confirm", "Confirmer mot de passe", 225),
        ]
        ctk.CTkButton(
            frame, text="<", width=30, height=30, fg_color="transparent",
            text_color="#0077CC", hover_color="#e0e0e0", command=show_login
        ).place(x=10, y=10)
        ctk.CTkLabel(
            frame, text="Creer un compte", text_color="#133A5C",
            font=("Arial", 16, "bold")
        ).place(relx=0.5, y=25, anchor="center")
        for key, placeholder, y_position in labels:
            if key in ("password", "confirm"):
                entry_frame = tk.Frame(frame, bg="white")
                entry_frame.place(relx=0.5, y=y_position, anchor="center")
                entry = ctk.CTkEntry(
                    entry_frame, width=180, height=38,
                    placeholder_text=placeholder, show="*"
                )
                entry.pack(side=tk.LEFT)
                add_eye(entry)
            else:
                entry = ctk.CTkEntry(frame, width=220, height=38, placeholder_text=placeholder)
                entry.place(relx=0.5, y=y_position, anchor="center")
            fields[key] = entry

        def register_action():
            if any(not entry.get().strip() for entry in fields.values()):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            if fields["password"].get() != fields["confirm"].get():
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return
            username = clean_username(fields["username"].get())
            messagebox.showinfo("Succes", f"Compte cree pour {username} !")
            open_home(username, is_new_user=True)

        ctk.CTkButton(
            frame, text="Creer le compte", width=160, height=38,
            fg_color="#F77F00", hover_color="#E57100", command=register_action
        ).place(relx=0.5, y=270, anchor="center")

    def show_forgot():
        clear_frame()
        ctk.CTkButton(
            frame, text="<", width=30, height=30, fg_color="transparent",
            text_color="#0077CC", hover_color="#e0e0e0", command=show_login
        ).place(x=10, y=10)
        ctk.CTkLabel(
            frame, text="Mot de passe oublie", text_color="#133A5C",
            font=("Arial", 16, "bold")
        ).place(relx=0.5, y=25, anchor="center")
        email_entry = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Votre email")
        email_entry.place(relx=0.5, y=65, anchor="center")

        def continue_reset():
            if not email_entry.get().strip():
                messagebox.showerror("Erreur", "Veuillez saisir votre email.")
                return
            messagebox.showinfo("Information", "La reinitialisation est disponible dans cette demo.")
            show_login()

        ctk.CTkButton(
            frame, text="Continuer", width=160, height=38,
            fg_color="#F77F00", hover_color="#E57100", command=continue_reset
        ).place(relx=0.5, y=115, anchor="center")

    show_login()
    window.mainloop()


if __name__ == "__main__":
    main()
