
---

````markdown
# CurvativeParameter

**CurvativeParameter** — это Django-приложение для численных вычислений с использованием алгоритмов Гаусса, градиентного спуска и других методов. Оно поддерживает управление таблицами данных, визуализацию результатов, пользовательские профили, аутентификацию и форумы.

---

## 🚀 Основные возможности

- Управление таблицами (`Table`) и точками (`Point`)
- Поддержка расчётных алгоритмов:
  - Метод Гаусса
  - Гаусс с шагом
  - Градиентный спуск
  - Метод отжига
- Отображение результатов (`CalculationResult`) в виде графиков
- Форум с возможностью создавать, редактировать и удалять посты
- Пользовательская регистрация, вход в систему и профили
- Автоматическое тестирование и отчёты о покрытии кода

---

## 🐳 Быстрый старт с Docker

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/CurvativeParameter.git
cd CurvativeParameter
````

### 2. Постройте и запустите контейнер:

```bash
docker-compose up --build
```

### 3. Примените миграции и создайте суперпользователя:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 4. (Опционально) Загрузите тестовые данные:

```bash
docker-compose exec web python manage.py loaddata table1_fixture.json
```

---

## 📊 Пример тестовой таблицы

В тестовых данных (`table1_fixture.json`) содержится реакция:

**1-Chlorobutane + Ethanol**, при температуре **278.15 K**.
Точки данных:

```
0.0697;407
0.0960;523
0.1038;554
0.1312;654
0.1325;659
0.2160;888
0.2739;995
0.4069;1116
0.4984;1112
0.5977;1036
0.6275;999
0.7020;880
0.7197;846
0.8078;643
0.8115;634
0.9187;307
```

---

## ⚙️ Установка вручную (без Docker)

### Требования

* Python 3.8+
* Django 4.0+
* `virtualenv`, `pip`

### Установка

```bash
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Тестирование

### Запуск тестов:

```bash
python manage.py test
```

### Проверка покрытия:

```bash
pip install coverage

coverage run --source='.' manage.py test
coverage report
coverage html
```

Откройте файл `htmlcov/index.html` в браузере для детального просмотра покрытия.

---

## 🗂️ Структура проекта

```
CurvativeParameter/
│
├── main/                   # Основное Django-приложение
│   ├── models.py           # Модели: Table, Point, CalculationResult, Post, Profile
│   ├── views.py            # Представления
│   ├── forms.py            # Формы для аутентификации, постов и графиков
│   ├── gauss.py            # Метод Гаусса
│   ├── gauss_step.py       # Метод Гаусса с шагом
│   ├── gradient.py         # Градиентный спуск
│   ├── otzhig.py           # Метод отжига
│   └── tests.py            # Тесты
│
├── website/                # Конфигурация проекта
│   ├── settings.py
│   └── urls.py
│
├── manage.py               # Django CLI
├── Dockerfile              # Docker-образ
├── docker-compose.yml      # Оркестрация контейнеров
├── requirements.txt        # Зависимости
└── table1_fixture.json     # Пример тестовой таблицы
```

---

## 🧩 Пример использования

1. **Создание таблицы:**

   * Войдите как зарегистрированный пользователь
   * Перейдите на страницу создания таблицы
   * Введите точки: пары значений `x` и `y`

2. **Выполнение вычислений:**

   * Выберите таблицу
   * Укажите нужный алгоритм
   * Запустите расчёт и получите результат

3. **Работа с форумом:**

   * Создавайте посты
   * Редактируйте и удаляйте обсуждения

---

## 🤝 Вклад в проект

Хотите помочь?

1. Сделайте форк:

   ```bash
   git checkout -b feature/your-feature
   ```
2. Внесите изменения, запустите тесты:

   ```bash
   python manage.py test
   ```
3. Создайте Pull Request

---

## 🛠️ Устранение неполадок

* **"No file to run: manage.py"**
  Убедитесь, что вы в корневой директории проекта.

* **Тесты не выполняются**
  Проверьте файл `main/tests.py` на наличие синтаксических ошибок и корректность импортов.

* **Низкое покрытие тестов**
  Добавьте тесты для `views.py`, `models.py`, `forms.py` и расчётных алгоритмов. Используйте `coverage html` для анализа.

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

---

