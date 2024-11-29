import pandas as pd
import json
import os
from datetime import datetime as dt

def greetings():
    print('Добро пожаловать в Персональный помощник!')

def show_menu():
    sections = ['Управление заметками', 
                'Управление задачами', 
                'Управление контактами', 
                'Управление финансовыми записями', 
                'Калькулятор', 
                'Выход']
    
    print('Выберите действие:')
    for i in range(1, 7):
        print(i, sections[i-1])
    while True:
        try:
            c = int(input('>> '))
            if 1 <= c <= 6:
                return c
            else:
                raise ValueError    
        except:
            print('Неверный ввод. Повторите ввод.')


greetings()
while True:
    com = show_menu()
    if com == 6:
        print('Завершение программы.')
        break
    else:
        print('Раздел в разработке. Выбери другой раздел.')

