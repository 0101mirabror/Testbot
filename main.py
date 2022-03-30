from telegram import (Update, 
                      Contact,
                      ReplyKeyboardMarkup,
                      KeyboardButton)

from telegram.ext import  (Updater,
                           CallbackContext,
                           Dispatcher,
                           CommandHandler,
                           MessageHandler,
                           Filters,
                           ConversationHandler,
                           MessageFilter
                           )
import logging
from openpyxl import load_workbook, Workbook
 
    
updater = Updater(token="5200114262:AAFO9hhfgCQL1FjQYOxBF0l2iILz5pz16EE")
logging.basicConfig(level=logging.DEBUG)

class FilterFullname(MessageFilter):
    
    def filter(self, message):
        
        fullname = message.text
        return (len(fullname.split()) > 1) and  fullname.split()[0][0].isupper() and fullname.split()[1][0].isupper()
filter_fullname =  FilterFullname()

class FilterNumber(MessageFilter):
    
    def filter(self, message):
        phone_number = message.text
        return (len(phone_number) == 14 or len(phone_number) == 9) and phone_number[1:].isnumeric()
filter_number = FilterNumber()

BUTTON = ReplyKeyboardMarkup([["📝 Ro'yxatdan o'tish"]],resize_keyboard=True)

def start_bot(update: Update, context: CallbackContext):
    update.effective_chat.send_action('typing')
    update.message.reply_text("**************************"\
                              "**************************")
    update.message.reply_html("Olimpiyadada ishtirok etish uchun <b> Ro'yxatdan o'tish </b> tugmasini bosing.", reply_markup=BUTTON)
    context.user_data['id'] = update.effective_user.id
 
    
         
def get_data(update: Update, context: CallbackContext):
    update.effective_chat.send_action('typing')
    update.message.reply_text("F.I.SH. kiriting")


def get_contact(update: Update, context: CallbackContext):
    context.user_data['familiya'] = (update.message.text).split()[0]
    print(context.user_data['familiya'])
    context.user_data['ism'] = (update.message.text).split()[1]
    if len((update.message.text).split()) == 3:
        context.user_data['sharif'] = (update.message.text).split()[2]
    key = ReplyKeyboardMarkup([[KeyboardButton("📱 Telefon raqamni jo'natish", request_contact=True)]],
                                 resize_keyboard=True)
    update.message.reply_text("Tugmani bosib telefon raqamingizni yuboring \nYoki raqamingizni kiriting.", reply_markup=key)
 
 
def get_location(update: Update, context: CallbackContext):
 
    key = ReplyKeyboardMarkup([[KeyboardButton("📍 Joylashgan manzilni jo'natish", request_location=True)]],
                                 resize_keyboard=True)
    update.message.reply_text("Manzilni yuborish uchun quyidagi tugmani bosing", reply_markup=key)

def get_fullname(update: Update, context: CallbackContext):
    context.chat_data['fullname'] = update.message.text
     
def main_menu(update: Update, context: CallbackContext):
    update.message.reply_html("BILIMTESTBOT", reply_markup=ReplyKeyboardMarkup([["🔠 Test Ishlash"], [" ℹ️ Ma'lumot", "👤 Profilim"]], resize_keyboard=True))

def check_fullname(update: Update, context: CallbackContext):
    # text = ism familiya 
    
    text = update.message.text
    update.message.reply_text(text+" "+f"{text.split()}")
    if len(text.split()) > 1:
        if text.split()[0][0].isupper() and text.split()[1][0].isupper():
            update.message.reply_text('Tugmani bosib telefon raqamingizni yuboring')
        else:
            update.message.reply_text("Familiya, ism, sharifingizni to'g'ri kiriting")
    
            
    
    

    
updater.dispatcher.add_handler(CommandHandler('start', start_bot))
updater.dispatcher.add_handler(MessageHandler( filters=Filters.text("📝 Ro'yxatdan o'tish"), callback=get_data))
updater.dispatcher.add_handler(MessageHandler( filters=filter_fullname, callback=get_contact))
updater.dispatcher.add_handler(MessageHandler( filters=Filters.contact, callback=main_menu))
updater.dispatcher.add_handler(MessageHandler( filters=Filters.text("Location"), callback=get_location))

updater.start_polling()
updater.idle()


# if update.message.text == '📝 Ro\'yxatdan o\'tish':



# updater.dispatcher.add_handler(MessageHandler( filters=Filters.text(), callback=check_fullname))
# updater.dispatcher.add_handler(MessageHandler( filters=Filters.text(["F.I.SH. kiriting", "Familiya, ism, sharifingizni to'g'ri kiriting"]), callback=get_fullname))
# updater.dispatcher.add_handler(MessageHandler( filters=Filters.text("Familiya, ism, sharifingizni to'g'ri kiriting"), callback=check_fullname))

# BUTTON2 = ReplyKeyboardMarkup([["📱 Telefon raqamni jo'natish"]], resize_keyboard=True)
 
# updater.dispatcher.add_handler(ConversationHandler(
#                                 entry_points=[CommandHandler('start', start_bot)],
#                                 states={
#                                     '1':[MessageHandler(filters=Filters.text("Ro'yxatdan o'tish"), callback=send_data)]
#                                 },
#                                 fallbacks=[MessageHandler(filters=Filters.command, callback=cancel)]
# ))
# def cancel(update: Update, context: CallbackContext):
#     """ Cancel current conversation """
#     update.message.reply_text('Siz noto\'g\'ri buyruqni belgiladingiz\n'\
#                               'Botni ishga tushirish uchun /start ni bosing')
#     return ConversationHandler.END 