import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Stream


def home(request):
    """Home page with option to start a new stream."""
    return render(request, 'streams/home.html')


@require_http_methods(["POST"])
@csrf_exempt
def create_stream(request):
    """API endpoint to create a new stream."""
    try:
        data = json.loads(request.body)
        title = data.get('title', 'Live Stream')
        host_name = data.get('host_name', 'Host')
        
        stream = Stream.objects.create(
            title=title,
            host_name=host_name,
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'stream_id': stream.stream_id,
            'title': stream.title,
            'host_name': stream.host_name
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def host_stream(request, stream_id):
    """Page for the host to stream their video."""
    stream = get_object_or_404(Stream, stream_id=stream_id, is_active=True)
    return render(request, 'streams/host.html', {
        'stream': stream,
        'share_url': request.build_absolute_uri(f'/watch/{stream.stream_id}/')
    })


def watch_stream(request, stream_id):
    """Page for viewers to watch the stream."""
    stream = get_object_or_404(Stream, stream_id=stream_id, is_active=True)
    return render(request, 'streams/watch.html', {
        'stream': stream
    })


def end_stream(request, stream_id):
    """End a stream (host only)."""
    stream = get_object_or_404(Stream, stream_id=stream_id)
    stream.is_active = False
    stream.save()
    return redirect('home')
