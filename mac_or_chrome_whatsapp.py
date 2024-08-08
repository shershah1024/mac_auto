from is_app_running import is_app_running
from send_whatsapp_message import send_whatsapp_message
from send_message_whatsapp_web import send_message_via_whatsapp_web


def send_whatsapp_chat(contact_name, message):
    if is_app_running("WhatsApp"):
        send_whatsapp_message(contact_name, message)
    else:
        send_message_via_whatsapp_web(contact_name, message)


