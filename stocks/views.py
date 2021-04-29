import json
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import yfinance as yf
from .models import Stock, Notification
from .forms import *


def index(request):
    request_data = {
        "user": request.session.get("user")
    }
    return render(request, 'stocks/index.html', request_data)


def dashboard(request):
    dashboard_data = {}
    notifications_list = []
    user = find_logged_user(request.session)
    if user:
        dashboard_data["user"] = user.to_json()
        notifications = Notification.objects.filter(user_id=user)
        for notification in (notifications or []):
            stock_name = notification.stock_name
            stock_abbreviation = notification.stock_abbreviation
            stock_value = notification.stock_value
            notification_percentage_change = notification.percentage_change
            setup_date = notification.notification_setup_date

            stock_info = yf.Ticker(stock_abbreviation).history()
            current_value = round(stock_info.tail(1)['Close'].iloc[0], 2)
            goal_value = round(stock_value + (stock_value * notification_percentage_change / 100), 2)
            current_percentage = round((current_value/stock_value) * 100 - 100, 1)

            notifications_list.append({
                "stock_name": stock_name,
                "stock_abbreviation": stock_abbreviation,
                "stock_base_value": stock_value,
                "stock_current_value": current_value,
                "stock_goal_value": goal_value,
                "stock_current_percentage": current_percentage,
                "stock_goal_percentage": notification_percentage_change,
                "setup_date": setup_date
            })
    else:
        return redirect('/user/login')

    dashboard_data["notifications"] = notifications_list

    return render(request, 'stocks/dashboard.html', dashboard_data)


def stocks(request):
    stock_data = get_stocks_data()
    request_data = {
        "data": stock_data,
        "user": request.session.get("user")
    }
    return render(request, 'stocks/stocks.html', request_data)


def get_stocks_data():
    stock_data = {}
    all_stocks = Stock.objects.all()
    if not all_stocks:
        return {}
    tickers = [stock.abbreviation for stock in all_stocks]
    print(tickers)
    stock_frame = yf.download(tickers=tickers[:5], period="1d", interval="1d", group_by="ticker")

    for stock in all_stocks[:5]:
        average = (stock_frame.get(stock.abbreviation).get("High").get(-1) +
                   stock_frame.get(stock.abbreviation).get("Low").get(-1)) / 2
        stock_data[stock] = round(average, 2)

    return stock_data


def login(request):
    if request.method == "GET":
        return render(request, 'stocks/login.html')

    form = LoginForm(request.POST)
    if form.is_valid():
        found_user = form.login(request)
        if found_user:
            request.session['user'] = found_user[0].to_json()
            print('rendering dashboard')
            return redirect('/user/dashboard')
        else:
            print("Wrong credentials")
            print(form.errors)
            return render(request, 'stocks/login.html', {"errors": {"Authentication": [["Invalid credentials"]]}})
    print(form.errors.as_data())
    return render(request, 'stocks/login.html', {"errors": form.errors.as_data()})


def register(request):
    if request.method == "GET":
        return render(request, 'stocks/register.html')
    form = RegistrationForm(request.POST)
    if form.is_valid() and passwords_match(form.cleaned_data):
        create_new_user(form.cleaned_data)
        print("Creating user")
        HttpResponseRedirect(reverse('stocks:login'))
    else:
        print(form.errors)
        print(passwords_match(form.cleaned_data))
        print("Invalid")
        return render(request, 'stocks/register.html', {"errors": form.errors.as_data()})


def create_new_user(form_data):
    user = User()
    user.email = form_data.get('email')
    user.password = form_data.get('password')
    user.username = form_data.get('username')
    user.phone_number = form_data.get('phone_number')
    user.save()


def update_telegram_user(form_data, subscriber):
    subscriber = User.objects.filter(phone_number=form_data.get("phone_number"), username=form_data.get("username"))
    if subscriber:
        subscriber.email = form_data.get("email")
        subscriber.password = form_data.get("password")
        subscriber.save(force_update=True)


def check_user_subscribes_to_telegram(form_data):
    subscriber = User.objects.filter(phone_number=form_data.get("phone_number"), username=form_data.get("username"))
    if subscriber:
        return True
    return False


def passwords_match(form_data):
    return form_data.get("password") == form_data.get("password_repeat")


def assemble_phone_number(form_data):
    prefix = str(form_data.get("number_prefix"))
    number = str(form_data.get("phone_number"))
    if prefix == "None" or number == "None":
        return None
    return int(prefix + number)


def logout(request):
    request.session.flush()
    return redirect('/user/login')


def find_logged_user(session_data):
    found_user = session_data.get('user')
    if found_user:
        email = found_user.get('email')
        return User.objects.filter(email=email)[0]
    else:
        return False


def add_notification(request):
    user = find_logged_user(request.session)
    if user:
        request_data = json.loads(request.body)
        
        notification = Notification(
            user_id=user,
            stock_name=request_data.get('name'),
            stock_abbreviation=request_data.get('abbreviation'),
            stock_value=request_data.get('value'),
            percentage_change=request_data.get('percentage'),
            notification_setup_date=datetime.now(tz=timezone.get_current_timezone()).strftime("%d/%m/%Y %H:%M:%S")
        )
        notification.save()
        return JsonResponse({'status_code': 200})
    else:
        return JsonResponse({'status_code': 400})


def delete_notification(request):
    user = find_logged_user(request.session)
    if user:
        request_data = json.loads(request.body)
        notification = Notification.objects.filter(user_id=user, notification_setup_date=request_data.get('setup_date'))
        notification.delete()
    return JsonResponse({'status_code': 200})


def telegram_update(request):
    request_data = json.loads(request.body)
    print(request_data)

    if request_data.get('chat_member'):
        new_user = request_data['chat_member']
        print(new_user)
    return HttpResponse(request, status=200)
