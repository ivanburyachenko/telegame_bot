import telebot
import random
import json

bot = telebot.TeleBot("6170040590:AAGUXDO0IbeiUo9UILZEQ9j1no5QpItGFuU")

reply_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = telebot.types.KeyboardButton("1️⃣Вгадай число")
btn2 = telebot.types.KeyboardButton("🪨✂️📄Камінь ножиці папір")
btn3 = telebot.types.KeyboardButton("❌⭕️Хрестики нулики")
reply_keyboard.add(btn1, btn2, btn3)

inline_keyboard = telebot.types.InlineKeyboardMarkup()
inl1 = telebot.types.InlineKeyboardButton("🪨", callback_data = "Stone")
inl2 = telebot.types.InlineKeyboardButton("✂️", callback_data = "Scissor")
inl3 = telebot.types.InlineKeyboardButton("📄", callback_data = "Paper")
inline_keyboard.add(inl1, inl2, inl3)

@bot.message_handler(content_types=["text"])
def get_text(message):
    if message.text == "/start" or message.text == "/new_game":
        bot.send_message(message.chat.id, "Будь ласка, оберіть гру!", reply_markup = reply_keyboard)
    elif message.text == "1️⃣Вгадай число":
        bot.send_message(message.chat.id, "Ви обрали гру Вгадай число", reply_markup = telebot.types.ReplyKeyboardRemove())
        
        game_number = random.randint(1,100)
        game_session = {
            'game_number': game_number
        }
        with open(str(message.chat.id)+'.json', "w") as file:
            json.dump(game_session, file)
            
        def guess_number(res):
            with open(str(message.chat.id)+'.json', "r") as f:
                user_dict = json.load(f)
                numb = user_dict["game_number"]
                numb = str(numb) 
                if numb == res.text:
                    bot.send_message(message.chat.id, "Ви вгадали! Оберіть іншу гру:", reply_markup = reply_keyboard)
                else:
                    reset = bot.send_message(message.chat.id, "Ви не вгадали. Спробуйте ще раз:")
                    bot.register_next_step_handler(reset, guess_number)

        res = bot.send_message(message.chat.id, "Число сгенеровоно! Введіть число:")
        bot.register_next_step_handler(res, guess_number)

    elif message.text == "🪨✂️📄Камінь ножиці папір":
        bot.send_message(message.chat.id, "Ви обрали гру Камінь ножиці папір")
        bot.send_message(message.chat.id, "Будь ласка, оберіть символ:", reply_markup = inline_keyboard)
    
    elif message.text == "❌⭕️Хрестики нулики":
        bot.send_message(message.chat.id, "Ви обрали гру Хрестики нулики")

@bot.callback_query_handler(func = lambda call: True)
def get_call(call):
    if call.data =="Stone":
        print("Победа")
    if call.data =="Scissor":
        print("Поражение")
    if call.data =="Paper":
        print("Ничья")
  
bot.infinity_polling()