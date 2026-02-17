import main
from decorator import my_decorator
from main import cf

import time

@my_decorator()
def answer(mess):
    if mess.reply_to_message:
        if mess.reply_to_message.from_user.is_bot:
            original_chat_id = main.db.id_scanner(mess.reply_to_message.message_id)
            
            if original_chat_id == 0:
                flag = main.kycok.send_message(mess.chat.id, "❌не могу найти id отправителя")
                time.sleep(1)
                main.kycok.delete_message(mess.chat.id, flag.message_id)
            else:
                main.kycok.copy_message(
                    chat_id=original_chat_id,
                    from_chat_id=mess.chat.id,
                    message_id=mess.message_id)
                flag = main.kycok.send_message(mess.chat.id, "✅сообщение отправельно")
                time.sleep(1)
                main.kycok.delete_message(mess.chat.id, flag.message_id)
        
@my_decorator()    
def comment(mess):
    msg = main.kycok.forward_message(
        chat_id=cf["chat_fo_send_id"],
        from_chat_id=mess.chat.id,
        message_id=mess.message_id)
    
    main.db.set_msg(mess.from_user.id,msg.message_id)
    flag = main.kycok.send_message(mess.chat.id, "✅сообщение отправельно")
    time.sleep(1)
    main.kycok.delete_message(mess.chat.id, flag.message_id)

@main.kycok.message_handler(commands=["ban"])
@my_decorator(admin_onle=True,bun_protection=True)
def ban(mess):
    if mess.reply_to_message:
        if mess.reply_to_message.from_user.is_bot:
            user_id = main.db.id_scanner(mess.reply_to_message.message_id)
            if user_id == 0:
                ValueError("не могу найти айди пользователя")
            user = main.db.user_rep(user_id)
            
            if user == None:
                try:
                    user_info = main.kycok.get_chat(user_id)
                    main.db.set_user(user_info.id,user_info.first_name+user_info.last_name,False,True)
                except:
                    raise ValueError("не могу определить данные пользователя")          
            elif user[3]:
                main.db.upd_user(user_id,user[2],False)
                main.kycok.send_message(mess.chat.id,"✅пользователь теперь разбанен")
            else:      
                main.db.upd_user(user_id,user[2],True)
                main.kycok.send_message(mess.chat.id,"✅пользователь забанен")

    else:
        main.kycok.send_message(mess.chat.id,"а каво банить?\nответь на ,преслонное ботом, сообщение")