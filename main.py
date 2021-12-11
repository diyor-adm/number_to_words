from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from function import uz_text, to_cyrillic
from telegram.ext import Updater,InlineQueryHandler, CommandHandler, dispatcher,CallbackContext, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle
from num2words import num2words 
import inflect
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

flag = ''
text_flag = '' 
updater = Updater(token='2125757852:AAFKLikrUEGcsaEWE0sxmErE6zGnJzRe7SE')

def send_welcome(update: Update, context: CallbackContext):
   update.message.reply_text(f'Assalomu alaykum {update.effective_user.first_name}, sonlarni matn ko`rinishiga o`girib beruvchi botga xush kelibsiz😊\nSizga kerak bo`lgan tilni tanlang!', reply_markup=main_menu_keyboard())
 
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='uz_latin'),
            InlineKeyboardButton('🇷🇺 Русский', callback_data='rus')],
            [InlineKeyboardButton('🇺🇿 Ўзбекча', callback_data='uzbek_kirill_key'), 
            InlineKeyboardButton('🇬🇧 English ', callback_data='en_key')]]
  return InlineKeyboardMarkup(keyboard)

def uzbek_latin(update: Update, context: CallbackContext):
    global flag
    flag = 'uz'
    update.callback_query.message.edit_text("🇺🇿 O'zbek tili tanlandi!")
    
def uzbek_kirill_key(update: Update, context: CallbackContext):
    global flag
    flag = 'uz_kr'
    update.callback_query.message.edit_text("🇺🇿 Ўзбек тили танланди!")
def rus(update: Update, context: CallbackContext):
    global flag
    flag = 'ru'
    update.callback_query.message.edit_text("🇷🇺 Русский был выбран!")
def en_key(update: Update, context: CallbackContext):
    global flag
    flag = 'en'
    update.callback_query.message.edit_text("🇬🇧 Language has been changed to English")

def check_text(text: str):
	text_list = text.strip().split(' ')
	for i in text_list:
		if i.isdigit():
			return int(i), True
	return 0, False

def num2words_ru(num): 
    return num2words(int(num), lang='ru')
    
def num2words_en(num):
    words = inflect.engine().number_to_words(num) 
    return words


