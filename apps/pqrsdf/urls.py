from django.urls import path
from .views import createPqrsdf, GetPqrsdfs, updatePqrsdf, deletePqrsdf
urlpatterns = [
    path('create_pqrsdf/', createPqrsdf, name="create_pqrsdf"),
    path('get_pqrsdfs/', GetPqrsdfs.as_view(), name="get_pqrsdfs"),
    path('update_pqrsdf/<int:id>', updatePqrsdf, name="update_pqrsdf"),
    path('delete_pqrsdf/<int:id>', deletePqrsdf, name="delete_pqrsdf")
]
