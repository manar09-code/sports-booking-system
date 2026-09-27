# news.py
# Import necessary modules for GUI creation and functionality
from tkinter import *  # Import all Tkinter widgets for building the GUI
from tkinter import scrolledtext  # Import scrolled text widget for chat area
import customtkinter as ctk  # Import customtkinter for modern-looking widgets
import home  # Import the home module for navigation
import random  # Import random for potential random selections (not used in this file)
import pandas as pd  # Import pandas for data manipulation
import os  # Import os for file path operations
from datetime import datetime  # Import datetime for date handling


def main():  # Define the main function to display the news and chatbot page
    fenetre = Tk()  # Create the main Tkinter window
    fenetre.title("Actualités - Système de Réservation Sportive")  # Set the window title
    fenetre.configure(bg="#f2f2f2")  # Configure the background color
    fenetre.state("zoomed")  # Maximize the window to full screen

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=100, height=40,  # Create a back button to return to home
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 12, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)  # Pack the button at the top left

    # --- Titre de la page ---
    ctk.CTkLabel(fenetre, text="Actualités et Informations", font=("Arial", 28, "bold"),  # Create a title label for the page
                 text_color="#133A5C").pack(pady=20)  # Pack the label with padding

    # --- Frame principal ---
    main_frame = Frame(fenetre, bg="#f2f2f2")  # Create the main frame to hold news and chatbot sections
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)  # Pack the frame to fill the window

    # --- News Section ---
    news_frame = LabelFrame(main_frame, text="Titres d'Actualités", font=("Arial", 14, "bold"), bg="white")  # Create a labeled frame for news titles
    news_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)  # Pack the frame on the left side

    news_titles = [  # List of news titles to display
        "Tournoi de Football ce weekend ! - Rejoignez-nous pour un tournoi excitant avec des équipes locales.",
        "Nouvelle salle de Padel ouverte ! - Découvrez notre nouvelle salle équipée des dernières technologies.",
        "Promotion spéciale abonnés Premium ! - Profitez de 20% de réduction sur tous les forfaits premium.",
        "Événement Handball le mois prochain - Événement handball inoubliable avec des équipes professionnelles.",
        "Championnat de Basketball régional - Le championnat régional commence ce samedi, réservez vos places !",
        "Cours de Tennis pour débutants - Cours gratuits de tennis tous les mercredis soir.",
        "Journée portes ouvertes au complexe - Venez visiter notre complexe sportif ce dimanche.",
        "Réduction sur les abonnements annuels - Économisez avec nos abonnements annuels à prix réduit."
    ]

    for title in news_titles:  # Loop through each news title and create a label for it
        ctk.CTkLabel(news_frame, text=title, font=("Arial", 12), text_color="#333",
                     wraplength=400, justify="left").pack(pady=5, padx=10, anchor="w")  # Pack the label with wrapping

    # --- Chatbot Section ---
    chatbot_frame = LabelFrame(main_frame, text="Assistant IA - Conseils de Réservation", font=("Arial", 14, "bold"), bg="white")  # Create a labeled frame for the chatbot
    chatbot_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)  # Pack the frame on the right side

    chat_area = scrolledtext.ScrolledText(chatbot_frame, wrap=WORD, width=50, height=15, font=("Arial", 10))  # Create a scrolled text area for chat
    chat_area.pack(pady=10, padx=10, fill=BOTH, expand=True)  # Pack the chat area
    chat_area.insert(END, "Assistant IA: Bonjour ! Je peux vous aider avec des conseils de réservation. Posez-moi une question !\n\n")  # Insert initial message
    chat_area.config(state=DISABLED)  # Disable editing of the chat area

    # Typing indicator
    typing_label = Label(chatbot_frame, text="", font=("Arial", 10, "italic"), fg="gray", bg="white")  # Create a label for typing indicator
    typing_label.pack(pady=(0, 5))  # Pack the typing label

    entry_frame = Frame(chatbot_frame, bg="white")  # Create a frame for user input and send button
    entry_frame.pack(fill=X, padx=10, pady=5)  # Pack the entry frame

    user_entry = ctk.CTkEntry(entry_frame, placeholder_text="Tapez votre question ici...", width=300)  # Create entry for user input
    user_entry.pack(side=LEFT, fill=X, expand=True)  # Pack the entry on the left

    # Quick reply buttons
    quick_replies_frame = Frame(chatbot_frame, bg="white")  # Create a frame for quick reply buttons
    quick_replies_frame.pack(fill=X, padx=10, pady=5)  # Pack the quick replies frame

    quick_replies = ["Prix", "Disponibilité", "Réservation", "Contact", "Terrains"]  # List of quick reply options

    def quick_reply_click(reply):  # Define function to handle quick reply button clicks
        user_entry.insert(0, reply.lower())  # Insert the reply into the entry field
        send_message()  # Call send_message function

    for reply in quick_replies:  # Loop through quick replies and create buttons
        btn = ctk.CTkButton(quick_replies_frame, text=reply, width=80, height=25, font=("Arial", 10),
                            command=lambda r=reply: quick_reply_click(r))  # Create button with command
        btn.pack(side=LEFT, padx=2)  # Pack the button

    conversation_history = []  # List to store conversation history

    def send_message():  # Define function to send user message and get response
        user_msg = user_entry.get().strip()  # Get and strip user message
        if user_msg:  # If message is not empty
            chat_area.config(state=NORMAL)  # Enable editing of chat area
            chat_area.insert(END, f"Vous: {user_msg}\n")  # Insert user message
            chat_area.config(state=DISABLED)  # Disable editing
            user_entry.delete(0, END)  # Clear entry field
            chat_area.see(END)  # Scroll to end

            # Show typing indicator
            typing_label.config(text="Assistant IA est en train d'écrire...")  # Set typing text
            fenetre.update()  # Update the window

            response = get_ai_response(user_msg, conversation_history)  # Get AI response
            conversation_history.append({"role": "user", "content": user_msg})  # Add to history
            conversation_history.append({"role": "assistant", "content": response})  # Add response to history

            # Hide typing indicator
            typing_label.config(text="")  # Clear typing text

            chat_area.config(state=NORMAL)  # Enable editing
            chat_area.insert(END, f"Assistant IA: {response}\n\n")  # Insert response
            chat_area.config(state=DISABLED)  # Disable editing
            chat_area.see(END)  # Scroll to end

    send_btn = ctk.CTkButton(entry_frame, text="Envoyer", command=send_message, width=80)  # Create send button
    send_btn.pack(side=RIGHT, padx=5)  # Pack the button on the right

    # --- Contact Info ---
    contact_frame = LabelFrame(fenetre, text="Informations de Contact", font=("Arial", 14, "bold"), bg="white")  # Create a labeled frame for contact information
    contact_frame.pack(fill=X, padx=20, pady=10)  # Pack the contact frame

    contact_info = """Contact details
    Adresse: Complexe Sportif Tunis, Avenue Habib Bourguiba, Tunis
    Téléphone: +216 71 123 456
    Email: contact@complexesportiftunis.tn
    Heures d'ouverture: Lundi-Dimanche 8h-22h
    """
    ctk.CTkLabel(contact_frame, text=contact_info, font=("Arial", 12), text_color="#333").pack(pady=10, padx=10)  # Create and pack the contact label

    fenetre.mainloop()

