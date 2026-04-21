import os
from math import sqrt
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
import socket

console = Console()

def is_port_available(port):
    """
    Vérifie si un port est disponible.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def clear_screen():
    """Efface l'écran du terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_error(message):
    """Gère les erreurs en affichant un message formaté."""
    console.print(f"[red][ERREUR] {message}[/red]")

def get_user_choice(options: int) -> int:
    """
    Demande à l'utilisateur de choisir une option parmi un nombre donné.
    
    :param options: Nombre d'options disponibles.
    :return: L'option choisie (entier entre 1 et options).
    """
    while True:
        try:
            choice = input(f"Choisissez une option (1-{options}): ")
            choice_int = int(choice)
            if 1 <= choice_int <= options:
                return choice_int
            else:
                console.print(f"[red]Erreur : Veuillez entrer un nombre valide entre 1 et {options}.[/red]")
        except ValueError:
            console.print("[red]Erreur : Veuillez entrer un nombre valide.[/red]")

def pause(message="Appuyez sur Entrée pour continuer..."):
    """
    Met en pause l'exécution en attendant une entrée utilisateur.
    
    :param message: Message affiché pendant la pause.
    """
    input(f"\n{message}")

def display_title(title: str):
    """
    Affiche un titre dans un panel formaté.
    
    :param title: Texte du titre.
    """
    console.print(Panel(Text(title, justify="center", style="bold blue")))

def display_welcome_message():
    """
    Affiche un message de bienvenue encadré, adapté à la largeur du terminal.
    """
    clear_screen()
    try:
        terminal_width = os.get_terminal_size().columns
    except Exception:
        terminal_width = 80  # Valeur par défaut

    welcome_message = """
    ════════════════════════════════════════════════════
    ✨ Bienvenue dans l'application de gestion de marché numérique ! ✨

    🌟 Initiative de M. Plénou 🌟

    🚀 Pour une première utilisation, veuillez lancer la démo 
    afin de découvrir, étape par étape, le processus 
    de fonctionnement de l'application.

    Merci d'utiliser notre application !
    """
    # Nettoyage et centrage du texte
    centered_message = "\n".join(line.strip() for line in welcome_message.strip().split("\n"))
    border = "╭" + "─" * (terminal_width - 2) + "╮"
    footer = "╰" + "─" * (terminal_width - 2) + "╯"
    console.print(border, style="bold blue")
    console.print(centered_message, style="bold cyan", justify="center")
    console.print(footer, style="bold blue")

def confirm_action(message: str) -> bool:
    """
    Demande une confirmation à l'utilisateur.
    
    :param message: Message de confirmation.
    :return: True si la réponse est positive.
    """
    response = Prompt.ask(message + " (o/n)").lower().strip()
    return response in ['o', 'oui', 'y', 'yes']

def calculer_distance(x1, y1, x2, y2):
    """
    Calcule la distance euclidienne entre deux points.
    
    :param x1: Coordonnée X du premier point.
    :param y1: Coordonnée Y du premier point.
    :param x2: Coordonnée X du second point.
    :param y2: Coordonnée Y du second point.
    :return: Distance euclidienne.
    """
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
