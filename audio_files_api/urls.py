from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
import audio_files_api.views


router = DefaultRouter()


urlpatterns = [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    
    # API endpoint for listing Songs/Podcasts/Audiobooks
    path('<str:audioFileType>/', audio_files_api.views.AudioViewSet.as_view({'get': 'list','post':'create'}), name='audio_file_create_list'),
    
    # API endpoint for retrieving, Updating and Deleting Songs/Podcasts/Audiobooks
    path('<str:audioFileType>/<int:pk>/',  audio_files_api.views.AudioViewSet.as_view( {'get': 'retrieve', 'put':'update', 'delete':'destroy'} ) , name='audio_file_rud'),

    # API endpoint for Uploading or Creating Songs/Podcasts/Audiobooks
    path('upload_audio/', audio_files_api.views.AudioViewSet.as_view({'post':'create'}), name='audio_file_create'),

    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Audio Server",
        description="API for AUDIO SERVER",
        version="0.0.1"
    ), name='openapi-schema'),

    path('', include(router.urls)),
]
