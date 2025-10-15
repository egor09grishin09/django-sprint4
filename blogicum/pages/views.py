from django.shortcuts import render


def handler404(request, exception):
    return render(request, 'pages/404.html', status=404)


def handler403csrf(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def handler500(request):
    return render(request, 'pages/500.html', status=500)
