from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import About, Contact, get_dealerships, signUp, get_dealer_details, add_review

from django.contrib.auth import views


app_name = 'djangoapp'
urlpatterns = [
    path('', get_dealerships, name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', signUp, name='signup'),
    path('dealer/<int:dealer_id>/', get_dealer_details, name='dealer_details'),
    path('addreview/<int:dealer_id>/', add_review, name="add_review"),

    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout



    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
