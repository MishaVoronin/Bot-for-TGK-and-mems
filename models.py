import sqlite3
from functools import wraps

class database:
    fael = ""

    def error(func):
        @wraps(func)  
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)  
                return result
            except Exception as e:
                error_text = f"""↳{func.__name__} \n{e}"""
                raise ValueError(error_text)
        return wrapper
    
    @error
    def __init__(self,fael):
        self.fael = fael
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()

        cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL
)
''')
        cursor.execute('''
CREATE TABLE IF NOT EXISTS Memes (
    id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL
)
''')
        cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    ban BOOLEAN NOT NULL DEFAULT FALSE
)
''')
        conn.commit()

        conn.close()

    
    @error
    def set_mem(self,chat_id, message_id):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM Memes")
        result = cursor.fetchone()[0]
        
        
        if result is None:
            id = 1
        else:
            id = result+1

        cursor.execute("INSERT INTO Memes (id, chat_id, message_id) VALUES (?, ?, ?)", (id, chat_id, message_id))
        
        new_id = cursor.lastrowid
        
        conn.commit()
        conn.close()        
        return new_id
    
    @error
    def pop_mem(self,delete_id):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()
        
        cursor.execute("SELECT chat_id, message_id FROM Memes WHERE id = ?", (delete_id,))
        deleted = cursor.fetchone()
        
        cursor.execute("DELETE FROM Memes WHERE id = ?", (delete_id,))
        cursor.execute("UPDATE Memes SET id = id - 1 WHERE id > ?", (delete_id,))
        
        conn.commit()
        conn.close()
        
        return deleted

    @error
    def set_user(self,user_id,name,admin,ban):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (id, name, admin, ban) VALUES (?, ?, ?, ?)", (user_id, name,admin,ban))
        
        conn.commit()
        conn.close()
        return

    @error
    def upd_user(self,user_id,admin,ban):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET ban = ?,admin = ?  WHERE id = ?", (ban,admin,user_id))
        
        conn.commit()
        conn.close()
        return
    

    
    @error
    def user_rep(self,user_id):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user
    
    @error
    def admins(self):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE admin = TRUE")
        ids = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return ids
    
    @error        
    def set_msg(self,chat_id,msg_id):
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO messages (message_id, chat_id) VALUES (?, ?)", (msg_id,chat_id))
        
        conn.commit()
        conn.close()
        return
    
    @error
    def id_scanner(self,msg_ig):
    
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()
        
        cursor.execute("SELECT chat_id FROM messages WHERE message_id = ?",(msg_ig,))
        chat_id = cursor.fetchone()
        if chat_id == [] or chat_id == None:
            return 0
        else:
            return chat_id[0]
    
    @error
    def mems_size(self):
        
        conn = sqlite3.connect(self.fael)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Memes")
        count = cursor.fetchone()[0]
        return count
