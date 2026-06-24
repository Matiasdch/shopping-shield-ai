import os
import telebot
import google.generativeai as genai
import PIL.Image
import io

# 1. Configuración de API Keys desde variables de entorno
# Render buscará esto en la sección "Environment Variables" que configuramos
API_KEY = os.environ.get("API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Configuración de los servicios
genai.configure(api_key=API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. Inicialización del modelo
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envíame una foto de un producto y lo analizaré por ti.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "🔍 Analizando imagen con IA...")
    
    try:
        # Descarga de imagen
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = PIL.Image.open(io.BytesIO(downloaded_file))
        
        # Procesamiento con Gemini
        response = model.generate_content(["Identifica este producto y dame una descripción corta.", img])
        
        bot.reply_to(message, f"✅ Resultado:\n\n{response.text}")
        
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error al procesar: {str(e)}")

print("Bot ShoppingShieldAI activo en Render.")
# Sustituye la última línea (bot.polling()) por esto:
if __name__ == '__main__':
    print("Iniciando el bot...")
    bot.remove_webhook() # Esto ayuda a liberar cualquier conexión colgada
    bot.polling(none_stop=True, interval=0, timeout=20)
