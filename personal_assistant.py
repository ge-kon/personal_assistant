import pandas as pd
import json
import os
from datetime import datetime as dt

#Полезные константы
NOTES_FILE = 'notes.json'
NOTES_EXPORT_FILE = 'notes_export.csv'
TASKS_FILE = 'tasks.json'
TASKS_EXPORT_FILE = 'tasks_export.csv'
MENU = {
    'main': ['1. Управление заметками', '2. Управление задачами', '3. Управление контактами', 
             '4. Управление финансовыми записями', '5. Калькулятор', '6. Выход'],
    'notes': ['1. Создание новой заметки', '2. Просмотр списка заметок', '3. Просмотр подробностей заметки', '4. Редактирование заметки', 
              '5. Удаление заметки', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню'],
    'tasks': ['1. Добавление новой задачи', '2. Просмотр списка задач', '3. Отметка задачи как выполненной', '4. Редактирование задачи', 
              '5. Удаление задачи', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню']
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

#Выбираем свободный id
def get_free_note_id():
    notes = get_notes()
    ids = [note.id for note in notes]
    return max(ids) + 1 if len(notes) > 0 else 1

#Добавляем новую заметку
def add_note():
    notes = get_notes()
    id = get_free_note_id()
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
                note.id = get_free_note_id()
            notes.append(note)
        save_notes(notes)
        print(f'Заметки импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


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

#Выбираем свободный id
def get_free_task_id():
    tasks = get_tasks()
    ids = [task.id for task in tasks]
    return max(ids) + 1 if len(tasks) > 0 else 1

#Добавляем новую задачу
def add_task():
    tasks = get_tasks()
    id = get_free_task_id()
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
                task.id = get_free_task_id()
            tasks.append(task)
        save_tasks(tasks)
        print(f'Задачи импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')


            

if __name__ == '__main__':
    print('Добро пожаловать в Персональный помощник!')

    while True:
        com = interaction(MENU['main'])
        
        #Выход
        if com == 6:
            print('\nЗавершение программы.')
            break
        
        #Заметки
        elif com == 1:
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
                else:
                    print('В разработке')
        #Контакты
        elif com == 3:
            print('\nРаздел: Управление контактами')

        #Фин. записи
        elif com == 4:
            print('\nРаздел: Управление финансовыми записями')

        #Калькулятор
        elif com == 5:
            print('\nРаздел: Калькулятор')

