from django.shortcuts import render

def get_registration(request):
    # ToDo errorMessagesの実装
    return render(request, 'owner/registration.html', {'errorMessages': None})