import random
import time
import hashlib
import os
import json
from player import Player
from kopilka import Kopilka

# Базовый класс для всех существ в бою
class Human:
    def __init__(self, name, hp, mp, strength, agility, intellect):
        self._name = name  # Имя существа
        self._hp = hp  # Текущее здоровье
        self._max_hp = hp  # Максимальное здоровье
        self._mp = mp  # Текущая мана
        self._strength = strength  # Сила (влияет на физический урон)
        self._agility = agility  # Ловкость (влияет на скорость/уворот)
        self._intellect = intellect  # Интеллект (влияет на магический урон)

    # Свойство: жив ли персонаж
    @property
    def is_alive(self):
        return self._hp > 0  # Возвращает True если здоровье > 0

    # Свойство: текущее здоровье
    @property
    def hp(self):
        return self._hp

    # Метод получения урона
    def take_damage(self, dmg):
        # Уменьшаем здоровье, но не ниже 0
        self._hp = max(0, self._hp - dmg)
        print(f"{self._name} получает {dmg} урона (HP={self._hp})")

    # Базовая атака
    def attack(self, target):
        dmg = self._strength  # Урон равен силе
        print(f"{self._name} атакует {target._name} на {dmg} урона")
        target.take_damage(dmg)  # Наносим урон цели


# Класс Воина (специализируется на физическом уроне)
class Warrior(Human):
    # Переопределяем метод атаки для воина
    def attack(self, target):
        # Воин наносит базовый урон + случайный бонус (1-3)
        dmg = self._strength + random.randint(1, 3)
        print(f"Воин {self._name} наносит {dmg} урона")
        target.take_damage(dmg)  # Наносим урон цели


# Класс Мага (специализируется на магическом уроне)
class Mage(Human):
    # Переопределяем метод атаки для мага
    def attack(self, target):
        if self._mp >= 5:  # Проверяем, достаточно ли маны
            # Магическая атака: урон = интеллект * 2
            dmg = self._intellect * 2
            # Тратим ману (не менее 0)
            self._mp = max(0, self._mp - 5)
            print(f"Маг {self._name} кастует заклинание и бьёт на {dmg} урона (MP={self._mp})")
        else:
            # Если маны нет - слабая физическая атака
            print(f"Маг {self._name} устал и бьёт кулаком (1 урона)")
            dmg = 1
        target.take_damage(dmg)  # Наносим урон цели


# Класс Босса (особый противник с двумя фазами)
class Boss(Human):
    def __init__(self, name, hp, mp, strength, agility, intellect):
        super().__init__(name, hp, mp, strength, agility, intellect)
        self.phase = 1  # Начальная фаза босса

    # Переопределяем метод атаки для босса
    def attack(self, target):
        if self.phase == 1:
            # Фаза 1: обычная атака
            dmg = self._strength
        else:
            # Фаза 2 (ярость): усиленная атака
            dmg = self._strength + 5
        print(f"{self._name} бьёт {target._name} на {dmg} урона")
        target.take_damage(dmg)  # Наносим урон цели


# Функция боя

