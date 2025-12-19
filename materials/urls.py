from django.urls import path

from materials.views import MaterialDataTableView, MaterialListView

urlpatterns = [
    path("lista-materiales", MaterialListView.as_view(), name="materials_list"),
    path("datatable/", MaterialDataTableView.as_view(), name="materials_datatable"),
]
