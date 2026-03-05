from django.urls import path
from . import views

urlpatterns = [
    path("", views.pledge_page, name="pledge"),
    path(
        "thankyou_page/<int:pledgeCreateObj_id>/<int:pledge_id>/",
        views.thankyou_page,
        name="thankyou"
    ),    
    path("pledge_list/", views.pledgeList, name="pledges" ),
    path("pledge_view/<int:id>/", views.pledgeView, name="pledgeview"),
    path("pledge/pdf/<int:id>/", views.generate_pdf, name="generate_pdf"),

    path("admin_list/", views.adminList, name="admins" ),
    path("admin_create/", views.adminCreate, name="admin_create" ),
    path("admin_store/", views.create_user, name="admin_store" ),

    path("login/", views.login_page, name="login_page"),
    path("login_submit/", views.login_view, name="checking_credentials"),
    path("logout/", views.logout_view, name="profile_logout"),

    path("pledge_create/", views.pledgeCreatePage, name="pledge_create"),
    path("pledge_store/", views.pledgeStore, name="pledgestore"),
    path("backend_pledges/", views.backendPledgeList, name="backend_pledges"),
    path("backend_pledges_view/<int:id>/", views.backendPledgeView, name="backend_pledge_view"),
    path("backend_pledges_update/<int:id>/", views.backendPledgeUpdate, name="backend_pledge_update"),
    path("backend_pledges_update_fun/<int:id>/", views.pledgeUpdateFun, name="backend_pledges_update_fun"),
    
path("download-certificate/<int:pledge_id>/", views.download_certificate, name="download_certificate"),
]