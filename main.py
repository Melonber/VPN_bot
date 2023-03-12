import subprocess
import telebot
import qrcode
from io import BytesIO

# Задайте токен вашего бота
TOKEN = ''

# Создайте экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /adduser
@bot.message_handler(commands=['adduser'])
def add_user(message):
    # Получаем от пользователя имя нового пользователя, которое будет использоваться для генерации ключей WireGuard
    user_name = message.text.split()[1]

    # Создаем нового пользователя с помощью Pivpn
    subprocess.run(['pivpn', '-a', '-n', user_name])

    # Читаем сгенерированный файл конфигурации WireGuard нового пользователя
    with open(f'/home/ubuntu/configs/{user_name}.conf', 'rb') as f:
        # Отправляем файл пользователю в виде документа
        bot.send_document(message.chat.id, f, caption=f'WireGuard configuration for {user_name}')

        # Генерируем QR-код
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f.read())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Создаем объект BytesIO для записи изображения QR-кода
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Отправляем изображение QR-кода пользователю в виде фотографии
        bot.send_photo(message.chat.id, img_io, caption=f'QR code for {user_name}')

# Запускаем бота
bot.polling()
