from Database.models import Notification, User
from Core.utils import clear_screen, handle_error
from datetime import datetime

# Créer une notification
def create_notification(utilisateur, message):
    """
    Crée une notification pour un utilisateur.
    :param utilisateur: L'utilisateur à notifier.
    :param message: Le message de la notification.
    """
    notification = Notification(utilisateur=utilisateur, message=message)
    notification.save()
    print(f"Notification créée pour {utilisateur.username}.")

# Marquer une notification comme lue
def mark_notification_as_read(notification_id):
    """
    Marque une notification comme lue.
    :param notification_id: L'ID de la notification.
    """
    notification = Notification.objects(id=notification_id).first()
    if notification:
        notification.marquer_comme_lue()
        print(f"Notification '{notification.message}' marquée comme lue.")
    else:
        handle_error("Notification non trouvée.")

# Afficher les notifications non lues pour un utilisateur
def show_unread_notifications(utilisateur):
    """
    Affiche les notifications non lues pour un utilisateur.
    :param utilisateur: L'utilisateur dont on veut afficher les notifications.
    """
    notifications = Notification.objects(utilisateur=utilisateur, lue=False)
    if notifications:
        print(f"=== NOTIFICATIONS NON LUES POUR {utilisateur.username} ===")
        for notification in notifications:
            print(f"- {notification.message} (ID: {notification.id})")
    else:
        print("Aucune notification non lue.")

# Supprimer une notification
def delete_notification(notification_id):
    """
    Supprime une notification.
    :param notification_id: L'ID de la notification.
    """
    notification = Notification.objects(id=notification_id).first()
    if notification:
        notification.delete()
        print(f"Notification '{notification.message}' supprimée.")
    else:
        handle_error("Notification non trouvée.")

# Envoyer une notification à un utilisateur
def send_notification(username, message):
    """
    Envoie une notification à un utilisateur.
    :param username: Le nom d'utilisateur du destinataire.
    :param message: Le message de la notification.
    """
    utilisateur = User.objects(username=username).first()
    if utilisateur:
        create_notification(utilisateur, message)
    else:
        handle_error("Utilisateur non trouvé.")