#свои файлы

if __name__ == "__main__":        
    
    import Pitch
    import memes
    from decorator import my_decorator
from models import database 

#библиотеки
import telebot
import time
import json


#==================ПЕРЕМЕННЫЕ=============================
with open('config.json', 'r', encoding='utf-8') as f:
    cf = json.load(f)

kycok = telebot.TeleBot(cf["token"],threaded=False, skip_pending=True)

db = database("database.db")
HTTPSerrors = 0

#==================КОМАНДЫ_БОТА===========================
if __name__ == "__main__":
    @kycok.message_handler(commands=["start"])
    @my_decorator(bun_protection=True)
    def start(mess):
        if mess.from_user.id in db.admins():
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('/mem', '/SPonoff', '/report', '/post','/ban','/abort')
            kycok.send_message(mess.chat.id,"Здравствуйте, многоуважаемый админ вот ваши команды",reply_markup=markup)
        else:
            kycok.send_message(mess.chat.id, "Привет! Это самописный бот предложки для канала Кусок Домкрата просто напиши сюда любой мем а я перешлю его админам")
            print(f"Новый пользователь: {mess.from_user.first_name} {mess.from_user.last_name} @{mess.from_user.username} {mess.chat.id}")

    @kycok.message_handler(commands=["mem"])
    @my_decorator(admin_onle=True,bun_protection=True)
    def mems(mess):
        memes.mem(mess)

    @kycok.message_handler(commands=["SPonoff"])
    @my_decorator(admin_onle=True, bun_protection=True)
    def SPonoff(mess):
        memes.SPonoff(mess)

    @kycok.message_handler(commands=["post"])
    @my_decorator(admin_onle=True,bun_protection=True)
    def post(mess):
        memes.post_mem()
        
    @kycok.message_handler(commands=["ban"])
    @my_decorator(admin_onle=True,bun_protection=True)
    def ban(mess):
        Pitch.ban(mess)

    @kycok.message_handler(commands=["report"])
    @my_decorator(admin_onle=True,bun_protection=True)
    def report(mess):
        memes.report(mess)

    #@kycok.message_handler(commands=["abort"])
    @my_decorator(admin_onle=True,bun_protection=True)
    def abort(mess):
        kycok.stop_polling()
        kycok.reply_to(mess,"✅Бот остановлен")

    @kycok.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker', 'animation', 'voice', 'video_note', 'audio'])
    @my_decorator(bun_protection=True)
    def pitch(mess):
        if memes.memesing_event:
            if mess.from_user.id in db.admins():
                memes.new_mem(mess)
                return
        if mess.chat.id == cf["chat_fo_send_id"]:
            Pitch.answer(mess)   
        else:
            Pitch.comment(mess)


    #==================ЗАПУСК_БОТА=====================


    @my_decorator(return_error=True)
    def run_bot():
        global HTTPSerrors
        try:
            kycok.polling(none_stop=True, timeout=120, long_polling_timeout=120)
        except Exception as e:
            try:
                for adm in db.admins():
                    kycok.send_message(adm,e)
            except:
                pass
            print(f"\033[91m[ERROR]{e}\033[0m")
            time.sleep(5)
            HTTPSerrors += 1
            if HTTPSerrors <= 3:
                run_bot()

    def main():

        run_bot()    

if __name__ == "__main__":
    main()
