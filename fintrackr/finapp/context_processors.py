# own
from .models import Users


def base_user(request):
    
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id= user_id)
    except:
        user = None
    
    context = {
        'user' : user
    }
    
    return context