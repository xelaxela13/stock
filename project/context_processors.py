def is_home(request):
    if request.path == '/' + request.LANGUAGE_CODE + '/' or request.path == '/':
        return True
    return False
