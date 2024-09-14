from django.utils import translation

class AdminLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin panel
        if request.path.startswith('/admin/'):
            # Set language to English for the admin
            translation.activate('en')
        else:
            # Use the default language (Arabic)
            translation.activate('ar')
        
        response = self.get_response(request)
        translation.deactivate()
        return response
