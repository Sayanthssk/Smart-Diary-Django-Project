from django.forms import ModelForm
from diaryapp.models import complaintsModel


class ComplaintsForm(ModelForm):
    class Meta:
        model=complaintsModel
        fields=['Complaint','Reply'] 

class ReplyForm(ModelForm):
    class Meta:
        model=complaintsModel
        fields=['Reply']          