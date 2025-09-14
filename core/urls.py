from django.urls import path
from django.shortcuts import redirect
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", lambda request: redirect("register")),
    path("login/",views.login,name="login"),
    path("home/",views.home,name="home"),
    path("profile/",views.profile,name="profile"),
    path("upload_prescription/", views.upload_prescription, name="upload_prescription"),
    path('upload_prescription/download/<int:file_id>/', views.download_prescription, name="download_prescription"),
    path('upload_prescription/preview/<int:file_id>/', views.preview_prescription, name="preview_prescription"),
    path("upload_xray/",views.upload_xray,name="upload_xray"),
    path("xray/preview/<int:file_id>/", views.xray_preview, name="xray_preview"),
    path("xray/download/<int:file_id>/", views.xray_download, name="xray_download"),
    path("upload_bloodtests/",views.upload_bloodtests,name="upload_bloodtests"),
    path("bloodtest/preview/<int:file_id>/", views.bloodtest_preview, name="bloodtest_preview"),
    path("bloodtest/download/<int:file_id>/", views.bloodtest_download, name="bloodtest_download"),
    path("logout/",views.logout,name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


