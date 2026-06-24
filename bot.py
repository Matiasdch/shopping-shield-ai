import os
import telebot
import google.generativeai as genai
import PIL.Image
import io
from flask import Flask # Necesitas instalar flask en tu requirements.txt
from threading import Thread

# Configuración
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TELEGRAM_TOKEN")
genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)
model = genai.GenerativeModel('gemini-1.5-flash')

# Servidor Flask minúsculo para que Render no cierre el bot
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot activo"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Lógica del bot... (tu código anterior de handle_photo aquí)

if __name__ == '__main__':
    # Arrancamos el servidor web en un hilo separado
    Thread(target=run_flask).start()
    # Arrancamos el bot
    bot.remove_webhook()
    bot.polling(none_stop=True)
