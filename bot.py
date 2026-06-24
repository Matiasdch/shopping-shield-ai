import os
import telebot
import google.generativeai as genai
import PIL.Image
import io

# Configuración segura
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TELEGRAM_TOKEN")

genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TOKEN)

# Usamos el modelo que es el estándar actual para imágenes
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "🔍 Analizando con IA...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = PIL.Image.open(io.BytesIO(downloaded_file))
        
        # Esta es la forma correcta de solicitar el análisis
        response = model.generate_content(["Describe este producto brevemente", img])
        
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Esto soluciona el error 409 (Conflict) que tenías
if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
