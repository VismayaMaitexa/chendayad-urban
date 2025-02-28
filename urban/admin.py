from django.contrib import admin

from .models import Consumer,Cart,Booking,Payment,Services,Worker,Chatmodel,Workerabout,Contractor,Feedback,Advertisement,Adpayment,CServices,Chats,Contractorabout,Notification
# Register your models here.

admin.site.register(Consumer)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Worker)
admin.site.register(Chatmodel)
admin.site.register(Workerabout)
admin.site.register(Contractor)
admin.site.register(Feedback)
admin.site.register(Advertisement)
admin.site.register(Adpayment)
admin.site.register(CServices)
admin.site.register(Chats)
admin.site.register(Contractorabout)
admin.site.register(Notification)
admin.site.register(Cart)
admin.site.register(Services)

