from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
import json
import logging

from .models import User, TourLeaderProfile, Reservation, Comment, LeaderReview

logger = logging.getLogger(__name__)

def send_telegram_alert(text, keyboard=None):
    if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': settings.TELEGRAM_ADMIN_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    if keyboard:
        payload['reply_markup'] = json.dumps(keyboard)
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        logger.error(f"Telegram Alert Error: {e}")

@receiver(post_save, sender=TourLeaderProfile)
def update_user_role_on_verify(sender, instance, created, **kwargs):

    if instance.is_verified and instance.user.role != 'leader':
        instance.user.role = 'leader'
        instance.user.save()
        print(f"User {instance.user.username} upgraded to LEADER.")


@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created and instance.role == 'user':
        msg = f"👤 ثبت نام کاربر جدید\n\nنام کاربری: {instance.username}\nنام: {instance.get_full_name()}"
        keyboard = {'inline_keyboard': [[{'text': 'مدیریت کاربر', 'callback_data': f'usr_toggle_{instance.id}'}]]}
        send_telegram_alert(msg, keyboard)

@receiver(post_save, sender=TourLeaderProfile)
def notify_leader_request(sender, instance, created, **kwargs):
    if not instance.is_verified and instance.documents:
        msg = (
            f"🎓 درخواست ارتقا به تور لیدر\n\n"
            f"👤 نام: {instance.user.get_full_name()}\n"
            f"🎯 تخصص: {instance.specialty}\n"
            f"💡 انگیزه: {instance.motivation[:100]}..."
        )
        keyboard = {'inline_keyboard': [[{'text': '✅ تایید لیدر', 'callback_data': f'lead_ver_{instance.id}'}]]}
        send_telegram_alert(msg, keyboard)

@receiver(post_save, sender=Reservation)
def notify_new_reservation(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        msg = (
            f"🎫 **رزرو جدید**\n\n"
            f"🏕 تور: {instance.tour.title}\n"
            f"👤 کاربر: {instance.user.username}\n"
            f"👥 تعداد: {instance.passengers_count}\n"
            f"💰 مبلغ: {instance.total_price:,}"
        )
        keyboard = {'inline_keyboard': [[{'text': '✅ تایید', 'callback_data': f'res_conf_{instance.id}'}, {'text': '❌ رد', 'callback_data': f'res_rej_{instance.id}'}]]}
        send_telegram_alert(msg, keyboard)

from .models import Tour
@receiver(post_save, sender=Tour)
def notify_new_tour(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        msg = (
            f"🏕 **ثبت تور جدید (در انتظار تایید)**\n\n"
            f"عنوان: {instance.title}\n"
            f"لیدر: {instance.leader.get_full_name()}\n"
            f"قیمت: {instance.price:,}"
        )
        keyboard = {'inline_keyboard': [[{'text': '✅ انتشار تور', 'callback_data': f'tour_act_{instance.id}'}]]}
        send_telegram_alert(msg, keyboard)