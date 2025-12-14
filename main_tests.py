import sqlite3
import os

db_path = "data/database.db"

def apply_migrations():
    conn = sqlite3.connect(db_path)         # подключаем бд
    
    # чтобы таблицы могли быть взаимосвязаные 
    # FOREIGN KEY (users_id) REFERENCES users(id)
    conn.execute("PRAGMA foreign_keys=ON;")  
    migrations_path = "migrations"

    for file in sorted(os.listdir(migrations_path)):         
    # получем пути из os.listdir и сортируем их 
        if file.endswith(".sql"):            # ищем файлы с окончанием на .sql
            with open(os.path.join(migrations_path, file), "r", encoding="utf-8") as f:        
                # path - путь, join - передает путь до файла
                # (migrations_path, file) - объеденяет путь до папки и файла
                sql = f.read()

                conn.executescript(sql)
    
    conn.commit()
    conn.close()

apply_migrations()