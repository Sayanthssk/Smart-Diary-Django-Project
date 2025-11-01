from diaryapp.models import *
from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers 


class Login_Serializer(ModelSerializer):
    class Meta:
        model = LoginModel
        fields = '__all__'

class User_Serializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

from datetime import datetime


class Activity_Serializer(ModelSerializer):
    class Meta:
        model = DailyActivities
        fields = '__all__'

    def to_internal_value(self, data):
        mutable_data = data.copy()

        day = mutable_data.get('Day')
        if day:
            try:
                mutable_data['Day'] = datetime.strptime(day, "%d/%m/%Y").date()
            except ValueError:
                pass

        return super().to_internal_value(mutable_data)


class Expense_Serializer(ModelSerializer):
    class Meta:
        model = ExpenseTable
        fields = '__all__'
        
    def to_internal_value(self, data):
        mutable_data = data.copy()

        day = mutable_data.get('Day')
        if day:
            try:
                mutable_data['Day'] = datetime.strptime(day, "%d/%m/%Y").date()
            except ValueError:
                pass

        return super().to_internal_value(mutable_data)


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = SalaryTable
        fields = "__all__"


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = ReminderModel
        fields = "__all__"

    def to_internal_value(self, data):
        mutable_data = data.copy()

        # Handle date conversion if needed
        day = mutable_data.get('Date')
        if day:
            try:
                # Try parsing standard date (yyyy-mm-dd or dd/mm/yyyy)
                if "-" in day:
                    mutable_data['Date'] = datetime.strptime(day, "%Y-%m-%d").date()
                else:
                    mutable_data['Date'] = datetime.strptime(day, "%d/%m/%Y").date()
            except ValueError:
                pass

        # Handle time conversion like "4:02 PM"
        time_str = mutable_data.get('Time')
        if time_str:
            try:
                # Convert 12-hour time to 24-hour
                time_obj = datetime.strptime(time_str.strip(), "%I:%M %p").time()
                mutable_data['Time'] = time_obj
            except ValueError:
                # If already valid format, keep it
                pass

        return super().to_internal_value(mutable_data)
    

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = "__all__"

class ComplaintSerializer(ModelSerializer):
    class Meta:
        model = complaintsModel
        fields = "__all__"