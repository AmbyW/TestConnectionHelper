import datetime
import json

from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from channels.layers import get_channel_layer


# Create your views here.
def catch_up_index(request, cookie_decoded=None):
    request_ip = request.META.get('REMOTE_ADDR')
    request_room = f'room_{request_ip.replace(".", "")}'
    request_group_room = f'group_{request_room}'
    layer = get_channel_layer()
    if request.is_ajax:

        request_headers = dict(request.headers)
        cookie = request_headers.get('Cookie') if 'Cookie' in request_headers.keys() else 'No cookies sent'
        request_cookies = dict(request.COOKIES)
        get_params = dict(request.GET)
        cookie_decoded = cookie
        files = request.FILES if request.FILES else 'No files sent'
        data = request.data if hasattr(request, 'data') else request.body
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        else:
            data = json.loads(data)
        context = {
            'request': {
                'method': request.method,
                'url': request.path,
                'headers': request_headers,
                'params': get_params,
                'cookies': request_cookies if request_cookies else cookie_decoded,
                'data_attribute': 'data' if hasattr(request, 'data') else 'body',
                'data': data,
                'files': files,
                'request_time': datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S.%f')
            }
        }

        response = JsonResponse({"OK": True, "context": context}, status=200)
        context["response"] = {
            'status': response.status_code,
            'headers': dict(response.headers),
            'data': dict(json.loads(response.content.decode('UTF-8'))),
            'cookies': dict(response.cookies),
            'response_time': datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S.%f')
        }
        async_to_sync(layer.group_send)(request_group_room, {'type': 'request_data_message', 'message': context})
        return response
    else:
        context = {
            'request': request,
            'room_name': f'Room {request_ip.replace(".", "")}',
            'room_slug': f'room_{request_ip.replace(".", "")}',
        }
        layer.group_send(request_group_room, {'type': 'request_data_message', 'message': context})
        return redirect(reverse_lazy('show_up'))


def show_up_index(request):
    source_ip = request.META.get('REMOTE_ADDR')
    context = {
        'room_name': f'Room {source_ip.replace(".", "")}',
        'room_slug': f'room_{source_ip.replace(".", "")}'
    }
    return render(request, 'index.html', context)