def battle(player, enemy_name, enemy_hp):
    # Отображаем информацию о начале боя
    print(f"\n{'=' * 50}")
    print(f"НАЧИНАЕТСЯ БИТВА!")
    print(f"{player.username} против {enemy_name}")
    print(f"{'=' * 50}")

    # Создаем персонажа игрока для битвы (на основе его статистики)
    player_character = Warrior(
        player.username,  # Имя
        player.hp,  # Здоровье
        player.mp,  # Мана
        player.strength,  # Сила
        player.agility,  # Ловкость
        player.intellect  # Интеллект
    )

    # Создаем врага (немного слабее игрока)
    enemy = Boss(
        enemy_name,  # Имя врага
        enemy_hp,  # Здоровье врага
        20,  # Мана врага
        player.strength - 2,  # Сила (на 2 меньше игрока)
        player.agility - 2,  # Ловкость (на 2 меньше игрока)
        player.intellect - 2  # Интеллект (на 2 меньше игрока)
    )

    round_num = 1  # Номер текущего раунда
    # Цикл боя: продолжается, пока оба участника живы
    while enemy.is_alive and player_character.is_alive:
        print(f"\n--- Раунд {round_num} ---")

        # Ход игрока
        print(f"\nВаш ход:")
        print("1. Атаковать")  # Обычная атака
        print("2. Использовать умение")  # Специальная атака

        choice = input("Выберите действие: ")
        if choice == "1":
            # Обычная атака
            player_character.attack(enemy)
        elif choice == "2":
            # Специальная атака (усиленная)
            dmg = player_character._strength + 5
            print(f"Вы используете специальную атаку на {dmg} урона!")
            enemy.take_damage(dmg)
        else:
            # Неверный выбор - обычная атака
            print("Неверный выбор, просто атакую")
            player_character.attack(enemy)

        # Ход врага (если он еще жив)
        if enemy.is_alive:
            enemy.attack(player_character)

        round_num += 1  # Переход к следующему раунду
        time.sleep(1)  # Пауза для читаемости

    # ОПРЕДЕЛЕНИЕ РЕЗУЛЬТАТА БОЯ
    if player_character.is_alive:
        # Игрок победил
        print(f"\nПОБЕДА! Вы победили {enemy_name}!")
        # Награда: случайное количество золота
        reward = random.randint(50, 150)
        player.gold += reward
        player.gain_exp(50)  # Опыт за победу
        print(f"Вы получили {reward} золота и 50 опыта!")
        return True  # Возвращаем True при победе
    else:
        # Игрок проиграл
        print(f"\nПОРАЖЕНИЕ! {enemy_name} победил вас!")
        # Наказание: здоровье уменьшается вдвое (но не меньше 1)
        player.hp = max(1, player.hp // 2)
        print(f"Ваше здоровье уменьшено до {player.hp}")
        return False  # Возвращаем False при поражении


# Класс игры (управляет основным процессом)

class Game:
    def __init__(self):
        self.kopilka = Kopilka()  # Инициализируем копилку артефактов
        self.player = None  # Текущий игрок (будет установлен позже)
        self.current_story = None  # Текущая сюжетная линия


    # Система аутентификации=>


    # Регистрация нового пользователя
    def register_user(self):
        print("\nРЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")
        username = input("Придумайте имя пользователя: ")
        password = input("Придумайте пароль: ")

        # Проверяем существование файла с пользователями
        if os.path.exists('users.json'):
            # Загружаем существующих пользователей
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
        else:
            # Создаем новый словарь пользователей
            users = {}

        # Проверяем, не существует ли уже такой пользователь
        if username in users:
            print("Пользователь с таким именем уже существует!")
            return False

        # Сохраняем пользователя (пароль в открытом виде по условию)
        users[username] = password

        # Сохраняем обновленный список пользователей
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        print(f"Пользователь {username} успешно зарегистрирован!")
        return True

    # Вход существующего пользователя
    def login(self):
        print("\nВХОД В СИСТЕМУ")
        username = input("Имя пользователя: ")
        password = input("Пароль: ")

        # Проверяем существование файла с пользователями
        if not os.path.exists('users.json'):
            print("Файл с пользователями не найден!")
            return False

        # Загружаем пользователей
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)

        # Проверяем логин и пароль
        if username in users and users[username] == password:
            print(f"Вход выполнен успешно! Добро пожаловать, {username}!")
            # Создаем объект игрока
            self.player = Player(username)

            # Предлагаем загрузить сохранение (если оно есть)
            if os.path.exists(f'saves/{username}.json'):
                choice = input("Найдено сохранение. Загрузить? (да/нет): ").lower()
                if choice == 'да':
                    self.player.load()  # Загружаем сохранение
                else:
                    print("Начинаем новую игру...")
            return True  # Успешный вход
        else:
            print("Неверное имя пользователя или пароль!")
            return False  # Неудачный вход

