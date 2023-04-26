from .views import (
    CajaListView,
    CajaCreateView,
    CajaDeleteView,
    CajaDetailView,
    CajaUpdateView,
    MovementCreateView,
    MovementCancelView,
)
from django.urls import path

app_name = "caja"

urlpatterns = [
    path("", CajaListView.as_view(), name="caja_list"),
    path("new", CajaCreateView.as_view(), name="caja_new"),
    path("<int:pk>/", CajaDetailView.as_view(), name="caja_detail"),
    path("<int:pk>/edit", CajaUpdateView.as_view(), name="caja_update"),
    path("<int:pk>/delete", CajaDeleteView.as_view(), name="caja_delete"),
    path("<int:pk>/movement/new", MovementCreateView.as_view(), name="movement_new"),
    path(
        "movement/<int:pk>/cancel", MovementCancelView.as_view(), name="movement_cancel"
    ),
]
