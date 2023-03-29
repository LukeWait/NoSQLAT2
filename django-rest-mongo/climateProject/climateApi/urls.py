from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('api/climateData/maxPrecipitation/', views.maxPrecipitation),
    path('api/climateData/stationData/', views.stationData),
    #path('api/climateData/indexKey/', views.index_key),
    #path('api/climateData/batchData/', views.batch_data),
    #path('api/stations/', views.add_station),
    path('api/users/', views.users), #add new, delete one/delete multiple (use query string)
    #path('api/climateData/fahrenheitFields/<str:station_id>/<str:date>/', views.fahrenheit_fields),
    #path('api/stations/<str:station_id>/', views.update_station),
    #path('api/users/accessLevel/', views.update_access_level),
    #path('api/users/<str:user_id>/', views.delete_user),
    #path('api/users/', views.delete_multiple_users)
    path('api/login/', views.login)
    ]