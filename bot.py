import os
import telebot
import google.generativeai as genai
import PIL.Image
import io

# 1. Configuración desde variables de entorno de Render
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Configurar servicios
genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envíame una foto de un producto y lo analizaré.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "🔍 Analizando...")
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = PIL.Image.open(io.BytesIO(downloaded_file))
        
        response = model.generate_content(["Describe este producto", img])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error en IA: {str(e)}")

# 2. LA CLAVE PARA EL ERROR 409
if __name__ == '__main__':
    print("Iniciando bot...")
    bot.remove_webhook()  # Esto borra cualquier conexión previa en Telegram
    bot.polling(none_stop=True, interval=0, timeout=20)
