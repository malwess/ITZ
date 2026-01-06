import json
import os
from datetime import datetime


#Класс Player представляет игрока и управляет всеми его данными
class Player:
    def __init__(self, username):
        #Основные атрибуты игрока
        self.username = username  #Имя пользователя
        self.level = 1  #Уровень персонажа
        self.exp = 0  #Опыт
        self.hp = 100  #Текущее здоровье
        self.max_hp = 100  #Максимальное здоровье
        self.mp = 50  #Текущая мана
        self.max_mp = 50  #Максимальная мана
        self.strength = 10  #Сила - влияет на физический урон
        self.agility = 10  #Ловкость - влияет на скорость и уворот
        self.intellect = 10  #Интеллект - влияет на магический урон
        self.gold = 100  #Золото - игровая валюта
        self.artifacts = []  #Список собранных артефактов
        self.story_branch = None  #Выбранная ветка сюжета
        self.choices = []  #История выборов игрока
        self.current_location = "Начало пути"  #Текущая локация
        self.quests_completed = []  #Завершенные квесты

    #Метод сохранения прогресса игрока в файл
    def save(self):
        #Собираем все данные игрока в словарь
        data = {
            'username': self.username,
            'level': self.level,
            'exp': self.exp,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'strength': self.strength,
            'agility': self.agility,
            'intellect': self.intellect,
            'gold': self.gold,
            'artifacts': self.artifacts,
            'story_branch': self.story_branch,
            'choices': self.choices,
            'current_location': self.current_location,
            'quests_completed': self.quests_completed,
            'last_save': datetime.now().isoformat()  #Время сохранения
        }

        #Создаем папку для сохранений, если она не существует
        if not os.path.exists('saves'):
            os.makedirs('saves')

        #Сохраняем данные в JSON файл с именем пользователя
        with open(f'saves/{self.username}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Игра сохранена для пользователя {self.username}")
        return True

    #Метод загрузки прогресса игрока из файла
    def load(self):
        try:
            #Открываем файл сохранения
            with open(f'saves/{self.username}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)  #Загружаем данные из JSON

            #Обновляем атрибуты игрока данными из файла
            self.__dict__.update(data)
            print(f"Загрузка завершена. Последнее сохранение: {data['last_save']}")
            return True
        except:
            #Если файл не найден или поврежден
            print("Файл сохранения не найден")
            return False

    #Добавление артефакта в инвентарь
    def add_artifact(self, artifact):
        self.artifacts.append(artifact)  # Добавляем артефакт в список
        print(f"Вы получили артефакт: {artifact}")

    #Удаление артефакта из инвентаря
    def remove_artifact(self, artifact):
        if artifact in self.artifacts:
            self.artifacts.remove(artifact)  # Удаляем артефакт
            print(f"Вы потеряли артефакт: {artifact}")
            return True
        return False  #Возвращаем False, если артефакта не было

    #Добавление записи о выборе игрока
    def add_choice(self, choice):
        self.choices.append({
            'choice': choice,  #Описание выбора
            'timestamp': datetime.now().isoformat()  #Время выбора
        })

    #Повышение уровня персонажа
    def level_up(self):
        self.level += 1  #Увеличиваем уровень
        self.max_hp += 20  #Увеличиваем максимальное здоровье
        self.max_mp += 10  #Увеличиваем максимальную ману
        self.hp = self.max_hp  #Восстанавливаем здоровье
        self.mp = self.max_mp  #Восстанавливаем ману
        self.strength += 2  #Увеличиваем силу
        self.agility += 2  #Увеличиваем ловкость
        self.intellect += 2  #Увеличиваем интеллект
        print(f"Уровень повышен! Теперь вы {self.level} уровня!")

    #Получение опыта
    def gain_exp(self, amount):
        self.exp += amount  #Добавляем опыт
        print(f"Получено {amount} опыта. Всего: {self.exp}/{self.level * 100}")

        #Проверяем, достаточно ли опыта для нового уровня
        if self.exp >= self.level * 100:
            self.level_up()  #Повышаем уровень
            self.exp = 0  #Сбрасываем опыт

    #Отображение статистики игрока
    def show_stats(self):
        print("\n" + "=" * 40)
        print(f"Игрок: {self.username}")
        print(f"Локация: {self.current_location}")
        print(f"Ветка истории: {self.story_branch or 'Не выбрана'}")
        print(f"Уровень: {self.level} (Опыт: {self.exp}/{self.level * 100})")
        print(f"Здоровье: {self.hp}/{self.max_hp}")
        print(f"Мана: {self.mp}/{self.max_mp}")
        print(f"Сила: {self.strength}")
        print(f"Ловкость: {self.agility}")
        print(f"Интеллект: {self.intellect}")
        print(f"Золото: {self.gold}")
        print(f"Артефакты: {len(self.artifacts)} шт.")
        #Выводим список артефактов с нумерацией
        for i, art in enumerate(self.artifacts, 1):
            print(f"   {i}. {art}")
        print("=" * 40)