import os
from datetime import datetime, date, timedelta
import sqlite3
import telebot
# from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from celery import Celery




token=''
bot=telebot.TeleBot(token)
channel_id = -1002
chat_id =  -1002



celery_app = Celery('myproject')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.timezone = 'UTC'
channel_layer = get_channel_layer()




def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        items = []
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request=request, username=username, password=password)

            user_ip = get_client_ip(request)
            bot.send_message(chat_id, f'{username} авторизовался на сайте. \nIP = {user_ip}')

            if user is not None:
                login(request, user)
                request.session.set_expiry(timezone.now() + timedelta(seconds=46800))
                request.session['session_expiry'] = int((timezone.now() + timedelta(seconds=10)).timestamp())
                return redirect('index')          

        return render(request, 'login.html', {
            'items': items
        })


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




@sync_to_async
def get_user_is_authenticated(user): 
    return user.is_authenticated




@api_view(['POST', 'GET'])
@csrf_exempt
def handle_post_request(request):
    if request.method == 'POST':        
        data = request.data  
        print(f"Пришёл новый запрос: {data}")
        valuesList = list(data.values())
        print(valuesList)
        name = valuesList

        print(f'Время: {time}')

        
        (bd)(name)

        return JsonResponse({'status': 'success', 'data': data})


def bd(name, id, district, address, reason, date, time):
    print(
        f'Обработка данных для: {name}')

    base = sqlite3.connect('stat.db')
    cur = base.cursor()
    cur.execute('INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?)',
                (date, time, name, id, district, address, reason))
    base.commit()
    base.close()

    bot.send_message(chat_id=channel_id, text=f'Новые данные!\nСпециалист: {name}')




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip






