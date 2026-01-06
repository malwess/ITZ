import json
import os
import random


#Класс Kopilka управляет системой артефактов
class Kopilka:
    def __init__(self):
        self.artifacts_pool = []  #Все существующие артефакты
        self.available_artifacts = []  #Артефакты, доступные для получения
        self.load_artifacts()  #Загружаем артефакты из файла

    #Загрузка артефактов из JSON файла
    def load_artifacts(self):
        if os.path.exists('artifacts.json'):
            #Если файл существует, загружаем данные
            with open('artifacts.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.artifacts_pool = data.get('pool', [])  #Все артефакты
                self.available_artifacts = data.get('available', [])  #Доступные
        else:
            #Если файла нет, создаем начальные артефакты
            self.artifacts_pool = [
                "Меч Древних Королей",
                "Щит Непробиваемой Воли",
                "Плащ Невидимости",
                "Кольцо Вечной Молодости",
                "Посох Бесконечной Магии",
                "Амулет Защиты от Тьмы",
                "Сапоги Скорости Ветра",
                "Перчатка Силы Титанов",
                "Корона Мудрости Предков",
                "Клинок Пожирателя Душ"
            ]
            #Изначально все артефакты доступны
            self.available_artifacts = self.artifacts_pool.copy()
            self.save_artifacts()  #Сохраняем в файл

    #Сохранение артефактов в JSON файл
    def save_artifacts(self):
        data = {
            'pool': self.artifacts_pool,  #Все артефакты
            'available': self.available_artifacts  #Доступные артефакты
        }
        with open('artifacts.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    #Получение случайного доступного артефакта
    def get_random_artifact(self):
        if not self.available_artifacts:
            #Если нет доступных артефактов, генерируем новые
            self.generate_new_artifacts()

        #Выбираем случайный артефакт из доступных
        artifact = random.choice(self.available_artifacts)
        #Удаляем его из списка доступных
        self.available_artifacts.remove(artifact)
        self.save_artifacts()  #Сохраняем изменения
        return artifact

    #Возврат артефакта в копилку
    def return_artifact(self, artifact):
        if artifact not in self.available_artifacts:
            #Добавляем артефакт обратно в список доступных
            self.available_artifacts.append(artifact)
            self.save_artifacts()  #Сохраняем изменения
            print(f"Артефакт '{artifact}' возвращен в копилку")
            return True
        return False  #Возвращаем False, если артефакт уже был доступен

    #Генерация новых артефактов (когда все собраны)
    def generate_new_artifacts(self):
        print("Все артефакты собраны! Генерирую новые...")
        #Создаем новые уникальные артефакты
        new_artifacts = [
            f"Легендарный {random.choice(['Меч', 'Щит', 'Посох', 'Клинок'])} {random.choice(['Дракона', 'Феникса', 'Единорога', 'Грифона'])}",
            f"{random.choice(['Запретный', 'Священный', 'Проклятый', 'Потерянный'])} {random.choice(['Свиток', 'Амулет', 'Кристалл', 'Ключ'])}",
            f"Артефакт {random.choice(['Временной Петли', 'Бесконечности', 'Созидания', 'Разрушения'])}",
            f"{random.choice(['Древний', 'Мистический', 'Божественный', 'Демонический'])} {random.choice(['Тотем', 'Идол', 'Символ', 'Знак'])}"
        ]

        #Добавляем новые артефакты в общий пул
        self.artifacts_pool.extend(new_artifacts)
        #Делаем новые артефакты доступными
        self.available_artifacts = new_artifacts.copy()
        self.save_artifacts()  #Сохраняем изменения

        print("Сгенерировано 4 новых артефакта:")
        for art in new_artifacts:
            print(f"   - {art}")

    #Отображение статуса копилки
    def show_status(self):
        print(f"\nКопилка артефактов:")
        print(f"   Всего артефактов в базе: {len(self.artifacts_pool)}")
        print(f"   Доступно для получения: {len(self.available_artifacts)}")
        if self.available_artifacts:
            print("   Список доступных:")
            #Выводим все доступные артефакты с нумерацией
            for i, art in enumerate(self.available_artifacts, 1):
                print(f"     {i}. {art}")