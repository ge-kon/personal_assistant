import pandas as pd
import json
import os
from datetime import datetime as dt


NOTES_FILE = 'notes.json'
NOTES_EXPORT_FILE = 'notes_export.csv'
TASKS_FILE = 'tasks.json'
TASKS_EXPORT_FILE = 'tasks_export.csv'
CONTACTS_FILE = 'contacts.json'
CONTACTS_EXPORT_FILE = 'contacts_export.csv'
FINANCE_FILE = 'finance.json'
FINANCE_EXPORT_FILE = 'finance_export.csv'
MENU = {
    'main': ['1. Управление заметками', '2. Управление задачами', '3. Управление контактами', 
             '4. Управление финансовыми записями', '5. Калькулятор', '6. Выход'],
    'notes': ['1. Создание новой заметки', '2. Просмотр списка заметок', '3. Просмотр подробностей заметки', '4. Редактирование заметки', 
              '5. Удаление заметки', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню'],
    'tasks': ['1. Добавление новой задачи', '2. Просмотр списка задач', '3. Отметка задачи как выполненной', '4. Редактирование задачи', 
              '5. Удаление задачи', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню'],
    'contacts': ['1. Добавление нового контакта', '2. Просмотр списка контактов', '3. Поиск контакта (по имени или телефону)', '4. Редактирование контакта', 
                 '5. Удаление контакта', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню'],
    'finance': ['1. Добавление новой финансовой записи (доход или расход)', '2. Просмотр всех записей с возможностью фильтрации по дате или категории', 
                '3. Генерация отчёта о финансовой активности за определённый период', '4. Удалить запись', '5. Импорт записей в формате csv', '6. Экспорт записей в формате csv', '7. Выход в главное меню'],
    'calculate': ['1. Ввод выражения', '2. Выход в главное меню']
}

def interaction(sections):
    print('\nВыберите действие:')
    for i in sections:
        print(i)

    while True:
        try:
            c = int(input('>> '))
            if 1 <= c <= len(sections):
                return c
            else:
                raise ValueError    
        except Exception as e:
            print(f'Ошибка: {e}')

def get_free_id(section):
    ids = []
    filename = ''
    if section == 'notes':
        filename = NOTES_FILE
    elif section == 'tasks':
         filename = TASKS_FILE
    elif section == 'contacts':
        filename = CONTACTS_FILE
    elif section == 'finance':
        filename = FINANCE_FILE

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            ids = [unit['id'] for unit in json.load(file)]
    return max(ids) + 1 if len(ids) > 0 else 1

def validate_date(date):
    try:
        dt.strptime(date, '%d-%m-%Y')
        return True 
    except:
        return False  


class Note:
    def __init__(self, id: int, title: str, content: str, timestamp: str = None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp if timestamp != None else dt.now().strftime('%d-%m-%Y %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

def dict_to_note(data):
    return Note(id=data['id'], title=data['title'], content=data['content'], timestamp=data['timestamp'])

def get_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as file:
        return [dict_to_note(note) for note in json.load(file)]

def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump([note.to_dict() for note in notes], file)

def view_notes():
    notes = get_notes()
    if len(notes) == 0:
        print('Заметки отсутствуют')
    else:
        print('Список всех заметок:')
        for note in notes:
            print(f'Заголовок: {note.title} (id: {note.id}, дата: {note.timestamp})')

def view_note():
    notes = get_notes()
    if len(notes) == 0:
        print('Заметки отсутствуют')
    else:
        try:
            id = int(input('Введите id заметки >> '))
            if id not in [note.id for note in notes]:
                print('Заметка не найдена')
            else:
                for note in notes:
                    if note.id == id:
                        print(f'Заголовок: {note.title}\nСодержание: {note.content}\nДата: {note.timestamp}')
                        break
        except Exception as e:
            print(f'Ошибка: {e}')

def update_note():
    notes = get_notes()
    if len(notes) == 0:
        print('Заметки отсутствуют')
    else:
        try:
            id = int(input('Введите id заметки >> '))
            note = next(filter(lambda x: x.id == id, notes), None)
            if note == None:
                print('Заметка не найдена')
            else:
                tmp_title = input('Введи новый заголовок >> ')
                tmp_content = input('Введи новое содержание >> ')
                note.title = tmp_title
                note.content = tmp_content
                note.timestamp = dt.now().strftime('%d-%m-%Y %H:%M:%S')
                save_notes(notes)
        except Exception as e:
            print(f'Ошибка: {e}')

def add_note():
    notes = get_notes()
    id = get_free_id('notes')
    title = input('Введи заголовок: ')
    content = input('Введи содержание: ')
    new_note = Note(id = id, title=title, content=content)
    notes.append(new_note)
    save_notes(notes)
    print(f'Заметка "{title}" добавлена.')

def delete_note():
    notes = get_notes()
    try:
        id = int(input('Введите id заметки >> '))
        notes = [note for note in notes if note.id != id]
        save_notes(notes)
        print('Заметка удалена')
    except Exception as e:
        print(f'Ошибка: {e}')

def export_notes_to_csv():
    try:
        pd.DataFrame([note.to_dict() for note in get_notes()]).to_csv(NOTES_EXPORT_FILE, index=False)
        print(f'Заметки экспортированы в {NOTES_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

def import_notes_from_csv():
    filename = input('Введите название файла (с расширением) для импорта заметок >> ')
    try:
        df = pd.read_csv(filename)
        notes = get_notes()
        for index, row in df.iterrows():
            note = Note(id=int(row['id']), title=row['title'], content=row['content'], timestamp=row['timestamp'])
            if note.id in [n.id for n in notes]:
                note.id = get_free_id('notes')
            notes.append(note)
            save_notes(notes)
        print(f'Заметки импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


class Task:
    def __init__(self, id: int, title: str, priority: str = 'Средний', due_date: str = None, description: str = '', done: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

def dict_to_task(data):
    return Task(id=data['id'], title=data['title'], description=data['description'], done=data['done'], priority=data['priority'], due_date=data['due_date'])

def get_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return [dict_to_task(task) for task in json.load(file)]

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file)

def view_tasks():
    tasks = get_tasks()
    if len(tasks) == 0:
        print('Задачи отсутствуют')
    else:
        print('Список всех задач:')
        for task in tasks:
            print(f'Краткое описание: {task.title}; приоритет: {task.priority}; дедлайн: {task.due_date}; подробное описание: {task.description}; выполнено: {task.done}; id: {task.id}')

def add_task():
    tasks = get_tasks()
    id = get_free_id('tasks')
    title = input('Введите название задачи >> ')
    description = input('Введите описание задачи >> ')
    priority = ''
    while True:
        priority = input('Введите новый приоритет задачи (Высокий/Средний/Низкий) >> ')
        if priority in ['Высокий', 'Средний', 'Низкий']:
            break
        else:
             print('Приоритет некорректен. Выберите из набора (Высокий/Средний/Низкий)')
    due_date = ''
    while True:
        due_date = input('Введите новый срок выполнения задачи (ДД-ММ-ГГГГ) >> ')
        if validate_date(due_date):
            break
        else:
            print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
    new_task = Task(id = id, title = title, description = description, priority = priority, due_date = due_date)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Задача "{title}" добавлена.')

def do_task():
    tasks = get_tasks()
    if len(tasks) == 0:
        print('Задачи отсутствуют')
    else:
        try:
            id = int(input('Введите id задачи >> '))
            task = next(filter(lambda x: x.id == id, tasks), None)
            if task == None:
                print('Задача не найдена')
            else:
                task.done = True
                print(f'Задача "{task.title}" отмечена выполненной')
                save_tasks(tasks)
        except Exception as e:
            print(f'Ошибка: {e}')

def update_task():
    tasks = get_tasks()
    if len(tasks) == 0:
        print('Задачи отсутствуют')
    else:
        try:
            id = int(input('Введите id задачи >> '))
            task = next(filter(lambda x: x.id == id, tasks), None)
            if task == None:
                print('Задача не найдена')
            else:
                task.title = input('Введите новое название задачи >> ')
                task.description = input('Введите новое описание задачи >> ')
                priority = ''
                while True:
                    priority = input('Введите новый приоритет задачи (Высокий/Средний/Низкий) >> ')
                    if priority in ['Высокий', 'Средний', 'Низкий']:
                        break
                    else:
                        print('Приоритет некорректен. Выберите из набора (Высокий/Средний/Низкий)')
                task.priority = priority
                due_date = ''
                while True:
                    due_date = input('Введите новый срок выполнения задачи (ДД-ММ-ГГГГ) >> ')
                    if validate_date(due_date):
                        break
                    else:
                        print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
                task.due_date = due_date
                print(f'Задача "{task.title}" изменена')
                save_tasks(tasks)
        except Exception as e:
            print(f'Ошибка: {e}')

def delete_task():
    tasks = get_tasks()
    try:
        id = int(input('Введите id задачи >> '))
        tasks = [task for task in tasks if task.id != id]
        save_tasks(tasks)
        print('Задача удалена')
    except Exception as e:
        print(f'Ошибка: {e}')

def export_tasks_to_csv():
    try:
        pd.DataFrame([task.to_dict() for task in get_tasks()]).to_csv(TASKS_EXPORT_FILE, index=False)
        print(f'Задачи экспортированы в {TASKS_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

def import_tasks_from_csv():
    filename = input('Введите название файла (с расширением) для импорта задач >> ')
    try:
        df = pd.read_csv(filename)
        tasks = get_tasks()
        for index, row in df.iterrows():
            task = Task(id=int(row['id']), title=row['title'], description=row['description'], done=row['done'], priority=row['priority'], due_date=row['due_date'])
            if task.id in [t.id for t in tasks]:
                task.id = get_free_id('tasks')
            tasks.append(task)
            save_tasks(tasks)
        print(f'Задачи импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


class Contact:
    def __init__(self, id: int, name: str, phone: str, email: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

def dict_to_contact(data):
    return Contact(id=data['id'], name=data['name'], phone=data['phone'], email=data['email'])

def get_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, 'r') as file:
        return [dict_to_contact(contact) for contact in json.load(file)]

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump([contact.to_dict() for contact in contacts], file)

def add_contact():
    contacts = get_contacts()
    id = get_free_id('contacts')
    name = input('Введите имя контакта >> ')
    phone = input('Введите номер телефона контакта >> ')
    email = input('Введите email контакта >> ')
    new_contact = Contact(id = id, name = name, phone = phone, email = email)
    contacts.append(new_contact)
    save_contacts(contacts)
    print(f'Контакт "{name}" добавлен.')

def view_contacts():
    contacts = get_contacts()
    if len(contacts) == 0:
        print('Контакты отсутствуют')
    else:
        print('Список всех контактов:')
        for contact in contacts:
            print(f'id: {contact.id}, имя: {contact.name}, номер: {contact.phone}, email: {contact.email}')

def view_contact():
    contacts = get_contacts()
    if len(contacts) == 0:
        print('Контакты отсутствуют')
    else:
        com = input('Искать контакт по имени или по номеру (имя/номер) >> ')
        while True:
            try:
                if com == 'имя':
                    name = input('Введите имя контакта >> ')
                    contacts = [contact for contact in contacts if contact.name == name]
                elif com == 'номер':
                    phone = input('Введите номер контакта >> ')
                    contacts = [contact for contact in contacts if contact.phone == phone]          
                else:
                    raise ValueError  
                
                if len(contacts) == 0:
                        print('Контакты не найдены')
                        return
                else:
                    for contact in contacts:
                        print(f'id: {contact.id}, имя: {contact.name}, номер: {contact.phone}, email: {contact.email}')
                    return  
                
            except Exception as e:
                print(f'Ошибка: {e}')
                return

def update_contact():
    contacts = get_contacts()
    if len(contacts) == 0:
        print('Контакты отсутствуют')
    else:
        try:
            id = int(input('Введите id контакта >> '))
            contact = next(filter(lambda x: x.id == id, contacts), None)
            if contact == None:
                print('Контакт не найден')
            else:
                tmp_name = input('Введи новое имя >> ')
                tmp_phone = input('Введи новый номер >> ')
                tmp_email = input('Введи новый email >> ')
                contact.name = tmp_name
                contact.phone = tmp_phone
                contact.email = tmp_email
                save_contacts(contacts)
        except Exception as e:
            print(f'Ошибка: {e}')

def delete_contact():
    contacts = get_contacts()
    try:
        id = int(input('Введите id контакта >> '))
        contacts = [contact for contact in contacts if contact.id != id]
        save_tasks(contacts)
        print('Контакт удален')
    except Exception as e:
        print(f'Ошибка: {e}')

def export_contacts_to_csv():
    try:
        pd.DataFrame([contact.to_dict() for contact in get_contacts()]).to_csv(CONTACTS_EXPORT_FILE, index=False)
        print(f'Контакты экспортированы в {CONTACTS_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

def import_contacts_from_csv():
    filename = input('Введите название файла (с расширением) для импорта контактов >> ')
    try:
        df = pd.read_csv(filename)
        contacts = get_contacts()
        for index, row in df.iterrows():
            contact = Contact(id=int(row['id']), name=row['name'], phone=row['phone'], email=row['email'])
            if contact.id in [t.id for t in contact]:
                contact.id = get_free_id('contacts')
            contacts.append(contact)
            save_contacts(contacts)
        print(f'Контакты импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


class FinanceRecord:
    def __init__(self, id: int, amount: float, category: str, description: str, date: str = None):
        self.id = id
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }

def dict_to_finance_record(data):
    return FinanceRecord(id=data['id'], amount=data['amount'], description=data['description'], category=data['category'], date=data['date'])

def get_finance_records():
    if not os.path.exists(FINANCE_FILE):
        return []
    with open(FINANCE_FILE, 'r') as file:
        return [dict_to_finance_record(finance_record) for finance_record in json.load(file)]

def save_finance_records(finance_records):
    with open(FINANCE_FILE, 'w') as file:
        json.dump([finance_record.to_dict() for finance_record in finance_records], file)

def add_finance_record():
    finance_records = get_finance_records()
    id = get_free_id('finance')
    neg = False

    while True:
            com = input('Введите тип операции (доход/расход) >> ')
            try:
                if com == 'доход':
                    neg = True
                    break
                elif com == 'расход':
                    neg = False  
                    break      
                else:
                    raise ValueError                
            except Exception as e:
                print(f'Ошибка: {e}')
    
    amount = float(input('Введите размер операции >> '))
    if neg:
        amount *= -1
    category = input('Введите тип категории >> ')
    description = input('Введите описание операции >> ')
    date = ''
    while True:
        date = input('Введите срок совершения операции (ДД-ММ-ГГГГ) >> ')
        if validate_date(date):
            break
        else:
            print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
    new_record = FinanceRecord(id = id, amount = amount, description = description, category = category, date = date)
    finance_records.append(new_record)
    save_finance_records(finance_records)
    print(f'Операция добавлена.')

def view_finance_records():
    finance_records = get_finance_records()
    if len(finance_records) == 0:
        print('Записи отсутствуют')
    else:
        while True:
            com = input('Введите по чему фильтровать записи (дата/категория/ничего) >> ')
            try:
                if com == 'дата':
                    inp = ''
                    while True:
                        inp = input('Введите дату (ДД-ММ-ГГГГ) >> ')
                        if validate_date(inp):
                            break
                        else:
                            print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
                    finance_records = [finance_record for finance_record in finance_records if finance_record.date == inp]
                    break
                elif com == 'категория':
                    inp = input('Введите категорию >> ')
                    finance_records = [finance_record for finance_record in finance_records if finance_record.category == inp]
                    break  
                elif com == 'ничего':
                    break      
                else:
                    raise ValueError                
            except Exception as e:
                print(f'Ошибка: {e}')
        print('Список записей:')
        for finance_record in finance_records:
            print(f'id: {finance_record.id}; размер: {finance_record.amount}; дата: {finance_record.date}; категория: {finance_record.category}; описание: {finance_record.description}')

def get_finance_analysis():
    l, r = '', ''
    while True:
        l = input('Введите начальную дату (ДД-ММ-ГГГГ) >> ')
        if validate_date(l):
            break
        else:
            print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
    while True:
        r = input('Введите конечную дату (ДД-ММ-ГГГГ) >> ')
        if validate_date(r):
            break
        else:
            print('Дата некорректна. Введите в формате ДД-ММ-ГГГГ')
    finance_records = get_finance_records()
    if len(finance_records) == 0:
        print('Записи отсутствуют')
    else:
        print(f'Финансовый отчёт за период с {l} по {r}:')
        date1 = dt.strptime(l, "%d-%m-%Y")
        date2 = dt.strptime(r, "%d-%m-%Y")
        finance_records = [finance_record for finance_record in finance_records if date1 <= dt.strptime(finance_record.date, "%d-%m-%Y") <= date2]
        income = sum([finance_record.amount for finance_record in finance_records if finance_record.amount > 0])
        outcome = sum([finance_record.amount for finance_record in finance_records if finance_record.amount < 0])
        print(f"Доход: {income}")
        print(f"Расход: {outcome}")
        print(f"Остаток: {income-outcome}")
        try:
            pd.DataFrame([finance_record.to_dict() for finance_record in finance_records]).to_csv(f'finance_report_{l}_{r}.csv', index=False)
            print(f'Подробная информация сохранена в файле finance_report_{l}_{r}.csv')
        except Exception as e:
            print(f'Ошибка при экспорте: {e}')    

def delete_finance_record():
    finance_records = get_finance_records()
    try:
        id = int(input('Введите id записи >> '))
        finance_records = [finance_record for finance_record in finance_records if finance_record.id != id]
        save_finance_records(finance_records)
        print('Запись удалена')
    except Exception as e:
        print(f'Ошибка: {e}')

def export_finance_records_to_csv():
    try:
        pd.DataFrame([finance_record.to_dict() for finance_record in get_finance_records()]).to_csv(FINANCE_EXPORT_FILE, index=False)
        print(f'Финансовые записи экспортированы в {FINANCE_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

def import_finance_records_from_csv():
    filename = input('Введите название файла (с расширением) для импорта финансовых записей >> ')
    try:
        df = pd.read_csv(filename)
        finance_records = get_finance_records()
        for index, row in df.iterrows():
            finance_record = FinanceRecord(id = int(row['id']), amount = row['amount'], description = row['description'], category = row['category'], date = row['date'])
            if finance_record.id in [r.id for r in finance_records]:
                finance_record.id = get_free_id('finance')
            finance_records.append(finance_record)
            save_finance_records(finance_records)
        print(f'Финансовые записи импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


def calculate():
    while True:
        s = input('Введите выражение (дробные числа через вводите точку) >> ')
        try:
            check = lambda x: True if x in '0123456789+-/*(). ' else False
            if all([check(c) for c in s]):
                res = eval(s)
                print(f'Результат: {res}')
                break
            else:
                raise SyntaxError('Введены неверные символы. Разрешены символы из данного набора: 0123456789+-/*().')
        except Exception as e:
            print(f'Ошибка: {e}. Пожалуйста, введите корректный пример')
    

if __name__ == '__main__':
    print('Добро пожаловать в Персональный помощник!')

    while True:
        com = interaction(MENU['main'])
        
        #Заметки
        if com == 1:
            print('\nРаздел: Управление заметками')
            while True:
                com = interaction(MENU['notes'])
                if com == 1:
                    add_note()
                elif com == 2:
                    view_notes()
                elif com == 3:
                    view_note()
                elif com == 4:
                    update_note()
                elif com == 5:
                    delete_note()
                elif com == 6:
                    import_notes_from_csv()
                elif com == 7:
                    export_notes_to_csv()
                elif com == 8:
                    break

        #Задачи
        elif com == 2:
            print('\nРаздел: Управление задачами')
            while True:
                com = interaction(MENU['tasks'])
                if com == 1:
                    add_task()
                elif com == 2:
                    view_tasks()
                elif com == 3:
                    do_task()
                elif com == 4:
                    update_task()
                elif com == 5:
                    delete_task()
                elif com == 6:
                    import_tasks_from_csv()
                elif com == 7:
                    export_tasks_to_csv()
                elif com == 8:
                    break

        #Контакты
        elif com == 3:
            print('\nРаздел: Управление контактами')
            while True:
                com = interaction(MENU['contacts'])
                if com == 1:
                    add_contact()
                elif com == 2:
                    view_contacts()
                elif com == 3:
                    view_contact()
                elif com == 4:
                    update_contact()
                elif com == 5:
                    delete_contact()
                elif com == 6:
                    import_contacts_from_csv()
                elif com == 7:
                    export_contacts_to_csv()
                elif com == 8:
                    break

        #Фин. записи
        elif com == 4:
            print('\nРаздел: Управление финансовыми записями')
            while True:
                com = interaction(MENU['finance'])
                if com == 1:
                    add_finance_record()
                elif com == 2:
                    view_finance_records()
                elif com == 3:
                    get_finance_analysis()
                elif com == 4:
                    delete_finance_record()
                elif com == 5:
                    import_finance_records_from_csv()
                elif com == 6:
                    export_finance_records_to_csv()
                elif com == 7:
                    break

        #Калькулятор
        elif com == 5:
            print('\nРаздел: Калькулятор')
            while True:
                com = interaction(MENU['calculate'])
                if com == 1:
                    calculate()
                elif com == 2:
                    break

        #Выход
        elif com == 6:
            print('\nЗавершение программы.')
            break