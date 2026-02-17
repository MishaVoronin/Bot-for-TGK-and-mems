from main import kycok, db
from functools import wraps
from datetime import datetime



def my_decorator(admin_onle = False, bun_protection = False,return_error = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if bun_protection:

                    if len(args) > 0 and hasattr(args[0], 'from_user'):
                        mess = args[0]

                        rep = db.user_rep(mess.from_user.id)
                        if rep == None:
                            user_name = (mess.from_user.first_name  if mess.from_user.first_name else "") + (mess.from_user.last_name  if mess.from_user.last_name else "")
                            db.set_user(mess.from_user.id,user_name,False,False)
                            print(f"""пользователь создан {user_name}""")
                            for adm in db.admins():
                                kycok.send_message(adm,f"""пользователь создан {user_name}""")
                        else:
                            if rep[3]:
                                kycok.send_message(mess.chat.id,"✋🕵️‍♂️ Вы были забанены")
                                return
                    else:
                        raise ValueError("не могу найти mess") 
                
                if admin_onle:
                    if len(args) > 0 and hasattr(args[0], 'from_user'):
                        mess = args[0]
                        
                        if not mess.from_user.id in db.admins():
                            kycok.send_message(mess.chat.id,"no no no ms fish эта функция тоько для админов")
                            return
                    else:
                        raise ValueError("не могу найти mess")
            except Exception as e:
                if return_error:
                    error_text = f"""↳ошибка в декораторе в {func.__name__}\n  {e} """
                    raise ValueError(error_text)
                else:
                    error_text = f"""ошибка в декораторе в {func.__name__}\nошибка:\n{e} """
                    print(error_text)
                    for adm in db.admins():
                        kycok.send_message(adm,error_text)
                    return
            try:

                print(f"{datetime.now().strftime("%H:%M")}:{func.__name__}() {args[0].from_user.first_name if len(args) > 0 and hasattr(args[0], 'from_user') else ""}")                       
                func(*args, **kwargs)  
            
            except Exception as e:
                
                if return_error:
                    error_text = f"""↳{func.__name__}\n {e} """
                    raise ValueError(error_text)
                else:
                    error_text = f"""[ERROR]:{func.__name__}\n{e}"""
                    print(f"\033[91m{error_text}\033[0m")
                    for adm in db.admins():
                        kycok.send_message(adm,error_text)
                    return 
        return wrapper
    return decorator


