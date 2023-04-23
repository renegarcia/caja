from .views import (
    CajaListView,
    CajaCreateView,
    CajaDetailView,
    MovementCreateView,
    MovementCancelView,
)
from django.urls import path

app_name = "caja"

urlpatterns = [
    path("", CajaListView.as_view(), name="caja_list"),
    path("new", CajaCreateView.as_view(), name="caja_new"),
    path("<int:pk>/", CajaDetailView.as_view(), name="caja_detail"),
    path("<int:pk>/movement/new", MovementCreateView.as_view(), name="movement_new"),
    path(
        "movement/<int:pk>/cancel", MovementCancelView.as_view(), name="movement_cancel"
    ),
]
