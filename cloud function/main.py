from dotenv import load_dotenv
import os
from pymongo import MongoClient
import yfinance as yf
from whatsapp import send_whatsapp_message

load_dotenv()
db = os.getenv('DB_HOST')
client = MongoClient(db)

stocks = {}


def send_notifications():
    notification_collection = client.get_database('stocks').get_collection('stocks_notification')
    for notification in notification_collection.find({}):

        if notification['stock_abbreviation'] not in stocks:
            stock_info = yf.Ticker(notification['stock_abbreviation'])
            current_stock_value = stock_info.history().tail(1)['Close'].iloc[0]
            stocks[notification['stock_abbreviation']] = current_stock_value

        notification_trigger_value = notification['stock_value'] + \
            (notification['stock_value'] * notification['percentage_change'] / 100)

        notification_ready = check_if_stock_reached_percentage(
            notification_trigger_value=notification_trigger_value,
            stock_abbreviation=notification['stock_abbreviation'],
            percentage=notification['percentage_change'])

        if notification_ready:
            print("User notified")
            message = prepare_notification_message(notification_trigger_value, notification['stock_abbreviation'])
            send_whatsapp_message(message, "+48796971012")
        else:
            print("Notification not ready")


def check_if_stock_reached_percentage(notification_trigger_value, stock_abbreviation, percentage):
    if percentage > 0:
        return notification_trigger_value <= stocks[stock_abbreviation]
    else:
        return notification_trigger_value >= stocks[stock_abbreviation]


def prepare_notification_message(notification_trigger_value, stock_abbreviation):
    return f'{stock_abbreviation} reached your goal and is currently at {notification_trigger_value}$'


if __name__ == "__main__":
    send_notifications()
