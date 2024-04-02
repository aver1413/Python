import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect("main.db")
    cur = base.cursor()
    if base:
        print('База данных подключена')
    base.execute('CREATE TABLE IF NOT EXISTS stager(login)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS ID(ID PRIMARY KEY, USERNAME, FIRSTNAME, LASTNAME)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS spec(ID PRIMARY KEY, USERNAME, FIRSTNAME, LASTNAME)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS trener(ID PRIMARY KEY, USERNAME, FIRSTNAME, LASTNAME)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS helper(ID PRIMARY KEY, USERNAME, FIRSTNAME, LASTNAME)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS admin(ID PRIMARY KEY, USERNAME, FIRSTNAME, LASTNAME)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS news(NEWS)')
    base.commit()


