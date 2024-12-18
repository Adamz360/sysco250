# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_low_stock_email(subject, message, recipient_list):
    send_mail(subject, message, 'noreply@inventorysystem.com', recipient_list)
