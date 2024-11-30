import pandas as pd
import json
import os
from datetime import datetime as dt

#Полезные константы
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
    'finance': []
}



#Анализ ввода пользователя
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

#############################
#Управление заметками

#Класс заметки
class Note:
    def __init__(self, id, title, content, timestamp=None):
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
    
#Конвертируем dict в заметку
def dict_to_note(data):
    return Note(id=data['id'], title=data['title'], content=data['content'], timestamp=data['timestamp'])

#Получаем заметки из хранилища
def get_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as file:
        return [dict_to_note(note) for note in json.load(file)]

#Сохраняем заметки в хранилище
def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump([note.to_dict() for note in notes], file)

#Смотрим все заметки
def view_notes():
    notes = get_notes()
    if len(notes) == 0:
        print('Заметки отсутствуют')
    else:
        print('Список всех заметок:')
        for note in notes:
            print(f'Заголовок: {note.title} (id: {note.id}, дата: {note.timestamp})')

#Просмотр определенной заметки
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

#Обновляем заметку
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

#Добавляем новую заметку
def add_note():
    notes = get_notes()
    id = get_free_id('notes')
    title = input('Введи заголовок: ')
    content = input('Введи содержание: ')
    new_note = Note(id = id, title=title, content=content)
    notes.append(new_note)
    save_notes(notes)
    print(f'Заметка "{title}" добавлена.')

#Удаляем заметку
def delete_note():
    notes = get_notes()
    try:
        id = int(input('Введите id заметки >> '))
        notes = [note for note in notes if note.id != id]
        save_notes(notes)
        print('Заметка удалена')
    except Exception as e:
        print(f'Ошибка: {e}')

#Экспорт заметок в csv
def export_notes_to_csv():
    try:
        pd.DataFrame([note.to_dict() for note in get_notes()]).to_csv(NOTES_EXPORT_FILE, index=False)
        print(f'Заметки экспортированы в {NOTES_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

#Импорт заметок из csv
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

#############################
#Управление задачами

#Класс задачи
class Task:
    def __init__(self, id, title, priority = 'Средний', due_date = None, description = '', done = False):
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

#Конвертируем dict в задачу
def dict_to_task(data):
    return Task(id=data['id'], title=data['title'], description=data['description'], done=data['done'], priority=data['priority'], due_date=data['due_date'])

#Получаем задачи из хранилища
def get_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return [dict_to_task(task) for task in json.load(file)]

#Сохраняем задачи
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file)

#Смотрим все задачи
def view_tasks():
    tasks = get_tasks()
    if len(tasks) == 0:
        print('Задачи отсутствуют')
    else:
        print('Список всех задач:')
        for task in tasks:
            print(f'Краткое описание: {task.title}; приоритет: {task.priority}; дедлайн: {task.due_date}; подробное описание: {task.description}; выполнено: {task.done}; id: {task.id}')

#Добавляем новую задачу
def add_task():
    tasks = get_tasks()
    id = get_free_id('tasks')
    title = input('Введите название задачи >> ')
    description = input('Введите описание задачи >> ')
    priority = input('Введите приоритет задачи («Высокий», «Средний», «Низкий») >> ')
    due_date = input('Введите срок выполнения задачи (ДД-ММ-ГГГГ) >> ')
    new_task = Task(id = id, title = title, description = description, priority = priority, due_date = due_date)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Задача "{title}" добавлена.')

#Отмечаем задачу
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

#Обновляем задачу
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
                task.priority = input('Введите новый приоритет задачи («Высокий», «Средний», «Низкий») >> ')
                task.due_date = input('Введите новый срок выполнения задачи (ДД-ММ-ГГГГ) >> ')
                print(f'Задача "{task.title}" изменена')
                save_tasks(tasks)
        except Exception as e:
            print(f'Ошибка: {e}')

#Удаляем задачу
def delete_task():
    tasks = get_tasks()
    try:
        id = int(input('Введите id задачи >> '))
        tasks = [task for task in tasks if task.id != id]
        save_tasks(tasks)
        print('Задача удалена')
    except Exception as e:
        print(f'Ошибка: {e}')

#Экспорт задач в csv
def export_tasks_to_csv():
    try:
        pd.DataFrame([task.to_dict() for task in get_tasks()]).to_csv(TASKS_EXPORT_FILE, index=False)
        print(f'Задачи экспортированы в {TASKS_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

#Импорт задач из csv
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

#############################
#Управление контантами

#Класс контакт
class Contact:
    def __init__(self, id, name, phone, email):
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

#Конвертируем dict в контакт
def dict_to_contact(data):
    return Contact(id=data['id'], name=data['name'], phone=data['phone'], email=data['email'])

#Получаем контакты из хранилища
def get_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, 'r') as file:
        return [dict_to_contact(contact) for contact in json.load(file)]

#Сохраняем контакты
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump([contact.to_dict() for contact in contacts], file)

#Добавляем новый контакт
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

#Смотрим все задачи
def view_contacts():
    contacts = get_contacts()
    if len(contacts) == 0:
        print('Контакты отсутствуют')
    else:
        print('Список всех контактов:')
        for contact in contacts:
            print(f'id: {contact.id}, имя: {contact.name}, номер: {contact.phone}, email: {contact.email}')


#Просмотр определенного контакта
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

#Обновляем контакт
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

#Удаляем контакт
def delete_contact():
    contacts = get_contacts()
    try:
        id = int(input('Введите id контакта >> '))
        contacts = [contact for contact in contacts if contact.id != id]
        save_tasks(contacts)
        print('Контакт удален')
    except Exception as e:
        print(f'Ошибка: {e}')

#Экспорт контактов в csv
def export_contacts_to_csv():
    try:
        pd.DataFrame([contact.to_dict() for contact in get_contacts()]).to_csv(CONTACTS_EXPORT_FILE, index=False)
        print(f'Контакты экспортированы в {CONTACTS_EXPORT_FILE}')
    except Exception as e:
        print(f'Ошибка: {e}')

#Импорт контактов из csv
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


#############################
#Управление фин. записями



#############################
#Калькулятор



#############################
#Main

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
                else:
                    print('В разработке')

        #Фин. записи
        elif com == 4:
            print('\nРаздел: Управление финансовыми записями')

        #Калькулятор
        elif com == 5:
            print('\nРаздел: Калькулятор')
        
        #Выход
        elif com == 6:
            print('\nЗавершение программы.')
            break

