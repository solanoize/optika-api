from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from optika.models import Order


def print_order(request, pk):
    order = Order.objects.get(pk=pk)
    # logic print / pdf / dll
    return HttpResponse("Printed!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/<int:pk>/print/', admin.site.admin_view(print_order), name='order_print'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/optika/', include('optika.urls', namespace='optika')),
]
