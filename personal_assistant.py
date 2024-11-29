import pandas as pd
import json
import os
from datetime import datetime as dt
import csv

#Все файлы, чтобы не терять
NOTES_FILE = 'notes.json'
NOTES_EXPORT_FILE = 'notes_export.csv'
MENU = {
    'main': ['1. Управление заметками', '2. Управление задачами', '3. Управление контактами', 
             '4. Управление финансовыми записями', '5. Калькулятор', '6. Выход'],
    'notes': ['1. Создание новой заметки', '2. Просмотр списка заметок', '3. Просмотр подробностей заметки', '4. Редактирование заметки', 
              '5. Удаление заметки', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню']
}

def greetings():
    print('Добро пожаловать в Персональный помощник!')

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
        except:
            print('Неверный ввод. Повторите ввод.')

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
    
#Конвертируем заметку в dict для json
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
            id = str(int(input('Введите id заметки >> ')))
            if id not in [note.id for note in notes]:
                print('Заметка не найдена')
            else:
                for note in notes:
                    if note.id == id:
                        print(f'Заголовок: {note.title}\nСодержание: {note.content}\nДата: {note.timestamp}')
                        break
        except:
            print('Некорректный id.')

#Обновляем заметку
def update_note():
    notes = get_notes()
    if len(notes) == 0:
        print('Заметки отсутствуют')
    else:
        try:
            id = str(int(input('Введите id заметки >> ')))
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
        except:
            print('Некорректный id.')

#Выбираем свободный id
def get_free_id():
    notes = get_notes()
    ids = [int(note.id) for note in notes]
    return str(max(ids) + 1) if len(notes) > 0 else '1'

#Добавляем новую заметку
def add_note():
    notes = get_notes()
    id = get_free_id()
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
        id = str(int(input('Введите id заметки >> ')))
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
            note = Note(id=str(row['id']), title=row['title'], content=row['content'], timestamp=row['timestamp'])
            if note.id in [n.id for n in notes]:
                note.id = get_free_id()
            notes.append(note)
        save_notes(notes)
        print(f'Заметки импортированы из {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')

if __name__ == '__main__':
    greetings()
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

        #Контакты
        elif com == 3:
            print('\nРаздел: Управление контактами')

        #Фин. записи
        elif com == 4:
            print('\nРаздел: Управление финансовыми записями')

        #Калькулятор
        elif com == 5:
            print('\nРаздел: Калькулятор')

