from .views import (
    CajaListView,
    CajaDetailView,
    MovementCreateView,
    MovementCancelView,
)
from django.urls import path

app_name = "caja"

urlpatterns = [
    path("", CajaListView.as_view(), name="caja_list"),
    path("<int:pk>/", CajaDetailView.as_view(), name="caja_detail"),
    path("<int:pk>/movement/new", MovementCreateView.as_view(), name="movement_new"),
    path(
        "movement/<int:pk>/cancel", MovementCancelView.as_view(), name="movement_cancel"
    ),
]
