import pandas as pd
import json
import os
from datetime import datetime as dt

#Все файлы, чтобы не терять
NOTES_FILE= 'notes.json'

def greetings():
    print('Добро пожаловать в Персональный помощник!')

def show_main_menu():
    sections = ['Управление заметками', 
                'Управление задачами', 
                'Управление контактами', 
                'Управление финансовыми записями', 
                'Калькулятор', 
                'Выход']
    
    print('Выберите действие:')
    for i in range(1, len(sections)+1):
        print(f'{i}. {sections[i-1]}')

    while True:
        try:
            c = int(input('>> '))
            if 1 <= c <= 6:
                return c
            else:
                raise ValueError    
        except:
            print('Неверный ввод. Повторите ввод.')

def show_notes_menu():
    sections = ['Создание новой заметки', 
                'Просмотр списка заметок', 
                'Просмотр подробностей заметки', 
                'Редактирование заметки', 
                'Удаление заметки', 
                'Импорт заметок в формате csv',
                'Экспорт заметок в формате csv',
                'Выход в главное меню']
    
    print('Выберите действие:')
    for i in range(1, len(sections)+1):
        print(f'{i}. {sections[i-1]}')

    while True:
        try:
            c = int(input('>> '))
            if 1 <= c <= 6:
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

#Выбираем свободный id
def get_free_id():
    notes = get_notes()
    ids = [int(note.id) for note in notes]
    return str(max(ids) + 1)

#добавляем новую заметку
def add_note():
    notes = get_notes()
    id = get_free_id()
    title = input('Введи заголовок: ')
    content = input('Введи содержание: ')
    new_note = Note(id = id, title=title, content=content)
    notes.append(new_note)
    save_notes()
    print(f'Заметка "{title}" добавлена.')


if __name__ == '__main__':
    greetings()
    while True:
        com = show_main_menu()
        if com == 6:
            print('Завершение программы.')
            break
        elif com == 1:
            print('Раздел: Управление заметками')
            com = show_notes_menu()
            if com == 8:
                continue

        else:
            print('Раздел в разработке. Выбери другой раздел.')