#Сюжетные ветки

    # Выбор начальной сюжетной ветки
    def choose_story_branch(self):
        print("\n" + "=" * 50)
        print("ВЫБОР ПУТИ СУДЬБЫ")
        print("=" * 50)
        print("\nТри пути открываются перед вами:")
        print("1. Путь Воина - Слава и честь через силу оружия")
        print("2. Путь Мудреца - Знания и магия через изучение тайн")
        print("3. Путь Странника - Свобода и приключения через путешествия")

        choice = input("\nВыберите свой путь (1-3): ")

        if choice == "1":
            # Путь Воина: бонус к силе
            self.player.story_branch = "Путь Воина"
            self.player.strength += 5
            self.player.add_choice("Выбран Путь Воина")
            print("\nВы выбрали Путь Воина!")
            print("Сила увеличена на +5")

        elif choice == "2":
            # Путь Мудреца: бонус к интеллекту и мане
            self.player.story_branch = "Путь Мудреца"
            self.player.intellect += 5
            self.player.mp += 20
            self.player.add_choice("Выбран Путь Мудреца")
            print("\nВы выбрали Путь Мудреца!")
            print("Интеллект увеличен на +5")
            print("Мана увеличена на +20")

        elif choice == "3":
            # Путь Странника: бонус к ловкости и здоровью
            self.player.story_branch = "Путь Странника"
            self.player.agility += 5
            self.player.max_hp += 30
            self.player.hp += 30
            self.player.add_choice("Выбран Путь Странника")
            print("\nВы выбрали Путь Странника!")
            print("Ловкость увеличена на +5")
            print("Максимальное здоровье увеличено на +30")

        else:
            # Неверный выбор - путь по умолчанию
            print("Неверный выбор, назначается путь по умолчанию")
            self.player.story_branch = "Путь Неопределившегося"

        # Обновляем локацию игрока
        self.player.current_location = "Перекресток Судьбы"
        time.sleep(2)  # Пауза для чтения

    # Сюжетная ветка "Путь Воина"
    def story_warrior(self):
        print("\n" + "=" * 50)
        print("ПУТЬ ВОИНА: ИСПЫТАНИЕ ЧЕСТИ")
        print("=" * 50)

        # Предлагаем выбор в рамках ветки Воина
        print("\nВы прибываете в замок рыцарей. Старый командир предлагает:")
        print("1. Присоединиться к защите границ")
        print("2. Пройти испытание в арене")
        print("3. Искать древний артефакт в руинах")

        choice = input("\nВаш выбор: ")
        # Сохраняем выбор игрока
        self.player.add_choice(f"На пути воина выбрано: {choice}")

        if choice == "1":
            print("\nВы отправляетесь защищать границы королевства.")
            self.player.current_location = "Граница королевства"

            print("\nНа границе вас атакуют разбойники!")
            # Начинаем бой с разбойниками
            if battle(self.player, "Главарь разбойников", 40):
                # Награда за победу
                print("\nКапитан гарнизона награждает вас.")
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)
                self.player.gold += 100

        elif choice == "2":
            print("\nВы выходите на арену перед тысячами зрителей.")
            self.player.current_location = "Главная арена"

            print("\nВаш противник - чемпион арены!")
            # Начинаем бой с чемпионом арены
            if battle(self.player, "Чемпион арены", 60):
                # Награда за победу
                print("\nКороль лично награждает вас.")
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)
                self.player.gain_exp(100)

        elif choice == "3":
            print("\nВы отправляетесь в древние руины.")
            self.player.current_location = "Древние руины"

            print("\nВ руинах вы встречаете древнего стража!")
            # Начинаем бой со стражем
            if battle(self.player, "Древний страж", 50):
                # Награда за победу (два артефакта!)
                print("\nВы нашли скрытую сокровищницу!")
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)
                artifact2 = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact2)
                print("Найдено 2 артефакта!")

        time.sleep(2)  # Пауза

    # Сюжетная ветка "Путь Мудреца" (структура аналогична)
    def story_mage(self):
        print("\n" + "=" * 50)
        print("ПУТЬ МУДРЕЦА: ТАЙНЫ МАГИИ")
        print("=" * 50)

        print("\nВы в Великой Библиотеке. Архивариус предлагает:")
        print("1. Изучить древние заклинания")
        print("2. Исследовать аномалию в магическом лесу")
        print("3. Расшифровать проклятый свиток")

        choice = input("\nВаш выбор: ")
        self.player.add_choice(f"На пути мудреца выбрано: {choice}")

        if choice == "1":
            print("\nВы погружаетесь в изучение древних фолиантов.")
            self.player.current_location = "Зал запретных знаний"

            print("\nДревний дух книги атакует вас!")
            if battle(self.player, "Дух запретной книги", 35):
                print("\nВы освоили новое заклинание!")
                self.player.intellect += 3
                self.player.mp += 30

        elif choice == "2":
            print("\nВы отправляетесь в магический лес.")
            self.player.current_location = "Сердце магического леса"

            print("\nМагические существа атакуют вас!")
            if battle(self.player, "Повелитель элементалей", 55):
                print("\nВы постигли тайны магии природы!")
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)
                self.player.gain_exp(80)

        elif choice == "3":
            print("\nВы пытаетесь расшифровать древний свиток.")
            self.player.current_location = "Кабинет алхимика"

            print("\nСвиток оживает и атакует вас!")
            if battle(self.player, "Древнее проклятие", 45):
                print("\nСвиток раскрывает свои секреты!")
                self.player.intellect += 5
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)

        time.sleep(2)

    # Сюжетная ветка "Путь Странника" (структура аналогична)
    def story_wanderer(self):
        print("\n" + "=" * 50)
        print("ПУТЬ СТРАННИКА: ДОРОГА ПРИКЛЮЧЕНИЙ")
        print("=" * 50)

        print("\nВы в таверне 'Бродячий феникс'. Слухи говорят о:")
        print("1. Затерянном городе в пустыне")
        print("2. Тайном обществе в портовом городе")
        print("3. Легендарном корабле-призраке")

        choice = input("\nВаш выбор: ")
        self.player.add_choice(f"На пути странника выбрано: {choice}")

        if choice == "1":
            print("\nВы отправляетесь через раскаленную пустыню.")
            self.player.current_location = "Затерянный город"

            print("\nДревние механизмы охраняют город!")
            if battle(self.player, "Страж пирамиды", 40):
                print("\nВы нашли сокровища фараона!")
                self.player.gold += 200
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)

        elif choice == "2":
            print("\nВы проникаете в тайное общество.")
            self.player.current_location = "Подземелья порта"

            print("\nЧлены общества испытывают вас в бою!")
            if battle(self.player, "Мастер клинков", 50):
                print("\nВас принимают в общество!")
                self.player.agility += 4
                self.player.gain_exp(70)

        elif choice == "3":
            print("\nВы выходите в открытое море.")
            self.player.current_location = "Палуба корабля-призрака"

            print("\nПризрачная команда атакует!")
            if battle(self.player, "Капитан-призрак", 60):
                print("\nВы завладели сокровищами корабля!")
                artifact = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact)
                artifact2 = self.kopilka.get_random_artifact()
                self.player.add_artifact(artifact2)
                print("Найдено 2 артефакта!")

        time.sleep(2)

#Система сохранения

    def save_progress(self):
        if self.player:
            # Спрашиваем, хочет ли игрок сохраниться
            save_choice = input("\nХотите сохранить прогресс? (да/нет): ").lower()
            if save_choice == 'да':
                self.player.save()  # Сохраняем прогресс
            else:
                print("\nПрогресс не сохранен!")
                print("Все артефакты возвращаются в копилку...")

                # Возвращаем все артефакты в копилку
                artifacts_to_return = self.player.artifacts.copy()
                for artifact in artifacts_to_return:
                    self.kopilka