def get_ai_response(user_msg, conversation_history=[]):  # Function to get AI response using fallback responses
    # Load reservations data for context
    csv_file = os.path.join(os.path.dirname(__file__), "reservations.csv")  # Path to the reservations CSV file
    availability_info = ""  # Initialize availability info string
    try:
        if os.path.isfile(csv_file):  # Check if the CSV file exists
            df = pd.read_csv(csv_file, parse_dates=["date"], dayfirst=True)  # Load the CSV into a DataFrame
            df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')  # Parse dates

            # Real-time availability checking
            today = datetime.now().date()  # Get today's date
            available_slots = {}  # Dictionary to hold available slots per terrain
            terrains = ["Terrain de Football", "Terrain de Basketball", "Terrain de Tennis", "Salle de Handball", "Terrain de Padel"]  # List of terrains
            hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]  # List of time slots

            for terrain in terrains:  # Loop through each terrain
                available_slots[terrain] = []  # Initialize list for available hours
                for hour in hours:  # Loop through each hour slot
                    conflict = any((res["date"] == str(today) and res["heure"] == hour and res["terrain"] == terrain) for res in df.to_dict('records'))  # Check for conflicts
                    if not conflict:  # If no conflict, add to available slots
                        available_slots[terrain].append(hour)

            availability_info = "Disponibilités aujourd'hui: " + "; ".join([f"{t}: {', '.join(h) if h else 'Aucune'}" for t, h in available_slots.items()])  # Build availability string
    except Exception as e:  # If loading data fails
        availability_info = "Informations de disponibilité non disponibles."  # Set default availability

    # Enhanced fallback to keyword-based responses
    responses = {  # Dictionary of keyword-based responses in French
        "meilleur": "Les meilleurs jours pour réserver sont les midis en semaine (lundi-mercredi) car moins de demandes.",
        "prix": "Les prix varient selon le forfait: Standard 33 TND (1h, 2 joueurs), Premium 66 TND (2h, 4 joueurs), VIP 99 TND (3h, 6 joueurs). Réductions de 10% le weekend et pour les abonnements mensuels.",
        "disponibilité": f"Vérifiez la disponibilité en temps réel dans l'onglet Réservation. {availability_info}",
        "contact": "Appelez-nous au +216 71 123 456 ou envoyez un email à contact@complexesportiftunis.tn. Heures d'ouverture: Lundi-Dimanche 8h-22h.",
        "réservation": "Pour réserver, allez dans l'onglet Réservation, choisissez un terrain et remplissez le formulaire. Nous proposons des alternatives automatiques en cas de conflit.",
        "réserver": "Pour réserver, allez dans l'onglet Réservation, choisissez un terrain et remplissez le formulaire. Nous proposons des alternatives automatiques en cas de conflit.",
        "payer": "Le paiement se fait après la réservation via notre système sécurisé. Acceptez cartes de crédit, PayPal et espèces.",
        "terrain": "Nous avons plusieurs terrains: Football, Basketball, Tennis, Handball, Padel. Tous équipés de matériel de qualité.",
        "heure": "Les créneaux disponibles sont de 8h à 23h, par tranches de 2h. Réservez à l'avance pour garantir votre place.",
        "abonnement": "L'abonnement mensuel offre 10% de réduction sur toutes les réservations et des avantages exclusifs comme la priorité de réservation.",
        "football": "Notre terrain de football est idéal pour les matchs amicaux et les entraînements. Réservez dès maintenant !",
        "basketball": "Le terrain de basketball est parfait pour les sessions de dribble et de tir. Équipé de paniers professionnels.",
        "tennis": "Les courts de tennis sont disponibles pour les débutants et les professionnels. Surface en terre battue de qualité.",
        "handball": "La salle de handball est climatisée et équipée pour des matchs intenses. Idéale pour les équipes.",
        "padel": "Le terrain de padel est notre dernière addition, avec des murs en verre et un éclairage LED.",
        "promotion": "Profitez de nos promotions actuelles: 20% de réduction pour les abonnés premium et réductions weekend.",
        "événement": "Ne manquez pas nos événements spéciaux: tournois, journées portes ouvertes et cours pour débutants.",
        "hi": "Bonjour ! Comment puis-je vous aider avec vos réservations sportives aujourd'hui ?",
        "hello": "Salut ! Je suis là pour vous assister avec toutes vos questions sur les réservations.",
        "bonjour": "Bonjour ! Ravi de vous aider avec le système de réservation sportive.",
        "salut": "Salut ! Que puis-je faire pour vous concernant les terrains et réservations ?",
        "thank": "De rien ! N'hésitez pas si vous avez d'autres questions.",
        "thanks": "Avec plaisir ! Je suis là pour vous aider.",
        "merci": "De rien ! Bonne journée et à bientôt pour une réservation !",
        "bye": "Au revoir ! Passez une excellente journée sportive.",
        "au revoir": "Au revoir ! Revenez quand vous voulez pour réserver.",
        "default": "Je peux vous aider avec des conseils sur les réservations, prix, terrains, disponibilités, heures, contacts ou événements. Posez une question spécifique ou utilisez les boutons rapides !"
    }
    user_lower = user_msg.lower()  # Convert user message to lowercase for matching
    for key in responses:  # Loop through response keys
        if key in user_lower:  # If key is in user message
            return responses[key]  # Return matching response
    return responses["default"]  # Return default response if no match

def back_home(win):  # Function to return to the home page
    win.destroy()  # Destroy the current window
    home.main()  # Call the main function of the home module

if __name__ == "__main__":  # If this script is run directly
    main()  # Call the main function
