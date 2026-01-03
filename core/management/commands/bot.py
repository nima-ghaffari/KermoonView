import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, 
    CallbackQueryHandler, MessageHandler, filters, ConversationHandler
)

from core.models import Tour, TourLeaderProfile, Comment, LeaderReview, User, Reservation, Hotel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

HOTEL_NAME, HOTEL_LOC, HOTEL_CAP = range(3)


@sync_to_async
def get_stats_db():
    u_count = User.objects.count()
    t_count = Tour.objects.count()
    r_count = Reservation.objects.count()
    pending_r = Reservation.objects.filter(status='pending').count()
    confirmed_res = Reservation.objects.filter(status='confirmed')
    income = sum(r.total_price for r in confirmed_res)
    
    return (
        f"📊 **آمار کلی سایت:**\n\n"
        f"👥 کاربران: {u_count}\n"
        f"🌍 تورها: {t_count}\n"
        f"🎫 رزروها: {r_count} (منتظر تایید: {pending_r})\n"
        f"💰 درآمد کل (تایید شده): {income:,} تومان"
    )

@sync_to_async
def get_users_list_data(limit=10):
    users = User.objects.all().order_by('-date_joined')[:limit]
    data = []
    for u in users:
        role_map = {'user': 'گردشگر', 'leader': 'لیدر', 'admin': 'ادمین'}
        data.append({
            'id': u.id,
            'username': u.username,
            'fullname': u.get_full_name() or u.username,
            'role': role_map.get(u.role, 'ناشناس'),
            'phone': u.phone_number,
            'is_active': u.is_active
        })
    return data

