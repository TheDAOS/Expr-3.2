# own created file
from django.urls import path
from . import views
# from .views import LoginView

# for image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path(''                             , views.default_home    , name='default_home'),
    
    path('home/'                        , views.home            , name='home'),
    path('table/'                       , views.table           , name='table'),
    
    path('signup/'                      , views.signup          , name='signup'),
    path('login/'                       , views.login_page      , name='login'),
    path('logout/'                      , views.logout          , name='logout'),
    
    path('insert/'                      , views.insert          , name="insert"),
    path('edit/<int:edit_item_id>/'     , views.edit            , name='edit'),
    path('delete/<int:delete_item_id>/' , views.delete          , name='delete'),
    
    path('edit_profile/'                , views.edit_profile    , name='edit_profile'),
    path('delete_profile/'              , views.delete_profile  , name='delete_profile'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for image
