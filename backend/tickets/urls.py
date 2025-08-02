
from django.urls import path
from .views import TicketListCreate, TicketUpdate

urlpatterns = [
    path('', TicketListCreate.as_view()),
    path('<int:pk>/', TicketUpdate.as_view()),
]
