import telebot
from telebot import apihelper
import google.generativeai as genai
import PIL.Image
import io

# 1. Configuración
TOKEN = '8958607225:AAFTJldth1RmaS-jzmG7izjLtqKqX-_jYns'
genai.configure(api_key="")

# 2. Configuración de red para PythonAnywhere
apihelper.proxy = {}
bot = telebot.TeleBot(TOKEN, threaded=False)

# 3. Inicialización con modelo verificado en tu cuenta
model = genai.GenerativeModel('models/gemini-3.1-flash-image')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "🔍 Analizando imagen con IA...")
    
    try:
        # Descarga de imagen
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = PIL.Image.open(io.BytesIO(downloaded_file))
        
        # Procesamiento
        response = model.generate_content(["Identifica este producto y dame una descripción corta.", img])
        
        bot.reply_to(message, f"✅ Resultado:\n\n{response.text}")
        
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error en la IA: {str(e)}")

print("Bot ShoppingShieldAI activo.")
bot.polling()