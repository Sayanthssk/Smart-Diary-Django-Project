from django.urls import path, include

from diaryapp.views import *

urlpatterns = [
 path('',LoginView.as_view(), name='LoginView'),
 path('users',UserView.as_view(), name='users'),
 path('view_feedback',FeedbackView.as_view(), name='view_feedback'),
 path('complaints_replay',complaintsView.as_view(), name='complaints_replay'),
 path('Homepage',Homepage.as_view(), name='Homepage'),
 path('Deleteuser/<int:id>',Deleteuser.as_view(), name='Deleteuser'),
 path('DeleteFeed/<int:id>',DeleteFeed.as_view(), name='DeleteFeed'),
path('ReplyView/<int:id>',ReplyView.as_view(), name='ReplyView'),




    path('api/usereg/', UserReg_api.as_view()),
    path('api/login/', LoginPageAPI.as_view()),
    path('api/verify_otp/', VerifyOTPAPI.as_view()),
    path('api/dailyactivities/<int:lid>', AddDailyActivity.as_view()),
    path('api/expense/<int:lid>', AddExpenceAPI.as_view()),
    path('api/viewexpense/<int:lid>', ViewExpensesApi.as_view()),
    path('api/profile/<int:lid>', ViewProfile.as_view()),
    path('api/viewincome/<int:lid>', ViewIncome.as_view()),
    path('api/income/<int:lid>', AddIncomeAPI.as_view()),
    path('api/histories/<int:lid>', ViewUserHistory.as_view()),
    path('api/viewactivitygraph/<int:lid>/', ViewDailyActivityGraph.as_view()),
    path('api/reminders/<int:lid>', AddReminder.as_view()),
    path('api/feedback/<int:lid>', FeedBackAPI.as_view()),  
    path('api/complaint/<int:lid>', ComplaintAPI.as_view()),
    path('api/deletedailyactivities/<int:id>', DeleteEntries.as_view()),
    path('api/daily_summary/<int:user_id>', DailySummary.as_view()),
    path('api/daily_summary/<int:user_id>/', DailySummary.as_view()),

]
