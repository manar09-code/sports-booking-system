# stats.py
from tkinter import *
import customtkinter as ctk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import home
from datetime import datetime
from tkinter import filedialog, messagebox

def main():
    fenetre = Tk()
    fenetre.title("Statistiques Interactives - Réservations Sportives")
    fenetre.configure(bg="#f2f2f2")
    fenetre.state("zoomed")

    # --- Menu Bar ---
    menubar = Menu(fenetre)
    fenetre.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=file_menu)
    file_menu.add_command(label="Exporter vers Excel", command=lambda: export_to_excel(df))
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=fenetre.quit)

    stats_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Statistiques", menu=stats_menu)
    stats_menu.add_command(label="Progression des Réservations", command=lambda: switch_view("matplotlib"))
    stats_menu.add_command(label="Terrains les Plus Réservés", command=lambda: switch_view("pandas"))

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=80, height=30,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 10, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- Titre ---
    ctk.CTkLabel(fenetre, text="Statistiques des Réservations", font=("Arial", 28, "bold"),
                 text_color="#133A5C").pack(pady=20)

    view_var = StringVar(value="matplotlib")

    def switch_view(view):
        view_var.set(view)
        update_stats()

    # --- Chargement CSV ---
    csv_file = os.path.join(os.path.dirname(__file__), "reservations.csv")
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file, parse_dates=["date"], dayfirst=True)
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
    else:
        df = pd.DataFrame(columns=["nom", "date", "heure", "terrain", "forfait", "abonnement", "equipment", "coaching", "user"])

    # --- Filtres ---
    frame_filters = Frame(fenetre, bg="#f2f2f2")
    frame_filters.pack(pady=10)

    ctk.CTkLabel(frame_filters, text="Filtrer par mois :", font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
    month_var = StringVar(value=datetime.now().strftime("%m/%Y"))
    months = sorted(df['date'].dt.strftime("%m/%Y").dropna().unique()) if not df.empty else []
    month_combo = ctk.CTkComboBox(frame_filters, values=months, variable=month_var, width=120)
    month_combo.pack(side=LEFT, padx=5)

    ctk.CTkLabel(frame_filters, text="Filtrer par terrain :", font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
    terrain_var = StringVar(value="Tous")
    all_terrains = ["Tous","Terrain de Football", "Terrain de Basketball", "Court de Tennis", "Salle de Handball", "Court de Padel"]
    terrain_combo = ctk.CTkComboBox(frame_filters, values=all_terrains, variable=terrain_var, width=150)
    terrain_combo.pack(side=LEFT, padx=5)

    # Update button
    ctk.CTkButton(frame_filters, text="Mettre à jour", width=80, height=30,
                  fg_color="#133A5C", hover_color="#F77F00", font=("Arial", 10, "bold"),
                  command=lambda: update_stats()).pack(side=LEFT, padx=10)

    # --- Frame pour stats ---
    frame_stats = Frame(fenetre, bg="#f2f2f2")
    frame_stats.pack(pady=10, padx=20, fill=X)

    # --- Frame pour graph ---
    frame_graph = Frame(fenetre, bg="#f2f2f2")
    frame_graph.pack(pady=20, fill=BOTH, expand=True)

    # --- Fonction pour mettre à jour stats et graph ---
    def update_stats():
        for widget in frame_stats.winfo_children():
            widget.destroy()
        for widget in frame_graph.winfo_children():
            widget.destroy()

        # Filtrage
        filtered_df = df.copy()
        month_selected = month_var.get()
        if month_selected and month_selected != "":
            month_dt = datetime.strptime("01/" + month_selected, "%d/%m/%Y")
            filtered_df = filtered_df[(filtered_df["date"].dt.month == month_dt.month) &
                                      (filtered_df["date"].dt.year == month_dt.year)]
        terrain_selected = terrain_var.get()
        if terrain_selected != "Tous":
            filtered_df = filtered_df[filtered_df["terrain"] == terrain_selected]

        if view_var.get() == "pandas":
            # Most Recommended Fields: bar charts for top terrains, days, times
            if not filtered_df.empty:
                fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

                # Top terrains
                terrain_counts = filtered_df['terrain'].value_counts().head(5)
                terrain_counts.plot(kind='bar', color="#F77F00", ax=ax1, edgecolor='black', linewidth=0.5)
                ax1.set_title("Terrains les Plus Réservés", fontsize=14, fontweight='bold')
                ax1.set_ylabel("Nombre de Réservations", fontsize=12)
                ax1.set_xlabel("Terrain", fontsize=12)
                ax1.tick_params(axis='x', rotation=45)
                ax1.grid(axis='y', linestyle='--', alpha=0.7)

                # Top days
                day_counts = filtered_df['date'].dt.day_name().value_counts().head(5)
                day_counts.plot(kind='bar', color="#133A5C", ax=ax2, edgecolor='black', linewidth=0.5)
                ax2.set_title("Jours les Plus Réservés", fontsize=14, fontweight='bold')
                ax2.set_ylabel("Nombre de Réservations", fontsize=12)
                ax2.set_xlabel("Jour", fontsize=12)
                ax2.tick_params(axis='x', rotation=45)
                ax2.grid(axis='y', linestyle='--', alpha=0.7)

                # Top times
                time_counts = filtered_df['heure'].value_counts().head(5)
                time_counts.plot(kind='bar', color="#1F5061", ax=ax3, edgecolor='black', linewidth=0.5)
                ax3.set_title("Heures les Plus Populaires", fontsize=14, fontweight='bold')
                ax3.set_ylabel("Nombre de Réservations", fontsize=12)
                ax3.set_xlabel("Heure", fontsize=12)
                ax3.tick_params(axis='x', rotation=45)
                ax3.grid(axis='y', linestyle='--', alpha=0.7)

                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=frame_graph)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        elif view_var.get() == "matplotlib":
            # Progress: cumulative reservations over time curve
            if not filtered_df.empty:
                filtered_df = filtered_df.sort_values('date')
                cumulative = filtered_df.groupby('date').size().cumsum()
                fig, ax = plt.subplots(figsize=(12, 6))
                cumulative.plot(kind='line', color="#F77F00", marker='o', markersize=6, linewidth=2, ax=ax, linestyle='-', alpha=0.8)
                ax.set_title("Progression des Réservations", fontsize=16, fontweight='bold')
                ax.set_ylabel("Nombre Cumulé de Réservations", fontsize=12)
                ax.set_xlabel("Date", fontsize=12)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='both', linestyle='--', alpha=0.7)
                ax.fill_between(cumulative.index, cumulative.values, color="#F77F00", alpha=0.3)  # Add fill for visual appeal

                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=frame_graph)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # --- Mettre à jour au changement ---
    month_combo.configure(command=lambda _: update_stats())
    terrain_combo.configure(command=lambda _: update_stats())

    # Initial
    update_stats()

    fenetre.mainloop()

def back_home(win):
    win.destroy()
    home.main()

def export_to_excel(df):
    if df.empty:
        messagebox.showwarning("Avertissement", "Aucune donnée à exporter.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Fichiers Excel", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Succès", f"Données exportées vers {file_path}")

if __name__ == '__main__':
    main()
