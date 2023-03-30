from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CreatePqrsdf, GetPqrsdfs, UpdatePqrsdf, DeletePqrsdf, DetailPqrsdf, UpdateState
urlpatterns = [
    path('create_pqrsdf/', login_required(CreatePqrsdf.as_view()),
         name="create_pqrsdf"),
    path('get_pqrsdfs/', login_required(GetPqrsdfs.as_view()), name="get_pqrsdfs"),
    path('detail_pqrsdf/<int:pk>', login_required(DetailPqrsdf.as_view()),
         name="detail_pqrsdf"),
    path('detail_pqrsdf/<int:pk>/update_state', login_required(UpdateState.as_view()),
         name="update_state"),
    path('update_pqrsdf/<int:pk>',
         login_required(UpdatePqrsdf.as_view()), name="update_pqrsdf"),
    path('delete_pqrsdf/<int:pk>',
         login_required(DeletePqrsdf.as_view()), name="delete_pqrsdf")
]
