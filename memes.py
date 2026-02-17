import main as main
from main import cf
from decorator import my_decorator

import time
from datetime import datetime, timedelta
from random import randint as rint
import threading


memesing_event = False
shitposting_event = False
taim_befor_next_mem = None


@my_decorator(return_error=True)
def new_mem(mess):
    global memesing_event
    if mess.text == 'stop':
        mem(mess)
    else:               
        main.db.set_mem(mess.chat.id,mess.message_id)

        msg = main.kycok.send_message(mess.chat.id,"мем добавлен")
        main.kycok.register_next_step_handler(msg, new_mem)
        time.sleep(1)
        main.kycok.delete_message(mess.chat.id, msg.message_id)

        
@my_decorator(return_error=True)
def post_mem(mess_to_adm = ""):

    count = main.db.mems_size()
    if count == 0:
        for a in main.db.admins():
            main.kycok.send_message(a,"У НАС НЕТ МЕМОВ")
    else:
        mem = main.db.pop_mem(rint(1,count))
        try:
            main.kycok.copy_message(
                chat_id=cf["tgk"],
                from_chat_id=mem[0],
                message_id=mem[1]
            )
        except:
            for a in main.db.admins():
                main.kycok.send_message(a,"мем не найден"+mess_to_adm)

        for a in main.db.admins():
            main.kycok.send_message(a,"мем отправлен"+mess_to_adm)


@my_decorator(return_error=True)
def shitpost():
    try:
        global taim_befor_next_mem, shitposting_event
        taim_befor_next_mem = datetime.now()
        while shitposting_event:
            naw = datetime.now()
            if taim_befor_next_mem <= naw:
                taim_befor_next_mem += timedelta(
                minutes=rint(cf["time_between_memes"][0], cf["time_between_memes"][1]))
                post_mem(mess_to_adm=f"""\n следующий мем в {taim_befor_next_mem.strftime("%H:%M")}""")
            time.sleep(15)

        taim_befor_next_mem = None
        
        for a in main.db.admins():
            main.kycok.send_message(a, "шитпост остановлен")
    except Exception as e:
        taim_befor_next_mem = None
        shitposting_event = False
        try:
            for a in main.db.admins():
                main.kycok.send_message(a, "шитпост остановлен")
        except:
            ...
        raise ValueError(e)
    
@my_decorator()
def SPonoff(mess):
    global shitposting_event
    if shitposting_event:
        shitposting_event = False
        main.kycok.send_message(mess.chat.id, "щитпост выключается")
    else:
        shitposting_event = True
        thread = threading.Thread(target=shitpost, daemon=True)
        thread.start()
        main.kycok.send_message(mess.chat.id, "щитпост включен")


@my_decorator(return_error=True)
def mem(mess):
    global memesing_event
    if memesing_event:
        memesing_event=False
        main.kycok.send_message(mess.chat.id, "всё ок")
    else:
        memesing_event=True
        main.kycok.send_message(mess.chat.id, "отправь свои мемы, когда закончеш напиши stop")

def report(mess):
    count = main.db.mems_size()
    report = ""
    report += "Отчёт:\n"
    if shitposting_event:
        report +="Шитпост включен\n"
        if count == 0:
            report +="МЕМОВ НЕТ\n"
        else:
            report +=f"""у нас {count} мемов\n"""
            if not taim_befor_next_mem is  None:
                ttnm = taim_befor_next_mem - datetime.now()
                total_seconds = ttnm.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                report += f"следующий мем в {taim_befor_next_mem.strftime('%H:%M')}\nЧерез {hours:02d}:{minutes:02d}\n"
            else:
                report += "следующий мем: время не задано\n"    
    else:
        report +="Шитпост выключен\n"
        if count == 0 or count == None:
            report +="МЕМОВ НЕТ\n"
        else:
            report +=f"""у нас {count} мемов\n"""
    main.kycok.send_message(mess.chat.id,report)