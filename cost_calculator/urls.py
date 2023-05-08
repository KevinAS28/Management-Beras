from django.urls import path, include
from django.shortcuts import render
import cost_calculator.views as views
urlpatterns = [
    path('daily/', views.cost_calculator_daily),
    path('monthly/', views.cost_calculator_monthly),
    path('calendar/', lambda x: render(x, 'calendar_new.html'))
]
