"""event_join URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

import events_app.views as events_views
import participants_app.views as part_views


# router = DefaultRouter()
# router.register(r'events', events_views.EventsViewSet, basename='events')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', events_views.Main.as_view(), name='main'),
    path('events/', events_views.EventsListView.as_view(), name='events-list'),
    path('events/<int:event_id>/', events_views.EventDetailsView.as_view(), name='events-details'),
    path('events/add-event/', events_views.AddEventView.as_view(), name='add-event'),
    path('events/register/<int:pk>/', part_views.RegisterView.as_view(), name='register'),
    path('participant/email/<confirmation_uuid>/', part_views.ConfirmEmailView.as_view(), name='email-confirmed'),
    path('login/', events_views.LoginView.as_view(), name='login'),
    path('participant/invite/<answer_id>/', part_views.AnswerInvite.as_view(), name='accept-invite'),
    path('logout/', events_views.LogoutView.as_view(), name='logout'),
    path('events/search/', events_views.SearchEventView.as_view(), name='search-view'),
    # path('error/', events_views.TestError.as_view()),
    # # path('', include(router.urls)),
]

handler404 = events_views.error_404_view
