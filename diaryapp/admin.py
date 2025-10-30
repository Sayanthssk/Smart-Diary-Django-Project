from django.contrib import admin

from diaryapp.models import *

# Register your models here.

admin.site.register(LoginModel)
admin.site.register(UserModel)
admin.site.register(FeedbackModel)
admin.site.register(complaintsModel)
admin.site.register(DailyActivities)
admin.site.register(ExpenseTable)
admin.site.register(SalaryTable)
admin.site.register(ReminderModel)