def index(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user_ip = get_client_ip(request)
        username = request.user.username
        bot.send_message(chat_id, (f'IP - {user_ip}\nСтраница - "Мониторинг"\nПользователь - {username}'))
        current_date = date.today()
        now = datetime.now()
        time_five_minutes_ago = now - timedelta(minutes=5)

        formatted_date = current_date.strftime("%d.%m.%Y")
        formatted_time = time_five_minutes_ago.strftime("%H:%M:%S")

        base = sqlite3.connect('stat.db')
        cur = base.cursor()

        reasons_list = [

                ]

        results = {}
        for reason in reasons_list:
            query = f"SELECT COUNT(*) FROM data WHERE data = ? AND time >= ? AND reason LIKE ?"
            cur.execute(query, (formatted_date, formatted_time, f'%{reason}%'))
            results[reason] = cur.fetchone()[0]

        data_from_db_reason = [{'reason': r, 'count': c}
                               for r, c in results.items()]
        query_full_data = 'SELECT * FROM data WHERE data = ? AND time >= ?'
        cur.execute(query_full_data, (formatted_date, formatted_time,))
        rows_full_data = cur.fetchall()
        data_from_db_full = []

        for row in rows_full_data:
            row_date, time, name, id, district, address, reason = row
            data_from_db_full.insert(0, {
                'name': name,

            })

        base.close()

        return render(request, 'index.html', {'data_from_db_reason': data_from_db_reason, 'data_from_db_full': data_from_db_full})


async def ajax_update(request):
    if request.method == 'GET':
        is_authenticated = await get_user_is_authenticated(request.user)
        if not is_authenticated:
            return render(request, 'login.html')

        current_date = date.today()
        now = datetime.now()
        time_five_minutes_ago = now - timedelta(minutes=5)

        formatted_date = current_date.strftime("%d.%m.%Y")
        formatted_time = time_five_minutes_ago.strftime("%H:%M:%S")

        base = sqlite3.connect('stat.db')
        cur = base.cursor()

        reasons_list = [
                    'Глобалка',

                ]

        results = {}
        for reason in reasons_list:
            query = f"SELECT COUNT(*) FROM data WHERE data = ? AND time >= ? AND reason LIKE ?"
            cur.execute(query, (formatted_date, formatted_time, f'%{reason}%'))
            results[reason] = cur.fetchone()[0]

        data_from_db_reason = [{'reason': r, 'count': c}
                               for r, c in results.items()]

        query_full_data = 'SELECT * FROM data WHERE data = ? AND time >= ?'
        cur.execute(query_full_data, (formatted_date, formatted_time,))
        rows_full_data = cur.fetchall()
        data_from_db_full = []

        for row in rows_full_data:
            row_date, time, name, id, district, address, reason = row
            data_from_db_full.insert(0, {
                'name': name,

            })

        base.close()

        return JsonResponse({'data_from_db_reason': data_from_db_reason, 'data_from_db_full': data_from_db_full})



def stat(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        selected_date = request.GET.get('date', None)
        current_date = date.today().strftime("%d.%m.%Y")
        if selected_date == 'undefined' or not selected_date:
            formatted_date = current_date
        else:
            formatted_date = datetime.strptime(
                selected_date, "%Y-%m-%d").strftime("%d.%m.%Y")

        base = sqlite3.connect('stat.db')
        cur = base.cursor()
        user_ip = get_client_ip(request)
        username = request.user.username
        bot.send_message(chat_id, (f'IP - {user_ip}\nСтраница - "Статистика"\nПользователь - {username}'))
        reasons_list = [
                    'Глобалка',

                ]

        results = {}
        for reason in reasons_list:
            query = "SELECT COUNT(*) FROM data WHERE data = ? AND reason LIKE ?"
            cur.execute(query, (formatted_date, f'%{reason}%'))
            results[reason] = cur.fetchone()[0]

        data_from_db_reason = [{'reason': r, 'count': c}
                               for r, c in results.items()]
        query_full_data = 'SELECT * FROM data WHERE data = ?'
        cur.execute(query_full_data, (formatted_date,))
        rows_full_data = cur.fetchall()
        data_from_db_full = []

        for row in rows_full_data:
            row_date, time, name, id, district, address, reason = row
            data_from_db_full.insert(0, {
                'name': name,

            })

        base.close()

        return render(request, 'stat.html', {'data_from_db_reason': data_from_db_reason, 'data_from_db_full': data_from_db_full})


def search(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        customer_id = request.GET.get('customer_id', None)

        if not customer_id:
            return render(request, 'search.html', {'data_from_db_full': [], 'customer_id': 'не указан'})

        base = sqlite3.connect('stat.db')
        cur = base.cursor()

        query = 'SELECT * FROM data WHERE id = ?'
        cur.execute(
            query, ('https://ai.sknt.ru/?cat=ai_c&customer_id=' + customer_id,))

        data_from_db_full = []

        for row in cur.fetchall():
            row_date, time, name, id, district, address, reason = row
            data_from_db_full.insert(0, {
                'name': name,

            })

        base.close()
        user_ip = get_client_ip(request)
        username = request.user.username
        bot.send_message(chat_id, (f'IP - {user_ip}\nВыполнин поиск по ID\nID - {customer_id}\nПользователь - {username}'))
        message = ''
        if not data_from_db_full:
            message = 'Поиск не дал результатов.'

    return render(request, 'search.html', {'message': message, 'customer_id': customer_id, 'data_from_db_full': data_from_db_full})


def statfull(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        selected_from_date = request.GET.get('from', None)
        selected_to_date = request.GET.get('to', None)

        if not selected_from_date or selected_from_date == 'undefined' or not selected_to_date or selected_to_date == 'undefined':
            return render(request, 'statfull.html')

        selected_from_date = datetime.strptime(
            selected_from_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        selected_to_date = datetime.strptime(
            selected_to_date, "%Y-%m-%d").strftime("%d.%m.%Y")

        base = sqlite3.connect('stat.db')
        cur = base.cursor()
        user_ip = get_client_ip(request)
        username = request.user.username
        bot.send_message(chat_id, (f'IP - {user_ip}\nСтраница - "Отчёт"\nДаты с "{selected_from_date} до {selected_to_date}"\nПользователь - {username}'))
        reasons_list = [
                    'Глобалка',

                ]

        results = {}
        for reason in reasons_list:
            query = "SELECT COUNT(*) FROM data WHERE data BETWEEN ? AND ? AND reason LIKE ?"
            cur.execute(query, (selected_from_date,
                        selected_to_date, f'%{reason}%'))
            result = cur.fetchone()[0]            
            results[reason] = result

        data_from_db_reason = [{'reason': r, 'count': c}
                               for r, c in results.items()]
                               
        base.close()

        return render(request, 'statfull.html', {'data_from_db_reason': data_from_db_reason})
