from django.urls import path

from .views import (
    generate_partner_api_key,
    secure_test
)

urlpatterns = [

    path(

        "partner/generate-key/<uuid:partner_id>/",

        generate_partner_api_key,

        name="generate-partner-api-key"

    ),

    path(

        "partner/test-auth/",

        secure_test,

        name="secure-test"

    ),

]