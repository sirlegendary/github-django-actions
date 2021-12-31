from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path('create_board/', views.create_board, name='create_board'),
    path("<int:board_id>/delete_board/", views.delete_board, name="delete_board"),
    path("<int:board_id>/edit_board/", views.edit_board, name="edit_board"),
    path('<int:board_id>/board/', views.board, name='board'),
    # Create Board Items
    path('<int:board_id>/create_board_text/', views.create_board_text, name='create_board_text'),
    path('<int:board_id>/create_sticky_note/', views.create_sticky_note, name='create_sticky_note'),
    path('<int:board_id>/create_url/', views.create_url, name='create_url'),
    path('<int:board_id>/upload_image/', views.upload_image, name='upload_image'),
    path('<int:board_id>/upload_video/', views.upload_video, name='upload_video'),
    # Delete Board Items
    path('<int:board_text_id>/delete_board_text/', views.delete_board_text, name='delete_board_text'),
    path('<int:note_id>/delete_sticky_note/', views.delete_sticky_note, name='delete_sticky_note'),
    path('<int:url_id>/delete_url/', views.delete_url, name='delete_url'),
    path('<int:image_id>/delete_image/', views.delete_image, name='delete_image'),
    path('<int:video_id>/delete_video/', views.delete_video, name='delete_video'),
    # Edit Board Items
    path('<int:bt_id>/edit_board_text/', views.edit_board_text, name='edit_board_text'),
    path('<int:link_id>/edit_url/', views.edit_url, name='edit_url'),
    path('<int:note_id>/edit_sticky_note/', views.edit_sticky_note, name='edit_sticky_note')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)