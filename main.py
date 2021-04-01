import os
import datetime as dt
import json

Moscow_time = dt.timedelta(hours=3)  # Время в Краснодаре по Мск
DATA = dt.datetime.utcnow() + Moscow_time


def counting_tasks(
        templates):

    completedTasks = {}  # Словарь для нахождения значения выполненных задач
    listTrueTasks = {}  # Список True
    uncompletedTasks = {}  # Словарь для нахождения значения невыполненных задач
    listFalseTasks = {}  # Список False

    for element in range(0, len(templates)):  # Проходим по templates, полученный из todos.json
        item = templates[element]
        uid = item.get('userId')
        title = item.get('title')
        success_task = item.get('completed')
        if uid is None:
            continue
        if title is None:
            item['title'] = "None"
            title = item['title']
        if success_task is None:
            item['completed'] = False
        if uid not in completedTasks:
            completedTasks[uid] = {'completed': 0}  # Подсчет выполненых заданий
            uncompletedTasks[uid] = {'completed': 0}  # Подсчет невыполненых заданий
            listTrueTasks[uid] = []  # Хранение списка выполненных задач
            listFalseTasks[uid] = []  # Хранение списка невыполненных задач
        if int(len(title)) > 50:  # Если название задачи больше 50 символов, то обрезать до 50
            title = title[0:50] + "..."  # 50 символов и добавление троеточия.
        if success_task:
            completedTasks[uid]['completed'] += 1
            listTrueTasks[uid].append(title)
        else:
            uncompletedTasks[uid]['completed'] += 1
            listFalseTasks[uid].append(title)

    adding_files(listTrueTasks, completedTasks,
                 listFalseTasks, uncompletedTasks,
                 templates)


def adding_files(
        listTrueTasks, completedTasks,
        listFalseTasks, uncompletedTasks,
        templates):

    for index in range(0, len(templates)):
        item = templates[index]
        if item.get('userId') is None:
            continue
        trueListString = '\n'.join(listTrueTasks[item.get('userId')])  # Корректный вывод в файл выполненных задач
        falseListString = '\n'.join(listFalseTasks[item.get('userId')])  # Корректный вывод в файл невыполненных задач
        if not os.path.isdir('tasks'):  # Для удобства создаю дирректорию если её нет, где будут храниться файлы
            os.mkdir('tasks')  # Создание директории
        # Запись в файл данных
        file = open(r"tasks\\" + str(item.get('userId')) + "_" +
                    str(DATA.strftime('%Y-%U-%dT%H-%M') + ".txt"), "w")  # Создаем и открываем файлы с ключом userId
        file.write("# Сотрудник №" + str(item.get('userId')))  # Сотрудник и его id
        file.write("\n")
        file.write(str(DATA.strftime('%d.%U.%Y %H:%M')))  # Дата создания документа
        file.write("\n\n")
        file.write("## Завершённые задачи (" + str(
            completedTasks[item.get('userId')].get('completed')) + "):")  # Завершенные задачи (их количество)
        file.write("\n")
        file.write(str(trueListString))  # Завершенные задачи (сами задачи)
        file.write("\n\n")
        file.write("## Оставшиеся задачи (" + str(
            uncompletedTasks[item.get('userId')].get('completed')) + "):")  # Незавершенные задачи (их количество)
        file.write("\n")
        file.write(str(falseListString))  # Незавершенные задачи (сами задачи)
        file.close()  # Закрываем файл


def run():
    with open('todos.json') as f:
        templates = json.load(f)

    counting_tasks(templates)


run()