@sync_to_async
def toggle_user_status_db(user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser: 
            return None, "ادمین اصلی قابل مسدودسازی نیست."
        user.is_active = not user.is_active
        user.save()
        status = "فعال" if user.is_active else "مسدود"
        return user.username, status
    except User.DoesNotExist:
        return None, "کاربر یافت نشد."

@sync_to_async
def get_tours_data(active_only=True):
    qs = Tour.objects.select_related('leader').order_by('-id')
    if active_only:
        qs = qs.filter(is_active=True)[:10]
    else:
        qs = qs.filter(is_active=False)
    
    data = []
    for t in qs:
        data.append({
            'id': t.id,
            'title': t.title,
            'leader': t.leader.username,
            'capacity': t.capacity,
            'price': t.price
        })
    return data

@sync_to_async
def toggle_tour_status_db(tour_id):
    try:
        tour = Tour.objects.get(id=tour_id)
        tour.is_active = not tour.is_active
        tour.save()
        return tour.title, tour.is_active
    except:
        return None, None

@sync_to_async
def get_reservations_data(status='pending'):
    reservations = Reservation.objects.filter(status=status).select_related('user', 'tour').order_by('-created_at')[:10]
    data = []
    for r in reservations:
        data.append({
            'id': r.id,
            'tour_title': r.tour.title,
            'user_name': r.user.username,
            'count': r.passengers_count,
            'price': r.total_price
        })
    return data

@sync_to_async
def change_reservation_status_db(res_id, new_status):
    try:
        res = Reservation.objects.select_related('user').get(id=res_id)
        res.status = new_status
        res.save()
        return True, res.user.username
    except:
        return False, None

@sync_to_async
def create_hotel_db(name, loc, cap):
    Hotel.objects.create(name=name, location=loc, capacity=cap, is_approved=True)

@sync_to_async
def get_pending_leaders_data():
    leaders = TourLeaderProfile.objects.filter(is_verified=False).select_related('user')
    data = []
    for l in leaders:
        data.append({
            'id': l.id,
            'fullname': l.user.get_full_name() or l.user.username,
            'specialty': l.specialty,
            'motivation': l.motivation,
            'has_doc': bool(l.documents)
        })
    return data

@sync_to_async
def verify_leader_db(lid):
    try:
        l = TourLeaderProfile.objects.select_related('user').get(id=lid)
        l.is_verified = True
        l.save()
        return l.user.get_full_name()
    except: return None

@sync_to_async
def get_pending_comments_data():
    t_cm = Comment.objects.filter(is_approved=False).select_related('user', 'tour')
    l_cm = LeaderReview.objects.filter(is_approved=False).select_related('user', 'leader__user')
    
    t_data = [{'id': c.id, 'text': c.text, 'user': c.user.username, 'target': c.tour.title} for c in t_cm]
    l_data = [{'id': c.id, 'text': c.comment, 'user': c.user.username, 'target': c.leader.user.get_full_name()} for c in l_cm]
    
    return t_data, l_data

@sync_to_async
def approve_cm_db(ctype, cid):
    try:
        if ctype == 'tour': 
            obj = Comment.objects.get(id=cid)
        else: 
            obj = LeaderReview.objects.get(id=cid)
        obj.is_approved = True
        obj.save()
        return True
    except: return False


async def is_admin(update: Update):
    if update.effective_user.id != settings.TELEGRAM_ADMIN_ID:
        await update.message.reply_text("⛔ عدم دسترسی. فقط ادمین اصلی می‌تواند از این بات استفاده کند.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    
    keyboard = [
        ['👥 مدیریت کاربران', '🎫 مدیریت رزروها'],
        ['🌍 مدیریت تورها', '🏨 افزودن هتل'],
        ['✅ تاییدیه ها', '📊 آمار کلی']
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 سلام ادمین عزیز، به پنل مدیریت تلگرامی کرمون ویو خوش آمدید.", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    text = update.message.text

    if text == '📊 آمار کلی':
        msg = await get_stats_db()
        await update.message.reply_text(msg)

    elif text == '👥 مدیریت کاربران':
        users = await get_users_list_data()
        if not users:
            await update.message.reply_text("لیست کاربران خالی است.")
        else:
            await update.message.reply_text("📋 **لیست ۱۰ کاربر آخر:**")
            for u in users:
                status_icon = "🟢" if u['is_active'] else "🔴"
                keyboard = [[InlineKeyboardButton(f"{'مسدود کردن' if u['is_active'] else 'فعال کردن'}", callback_data=f"usr_toggle_{u['id']}")]]
                
                msg = f"{status_icon} **{u['username']}**\nنام: {u['fullname']}\nنقش: {u['role']}\nموبایل: {u['phone']}"
                await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

    elif text == '🎫 مدیریت رزروها':
        res_list = await get_reservations_data('pending')
        if not res_list:
            await update.message.reply_text("✅ همه رزروها تعیین تکلیف شده‌اند.")
        else:
            for r in res_list:
                keyboard = [
                    [
                        InlineKeyboardButton("✅ تایید بلیط", callback_data=f"res_conf_{r['id']}"),
                        InlineKeyboardButton("❌ رد کردن", callback_data=f"res_rej_{r['id']}")
                    ]
                ]
                msg = f"🎫 **رزرو جدید**\nتور: {r['tour_title']}\nکاربر: {r['user_name']}\nتعداد: {r['count']}\nمبلغ: {r['price']:,}"
                await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

    elif text == '🌍 مدیریت تورها':
        tours = await get_tours_data(active_only=True)
        if not tours:
            await update.message.reply_text("توری فعال نیست.")
        else:
            await update.message.reply_text("📋 **لیست تورهای فعال (جهت غیرفعال سازی):**")
            for t in tours:
                keyboard = [[InlineKeyboardButton("⛔ غیرفعال کردن", callback_data=f"tour_deact_{t['id']}")]]
                msg = f"🏕 {t['title']}\nلیدر: {t['leader']}\nظرفیت: {t['capacity']}\nقیمت: {t['price']:,}"
                await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

    elif text == '✅ تاییدیه ها':
        keyboard = [
            ['🏕 تایید تورهای جدید', '👤 تایید لیدرهای جدید'],
            ['💬 تایید نظرات', '🔙 بازگشت']
        ]
        await update.message.reply_text("بخش مورد نظر را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    elif text == '🔙 بازگشت':
        await start(update, context)
    elif text == '🏕 تایید تورهای جدید':
        tours = await get_tours_data(active_only=False)
        if not tours: await update.message.reply_text("✅ توری برای تایید نیست.")
        for t in tours:
            kb = [[InlineKeyboardButton("✅ تایید انتشار", callback_data=f"tour_act_{t['id']}")]]
            msg = f"🏕 {t['title']}\nلیدر: {t['leader']}\nقیمت: {t['price']:,}"
            await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif text == '👤 تایید لیدرهای جدید':
        leaders = await get_pending_leaders_data()
        if not leaders: await update.message.reply_text("✅ لیدری برای تایید نیست.")
        for l in leaders:
            kb = [[InlineKeyboardButton("✅ تایید لیدر", callback_data=f"lead_ver_{l['id']}")]]
            msg = f"👤 {l['fullname']}\n🎯 تخصص: {l['specialty']}\n💡 انگیزه: {l['motivation'][:100]}..."
            if l['has_doc']: msg += "\n📎 (دارای مدرک)"
            await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

    elif text == '💬 تایید نظرات':
        tc, lc = await get_pending_comments_data()
        if not tc and not lc: await update.message.reply_text("✅ نظری برای تایید نیست.")
        
        for c in tc:
            kb = [[InlineKeyboardButton("✅ تایید نظر", callback_data=f"cm_tour_{c['id']}")]]
            await update.message.reply_text(f"📝 نظر تور: {c['target']}\n👤 کاربر: {c['user']}\nمتن: {c['text']}", reply_markup=InlineKeyboardMarkup(kb))
            
        for c in lc:
            kb = [[InlineKeyboardButton("✅ تایید نظر", callback_data=f"cm_lead_{c['id']}")]]
            await update.message.reply_text(f"📝 نظر لیدر: {c['target']}\n👤 کاربر: {c['user']}\nمتن: {c['text']}", reply_markup=InlineKeyboardMarkup(kb))
    
    elif text == '🏨 افزودن هتل':
        await update.message.reply_text("🏨 نام هتل را وارد کنید:", reply_markup=ReplyKeyboardRemove())
        return HOTEL_NAME

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("usr_toggle_"):
        uid = int(data.split("_")[2])
        uname, status = await toggle_user_status_db(uid)
        if uname: await query.edit_message_text(f"✅ وضعیت کاربر {uname} به {status} تغییر یافت.")
        else: await query.edit_message_text("❌ خطا در تغییر وضعیت یا تلاش برای مسدود کردن ادمین.")

    elif data.startswith("res_conf_"):
        rid = int(data.split("_")[2])
        ok, uname = await change_reservation_status_db(rid, 'confirmed')
        if ok: await query.edit_message_text(f"✅ بلیط برای {uname} صادر شد (تایید شد).")

    elif data.startswith("res_rej_"):
        rid = int(data.split("_")[2])
        ok, uname = await change_reservation_status_db(rid, 'rejected')
        if ok: await query.edit_message_text(f"⛔ درخواست رزرو {uname} رد شد.")

    elif data.startswith("tour_deact_"):
        tid = int(data.split("_")[2])
        title, active = await toggle_tour_status_db(tid)
        await query.edit_message_text(f"⛔ تور '{title}' غیرفعال شد.")

    elif data.startswith("tour_act_"):
        tid = int(data.split("_")[2])
        title, active = await toggle_tour_status_db(tid)
        await query.edit_message_text(f"✅ تور '{title}' فعال و منتشر شد.")

    elif data.startswith("lead_ver_"):
        lid = int(data.split("_")[2])
        name = await verify_leader_db(lid)
        await query.edit_message_text(f"✅ لیدر {name} تایید شد.")

    elif data.startswith("cm_"):
        ctype = 'tour' if 'tour' in data else 'leader'
        cid = int(data.split("_")[2])
        if await approve_cm_db(ctype, cid): await query.edit_message_text("✅ نظر منتشر شد.")

async def hotel_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['h_name'] = update.message.text
    await update.message.reply_text("📍 آدرس هتل را وارد کنید:")
    return HOTEL_LOC

async def hotel_loc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['h_loc'] = update.message.text
    await update.message.reply_text("🔢 ظرفیت کل هتل را وارد کنید (عدد):")
    return HOTEL_CAP

async def hotel_cap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cap = int(update.message.text)
        await create_hotel_db(context.user_data['h_name'], context.user_data['h_loc'], cap)
        
        keyboard = [
            ['👥 مدیریت کاربران', '🎫 مدیریت رزروها'],
            ['🌍 مدیریت تورها', '🏨 افزودن هتل'],
            ['✅ تاییدیه ها', '📊 آمار کلی']
        ]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ هتل با موفقیت ثبت شد.", reply_markup=markup)
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("❌ لطفا فقط عدد وارد کنید. دوباره تلاش کنید:")
        return HOTEL_CAP

async def cancel_hotel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return ConversationHandler.END



class Command(BaseCommand):
    help = 'Runs the Advanced Telegram Admin Bot'

    def handle(self, *args, **options):
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(self.style.ERROR("Error: TELEGRAM_BOT_TOKEN missing in settings."))
            return

        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        hotel_conv = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex('^🏨 افزودن هتل$'), handle_message)],
            states={
                HOTEL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_name)],
                HOTEL_LOC: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_loc)],
                HOTEL_CAP: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_cap)],
            },
            fallbacks=[CommandHandler('cancel', cancel_hotel)]
        )

        app.add_handler(hotel_conv)
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        self.stdout.write(self.style.SUCCESS("🤖 Advanced Admin Bot started!"))
        app.run_polling()