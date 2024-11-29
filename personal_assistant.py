import pandas as pd
import json
import os
from datetime import datetime as dt

#Все файлы, чтобы не терять
NOTES_FILE = 'notes.json'

MENU = {
    'main': ['1. Управление заметками', '2. Управление задачами', '3. Управление контактами', 
             '4. Управление финансовыми записями', '5. Калькулятор', '6. Выход'],
    'notes': ['1. Создание новой заметки', '2. Просмотр списка заметок', '3. Просмотр подробностей заметки', '4. Редактирование заметки', 
              '5. Удаление заметки', '6. Импорт заметок в формате csv', '7. Экспорт заметок в формате csv', '8. Выход в главное меню']
}

def greetings():
    print('Добро пожаловать в Персональный помощник!')

def interaction(sections):
    print('Выберите действие:')
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
            if str(id) not in [note.id for note in notes]:
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
            id = int(input('Введите id заметки >> '))
            if str(id) not in [note.id for note in notes]:
                print('Заметка не найдена')
            else:
                tmp_title = input('Введи новый заголовок >> ')
                tmp_content = input('Введи новое содержание >> ')
                notes = [note for note in notes if note.id != str(id)]
                notes.append(Note(id = str(id), title=tmp_title, content=tmp_content, timestamp=dt.now().strftime('%d-%m-%Y %H:%M:%S')))
        except:
            print('Некорректный id.')

#Выбираем свободный id
def get_free_id():
    notes = get_notes()
    ids = [int(note.id) for note in notes]
    return str(max(ids) + 1)

#Добавляем новую заметку
def add_note():
    notes = get_notes()
    id = get_free_id()
    title = input('Введи заголовок: ')
    content = input('Введи содержание: ')
    new_note = Note(id = id, title=title, content=content)
    notes.append(new_note)
    save_notes()
    print(f'Заметка "{title}" добавлена.')

#Удаляем заметку
def delete_note():
    notes = get_notes()
    try:
        id = int(input('Введите id заметки >> '))
        notes = [note for note in notes if note.id != str(id)]
        save_notes()
        print('Заметка удалена')
    except:
        print('Некорректный id.')

if __name__ == '__main__':
    greetings()
    while True:
        com = interaction(MENU['main'])
        
        if com == 6:
            print('Завершение программы.')
            break
        
        elif com == 1:
            print('Раздел: Управление заметками')
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
                    print('Команда в разработке')
                elif com == 7:
                    print('Команда в разработке')
                elif com == 8:
                    break
                else:
                    print('Выбрана неверная команда')

        else:
            print('Раздел в разработке. Выбери другой раздел.')
