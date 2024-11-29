def greetings():
    print('Добро пожаловать в Персональный помощник!')

def show_menu():
    print('Выберите действие:')
    sections = ['Управление заметками', 'Управление задачами', 'Управление контактами', 'Управление финансовыми записями', 'Калькулятор', 'Выход']
    for i in range(1, 7):
        print(i, sections[i-1])
    print('>> ', end='')
    n = 6
    try:
        n = int(input())
    except:
        print('Неверный ввод')
    return n


