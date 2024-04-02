import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect("main.db")
    cur = base.cursor()
    if base:
        print('База данных подключена')
    base.execute('CREATE TABLE IF NOT EXISTS user(login)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS intime(time)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS outtime(time)')
    base.commit()


