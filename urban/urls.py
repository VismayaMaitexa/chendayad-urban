from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',views.home_view,name='home'),

    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),

    path('adminlogin', LoginView.as_view(template_name='owner/admin_login.html'),name='adminlogin'),

    path('afterlogin',views.afterlogin_view,name='afterlogin'),
    path('accounts/profile/',views.afterlogin_view,name='accounts/profile/'),

    path('admin-dashboard',views.admin_dashboard_view,name='admin-dashboard'),

    path('worker-request',views.worker_request_view,name='worker-request'),
    path('approve-worker/<int:pk>',views.approve_worker_view,name='approve-worker'),
    path('admin-approve-worker',views.admin_approve_worker,name='admin-approve-worker'),
    path('reject-worker/<int:pk>',views.reject_worker_view,name='reject-worker'),

    path('manage-worker',views.manage_worker_view,name='manage-worker'),
    path('update-worker/<int:pk>',views.update_worker_view,name='update-worker'),
    path('delete-worker/<int:pk>',views.delete_worker_view,name='delete-worker'),

    path('manage-consumer',views.manage_consumer_view,name='manage-consumer'),
    path('update-consumer/<int:pk>',views.update_consumer_view,name='update-consumer'),
    path('delete-consumer/<int:pk>',views.delete_consumer_view,name='delete-consumer'),
    path('workerlogin',views.login_view,name='workerlogin'),
    path('worker-signup',views.worker_signup_view,name='worker-signup'),

    path('worker-dashboard',views.worker_dashboard_view,name='worker-dashboard'),
    path('worker-profile',views.worker_profile_view,name='worker-profile'),

    path('services',views.services_view,name='services'),
    path('update-service/<int:pk>',views.update_services_view,name='update-service'),
    path('delete-service/<int:pk>',views.delete_service_view,name='delete-service'),

    path('bookings',views.bookings_view,name='bookings'),
    path('approve-booking/<int:pk>',views.approve_booking_view,name='approve-booking'),
    path('reject-booking/<int:pk>',views.reject_booking_view,name='reject-booking'),
    #  path('consumerlogin',views.login_view,name='consumerlogin'),
    path('consumer-signup',views.consumer_signup_view,name='consumer-signup'),

    path('consumer-dashboard',views.consumer_dashboard_view,name='consumer-dashboard'),
    path('consumer-profile',views.consumer_profile_view,name='consumer-profile'),
    path('search',views.search_view,name='search'),
    path('csearch',views.csearch_view,name='csearch'),


    path('add-to-cart/<int:pk>',views.add_to_cart_view,name='add-to-cart'),
    path('cart',views.cart_view,name='cart'),
    path('remove-service-from-cart/<int:pk>',views.remove_service_from_cart,name='remove-service-from-cart'),
    
    # path('consumer-address',views.consumer_address_view,name='consumer-address'),
    # path('payment-success',views.payment_success_view,name='payment-success'),
    path('consumer-address', views.consumer_address_view,name='consumer-address'),
    path('payment', views.payment_view,name='payment'),

    path('payment-success', views.payment_success_view,name='payment-success'),

    path('my-bookings',views.my_bookings_view,name='my-bookings'),
    path('delete-booking/<int:pk>',views.delete_booking_from_mybookings,name='delete-booking'),
    path('consumerlogin',LoginView.as_view(template_name='consumer/consumer_login.html'),name='consumerlogin'),
    path('consumer-signup',views.consumer_signup_view,name='consumer-signup'),

    path('consumer-dashboard',views.consumer_dashboard_view,name='consumer-dashboard'),
    path('consumer-profile',views.consumer_profile_view,name='consumer-profile'),
    path('search',views.search_view,name='search'),

    path('add-to-cart/<int:pk>',views.add_to_cart_view,name='add-to-cart'),
    path('cart',views.cart_view,name='cart'),
    path('remove-service-from-cart/<int:pk>',views.remove_service_from_cart,name='remove-service-from-cart'),
    
    # path('consumer-address',views.consumer_address_view,name='consumer-address'),
    # path('payment-success',views.payment_success_view,name='payment-success'),
    path('consumer-address', views.consumer_address_view,name='consumer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),

    path('my-bookings',views.my_bookings_view,name='my-bookings'),
    path('delete-booking/<int:pk>',views.delete_booking_from_mybookings,name='delete-booking'),

    path('amountpay<int:booking_id>/',views.amountpay_view,name='amountpay'),
    path('pay-success/<int:id>/',views.paysuccess_view,name='pay-success'),
    path('view-payment/',views.view_payment_details,name='view-payment'),
    path('singlepayment/',views.singlepayment_view,name='singlepayment'),
    path('payment-details/<int:worker_id>/',views.worker_payment_details,name='payment_details'),
    path('chat/<int:rec_id>/',views.chat,name='chat'),
    path('chat_message/<int:receiverid>/',views.chat_message,name='chat_message'),
    path('contractor-dashboard/',views.contractor_dashboard_view,name='contractor-dashboard'),
    path('workerabout',views.workerabout_view,name='workerabout'),
    path('aboutinfo/<int:worker_id>/',views.aboutinfo_view,name='aboutinfo'),
    path('contractor_register/',views.contractor_register, name='contractor_register'),

    path('contractor-request',views.contractor_request_view,name='contractor-request'),
    path('approve-contractor/<int:pk>',views.approve_contractor_view,name='approve-contractor'),
    path('admin-approve-contractor',views.admin_approve_contractor,name='admin-approve-contractor'),
    path('reject-contractor/<int:pk>',views.reject_contractor_view,name='reject-contractor'),

    path('manage-contractor',views.manage_contractor_view,name='manage-contractor'),
    path('update-contractor/<int:pk>',views.update_contractor_view,name='update-contractor'),
    path('delete-contractor/<int:pk>',views.delete_contractor_view,name='delete-contractor'),
    path('location/<int:re_id>/',views.location,name='location'),

    path('contractorlogin/',views.contractor_login, name='contractorlogin'),
    path('contractorwaiting/',views.contractor_waiting, name='contractor_waiting'),

    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback-list/', views.feedback_list, name='feedback_list'), 

    
    path('advertisement/create/', views.advertisement_create, name='advertisement_create'),
    path('contractor/advertisements/', views.contractor_advertisement_list, name='contractor_advertisement_list'),
    path('contractor/advertisement/approve/<int:pk>/', views.approve_advertisement, name='approve_advertisement'),   
    path('contractor/payment/add/', views.add_payment, name='contractor-add-payment'),  # Contractor adding payment
    path('admin-payment-list/', views.admin_payment_list, name='admin-payment-list'), 


    path('contractor-dashboard/cservices',views.cservices_view,name='cservices'),
    path('update-cservice/<int:pk>',views.update_cservices_view,name='update-cservice'),
    path('delete-cservice/<int:pk>',views.delete_cservice_view,name='delete-cservice'),


    path('chats/<int:chat_id>/',views.chats,name='chats'),
    path('chats_message/<int:receiver_id>/',views.chats_message,name='chats_message'),
    path('contractor/<int:contractor_id>/all_consumers/', views.all_consumers, name='all_consumers'),


    
    path('contractorabout', views.contractorabout_view, name='contractorabout'),
    path('contaboutinfo/<int:contractor_id>/', views.contaboutinfo_view, name='contaboutinfo'),
    path('approved-ads/', views.approved_ads_view, name='approved_ads'),


    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('editinfo/<int:pk>',views.editinfo_view,name='editinfo'),
    path('add-notification/', views.add_notification, name='add_notification'),  # New URL for adding notification
    path('contractor/notifications/', views.contractor_notifications, name='contractor-notifications'),
    path('complete', views.completes, name='complete'),
    path('contractor-complete', views.contractor_complete, name='contractor-complete'),

    path('password_reset/',views.password_reset, name='password_reset'),

    path('verify_otp/<int:otp_id>/',views.verify_otp, name='verify_otp'),
    path('set_new_password/<int:pk>/',views.set_new_password, name='set_new_password'),


]
