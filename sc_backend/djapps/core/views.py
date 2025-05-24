from django.shortcuts import render


def settings_page(request):
    """
    View that displays DEBUG and other settings values
    made available by the context processor.
    """
    return render(request, 'core/settings_page.html')
