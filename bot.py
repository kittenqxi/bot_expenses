import sqlite3
ui=1
conn=sqlite3.connect('expenses.db')
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
amount REAL,
category TEXT,
date TEXT,
comment TEXT
)
''')
conn.commit()
conn.close()
def check_input(a):
    if (a.replace('.', '', 1).isdigit() and a.count('.')<=1) and (float(a)*100)%1==0 and float(a)>0:
        return float(a)
    return False
def check_index(b, user):
    if b.isdigit() and int(b) > 0:
        conn=sqlite3.connect('expenses.db')
        c=conn.cursor()
        c.execute('SELECT id FROM expenses WHERE id=? AND user=?', (int(b), user))
        row=c.fetchone()
        conn.close()
        if row is not None:
            return int(b)
    return False
def check_date(d):
    parts=d.split('.')
    if len(parts)==3:
        day, month, year=parts
        if len(day)==2 and len(month)==2 and len(year)==4:
            if day.isdigit() and month.isdigit() and year.isdigit():
                if 1<=int(day)<=31 and 1<=int(month)<=12 and int(year)>0:
                    return d
    return False
def add_expense(user, value, category, date_str, text_comment):
    if category=='':
        category='No category'
    if text_comment=='':
        text_comment='No comment'
    conn=sqlite3.connect('expenses.db')
    c=conn.cursor()
    c.execute('INSERT INTO expenses (user, amount, category, date, comment) VALUES (?, ?, ?, ?, ?)', (user, value, category, date_str, text_comment),)
    conn.commit()
    conn.close()
    print('Expense added')
def show_expenses(user):
    conn=sqlite3.connect('expenses.db')
    c=conn.cursor()
    c.execute('SELECT id, amount, category, comment, date FROM expenses WHERE user=?', (user,),)
    row=c.fetchall()
    conn.close()
    return row
def get_count(user):
    conn=sqlite3.connect('expenses.db')
    c=conn.cursor()
    c.execute('SELECT amount FROM expenses WHERE user=?', (user,))
    row=c.fetchall()
    conn.close()
    return len(row)
def start(user):
    while True:
        print('5 - add new expenses')
        print('7 - show all expenses')
        print('12 - count expenses')
        print('0 - exit')
        print()
        choise=input('Select an option: ')
        if choise=='5':
            while True:
                value_raw=input('Enter new expense: ')
                value=check_input(value_raw)
                if value is not False:
                    category=input('Enter category: ')
                    while True:
                        date_raw=input('Enter date: ')
                        date_str=check_date(date_raw)
                        if date_str is not False:
                            break
                        print('Input error, enter in this form: dd.mm.yyyy')
                    text_comment=input('Enter comment: ')
                    add_expense(user, value, category, date_str, text_comment)
                    break
                print('Input error, enter another number')
        elif choise=='7':
            row=show_expenses(user)
            if not row:
                print('List is empty')
            else:
                for exp_id, amount, category, comment, date in row:
                    print(f'ID: {exp_id} / Amount: {amount} / Category: {category} / Comment: {comment} / Date: {date}')
        elif choise=='12':
            print('Count:', get_count(user))
        elif choise=='0':
            print('Bye bye')
            break
        else:
            print("We don't have this choise, try again")
start(ui)