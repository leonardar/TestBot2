import telebot
from telebot import types

# Инициализация бота с токеном
bot = telebot.TeleBot('7859592121:AAHcvWuUYmY7x9kbyKFBSE-69jL7tYACy28')

# Переменная для подсчета очков
points = 0

# Ответы для правильных и неправильных ответов
correct_response = "Ответ правильный!"
incorrect_response = "Ответ неправильный!"

# Вопросы викторины с темами по Python
quiz_data = [
    {
        "question": "Как называется тип данных для хранения целых чисел в Python?",
        "options": ["int", "float", "str"],
        "correct": "int"
    },
    {
        "question": "Какая функция используется для вывода текста в Python?",
        "options": ["print()", "input()", "def()"],
        "correct": "print()"
    },
    {
        "question": "Каким символом обозначаютсякомментарии в Python?",
        "options": ["//", "#", "--"],
        "correct": "#"
    },
    {
        "question": "Какой метод используется для добавления элемента в список в Python?",
        "options": ["append()", "insert()", "add()"],
        "correct": "append()"
    }
]

# Индекс текущего вопроса
current_question = 0

# Команда /start, которая запускает меню
@bot.message_handler(commands=['start'])
def start(message):
    global points, current_question
    points = 0  # Сбрасываем очки
    current_question = 0  # Начинаем с первого вопроса

    # Создаем инлайн-кнопку "Начать"
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton('Начать',
callback_data='start_quiz')
    markup.add(start_button)

    # Отправляем сообщение с инлайн-кнопкой "Начать"
    bot.send_message(message.chat.id, 'Привет! Я бот-викторина! Нажмите кнопку "Начать", чтобы начать викторину.',
reply_markup=markup)

# Обработка нажатий инлайн-кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'start_quiz')
def start_quiz(call):
    global points, current_question
    points = 0  # Сбрасываем очки
    current_question = 0  # Начинаем с первого вопроса
    ask_question(call.message)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in [opt for q in quiz_data for opt in q["options"]]:
        check_answer(message)

# Функция для отправки вопроса и вариантов ответа
def ask_question(message):
    global current_question
    if current_question < len(quiz_data):
        # Получаем текущий вопрос и варианты ответов
        question = quiz_data[current_question]["question"]
        options = quiz_data[current_question]["options"]

        # Создаем инлайн-клавиатуру с вариантами ответа
        markup = types.InlineKeyboardMarkup()
        for option in options:
            markup.add(types.InlineKeyboardButton(option, callback_data=option))

        # Отправляем вопрос и клавиатуру
        bot.send_message(message.chat.id, question, reply_markup=markup)
    else:
        # Викторина закончена
        bot.send_message(message.chat.id, f"Викторина окончена!аши баллы: {points}.")
        current_question = 0  # Сбрасываем для возможности начать заново

# Функция для проверки ответа
@bot.callback_query_handler(func=lambda call: call.data
in [opt for q in quiz_data for opt in q["options"]])
def check_answer(call):
    global points, current_question
    correct_answer = quiz_data[current_question]["correct"]

    if call.data == correct_answer:
        points += 1  # Если ответ правильный, увеличиваем очки
        bot.answer_callback_query(call.id, text=correct_response)
    else:
        bot.answer_callback_query(call.id, text=incorrect_response +
f" Правильный ответ: {correct_answer}.")

    current_question += 1  # Переход к следующему вопросу
    ask_question(call.message)  # Задаем следующий вопрос

# Запуск бота
bot.polling(none_stop=True)
