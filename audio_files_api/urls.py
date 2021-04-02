from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
import audio_files_api.views


router = DefaultRouter()

#RUD-able APIs
# router.register(r'<str:audioFileType>', audio_files_api.views.AudioViewSet, basename='audio_files')


urlpatterns = [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    
    path('<str:audioFileType>/', audio_files_api.views.AudioViewSet.as_view({'get': 'list', 'post':'list'}), name='audio_file_create_list'),
    path('<str:audioFileType>/<int:pk>/',  audio_files_api.views.AudioViewSet.as_view( {'get': 'retrieve', 'post':'update', 'delete':'destroy'} ) , name='audio_file_rud'),

    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Audio Server",
        description="API for CRUDing community artifacts.",
        version="0.0.1"
    ), name='openapi-schema'),

    path('', include(router.urls)),
]
