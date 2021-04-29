import requests

def send_telegram_message(message_content, receiver):
    request_data = {
        "chat_id": "@mwatrak1",
        "text": "Siema"
    }
    token = "1549227650:AAH-ci2MXQT1Vp76blrNiDnFKSkrrUArOe0"
    message = requests.post('https://api.telegram.org/bot1549227650:AAH-ci2MXQT1Vp76blrNiDnFKSkrrUAr0e0/sendMessage', json=request_data)

    print(message.content)