def num2words_kr(num):
    under_10 = ['Нол','бир','икки','уч','тўрт','беш','олти','етти','саккиз','тўққиз'] 
    tens = ['ўн', 'йигирма', 'ўттиз', 'қирқ', 'эллик', 'олтмиш', 'етмиш', 'саксон', 'тўқсон'] 
    above_100 = {100: 'юз',1000:'минг', 1000000:'миллион', 1000000000:'миллиард'} 
    if num < 10: 
        return under_10[num]
    if num < 100: 
        return tens[(int)(num/10)-1] + ('' if num%10==0 else ' ' + under_10[num%10]) 
    pivot = max([key for key in above_100.keys() if key <= num]) 
    return num2words_kr((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words_kr(num%pivot)) 


def num2words_uz(num): 
	under_10 = ['nol','bir','ikki','uch','to`rt','besh','olti','yetti','sakkiz','to`qqiz',] 
	tens = ['o`n','yigirma','o`ttiz','qirq','ellik','oltmish','yetmish','sakson','to`qson'] 
	above_100 = {100: 'yuz',1000:'ming', 1000000:'million', 1000000000:'milliard'} 
	if num < 10: 
		return under_10[num]
	if num < 100: 
		return tens[(int)(num/10)-1] + ('' if num%10==0 else ' ' + under_10[num%10]) 
	pivot = max([key for key in above_100.keys() if key <= num]) 
	return num2words_uz((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words_uz(num%pivot)) 


def control(update: Update, context: CallbackContext):
    args = update.effective_message.text
    number, isnum = check_text(args)
    if flag == 'uz':
        if isnum:
            text = num2words_uz(number)
            update.message.reply_text(text)
        else:
            update.message.reply_text('Iltimos faqat son kiriting!')
    elif flag == 'uz_kr':
        if isnum:
            text = num2words_kr(number)
            update.message.reply_text(text)
        else:
            update.message.reply_text('Илтимос фақат сон киритинг!')
            return
    elif flag == 'ru':
        if isnum:
            text = num2words_ru(number)
            update.message.reply_text(text)
        else:
            update.message.reply_text('Пожалуйста, просто введите число')
            return
    elif flag == 'en':
        if isnum:
            text = num2words_en(number)
            update.message.reply_text(text)
        else:
            update.message.reply_text('Please just enter a number')
            return 
    else:
        update.message.reply_text(f'Iltimos {update.effective_user.first_name}, tilni tanlang!', reply_markup=main_menu_keyboard())



def about(update: Update, context: CallbackContext):
    update.message.reply_text('Bot test rejimida ishlamoqda. Ushbu xizmatni siz inline mode orqali ham ishlatishingiz mumkin. \nBot Diyorbek Abduqodirov tomonidan ishlab chiqildi.\nTakliflar uchun @diyor_adm')



       

def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if query.isnumeric():
        text = uz_text(query).capitalize()
        global text_flag
        text_flag=text
        update.inline_query.answer([
            InlineQueryResultArticle(
                id=text, description=f'Salom {update.effective_user.first_name}  \nMade with 🖤 by @diyoradm',
                title=f'✅ {text}', 
                input_message_content=InputTextMessageContent(text + '\nQuyidagi tugmalarni bosish orqali kerakli tilni tanlang\n@sonnimatngabot'),
                reply_markup=inline_menu_keyboard() )
            ])
    elif (len(query) == 0):
            text = 'Hech bo`lmasa bitta son yozing😁'
            print(text)
            update.inline_query.answer([
                InlineQueryResultArticle(
                    id='a', description=f'Salom {update.effective_user.first_name}  \nMade with 🖤 by @diyoradm',
                    title=f'⛔️ {text}',
                    input_message_content=InputTextMessageContent(text + '\n\n@sonnimatngabot'))
            ])
    else:
        text = '⛔️ Iltimos faqat son yozing'
        update.inline_query.answer([
                InlineQueryResultArticle(
                    id=text, description=f'Salom {update.effective_user.first_name}  \nMade with 🖤 by @diyoradm',
                    title=text,
                    input_message_content=InputTextMessageContent(text))
        ])

def xato_keyboard ():
    keyboard = [[InlineKeyboardButton('Ha', callback_data='trans_error'),
    InlineKeyboardButton('Yo`q', callback_data='trans_correct')]]        
    return InlineKeyboardMarkup(keyboard)

def inline_menu_keyboard():
  keyboard = [[InlineKeyboardButton('🇺🇿 Ўзбекча', callback_data='uz_kirill'), InlineKeyboardButton('🇷🇺 Русский', callback_data='russian'), InlineKeyboardButton('🇬🇧 English ', callback_data='english')]]        
  return InlineKeyboardMarkup(keyboard)

def uzbek_kirill(update: Update, context: CallbackContext):
    text = to_cyrillic(text_flag)
    update.callback_query.edit_message_text(text)

def english(update: Update, context: CallbackContext):
    text = num2words_en(text_flag)
    update.callback_query.edit_message_text(text)

def russian(update: Update, context: CallbackContext):
    text = num2words_ru(text_flag)
    update.callback_query.edit_message_text(text)

def select_lang(update: Update, context: CallbackContext):
    if flag == 'ru':
        update.message.reply_text(f'{update.effective_user.first_name} выбери нужный язык!', reply_markup=main_menu_keyboard())
    elif flag == 'uz_kr':
        update.message.reply_text(f'{update.effective_user.first_name} керакли тилни танланг!', reply_markup=main_menu_keyboard())
    elif flag == 'en':
        update.message.reply_text(f'{update.effective_user.first_name} choose the language you need!', reply_markup=main_menu_keyboard())
    else:
        update.message.reply_text(f'{update.effective_user.first_name} kerakli tilni tanlang!', reply_markup=main_menu_keyboard())

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', send_welcome))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('language', select_lang))
dispatcher.add_handler(CallbackQueryHandler(uzbek_latin, pattern='uz_latin'))
dispatcher.add_handler(CallbackQueryHandler(uzbek_kirill, pattern='uz_kirill'))
dispatcher.add_handler(CallbackQueryHandler(uzbek_kirill_key, pattern='uzbek_kirill_key'))
dispatcher.add_handler(CallbackQueryHandler(russian, pattern='russian'))
dispatcher.add_handler(CallbackQueryHandler(english, pattern='english'))
dispatcher.add_handler(CallbackQueryHandler(rus, pattern='rus'))
dispatcher.add_handler(CallbackQueryHandler(en_key, pattern='en_key'))

dispatcher.add_handler(InlineQueryHandler(inline_query))

dispatcher.add_handler(MessageHandler(Filters.all, control))





updater.start_polling()
updater.idle()


# def kirill(message): return translit(latin_text(message))
# all_text = f"O'zbekcha: {javob(message)}\nKirillcha: {kirill(message)}\n\n@diyoradm :)"