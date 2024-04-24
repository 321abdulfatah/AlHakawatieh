# basic URL Configurations
from django.urls import path

# import everything from views
from .views import ClientViews,ServiceViews,check_client_existing,withdrawal_availability,count_videos_terms_and_conditions

# specify URL Path for rest_framework
urlpatterns = [
    path('open_account', ClientViews.as_view()),

    path('check_client_existing', check_client_existing),
    path('withdrawal_availability',withdrawal_availability),
    path('deposit', ServiceViews.as_view()),
    path('withdrawal', ServiceViews.as_view()),
    path('count_videos_terms_and_conditions', count_videos_terms_and_conditions)
]
