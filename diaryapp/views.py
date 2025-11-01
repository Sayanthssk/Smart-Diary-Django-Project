
import os
import subprocess
import tempfile
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from diaryapp.forms import *
from .models import *

class LoginView(View):
     def get(self,request):
        return render(request,'administration/login.html')
     
     def post(self,request):
         username = request.POST.get('Username')
         password = request.POST.get('Password')
         try:
             obj=LoginModel.objects.get(Username=username, Password=password)
             request.session['user_id'] = obj.id
             if obj.UserType == 'admin' :
                 return HttpResponse('''<script>alert("Login successful");window.location='/Homepage'</script>''')
             
             else:
                  return HttpResponse('''<script>alert("invalid user");window.location='/Homepage'</script>''')
         except LoginModel.DoesNotExist:
                  return HttpResponse('''<script>alert("invalid credentials ");window.location='/'</script>''')
             

class UserView(View):
     def get(self,request):
        c=UserModel.objects.all()
        return render(request,'administration/users.html',{'use':c})

class Deleteuser(View):
    def get(self, request,id):
        try:
            user = LoginModel.objects.get(id=id)
            user.delete()

            return HttpResponse('''<script>alert("user deleted successfully");window.location='/users'</script>''')
        except LoginModel.DoesNotExist:
            return HttpResponse('''<script>alert("user not found");window.location='/users'</script>''')             
             
 
     

class FeedbackView(View):
     def get(self,request):
        c=FeedbackModel.objects.all()
        return render(request,'administration/view_feedback.html',{'feed':c})
     
class DeleteFeed(View):
    def get(self, request,id):
        try:
            user = FeedbackModel.objects.get(id=id)
            user.delete()

            return HttpResponse('''<script>alert("ufeedback deleted successfully");window.location='/view_feedback'</script>''')
        except FeedbackModel.DoesNotExist:
            return HttpResponse('''<script>alert(feedback not found");window.location='/view_feedback'</script>''')             
             


class complaintsView(View):
    def get(self,request):
     a = complaintsModel.objects.all()
     return render(request,'administration/complaints_replay.html',{'complaint':a}) 
     
class ReplyView(View):
      def post(self,request,id):  
        c=complaintsModel.objects.get(id=id)    
        d=ReplyForm(request.POST,instance=c) 
        if d.is_valid():
            d.save()
            return redirect('/complaints_replay')
     
class Homepage(View):
     def get(self,request):
        return render(request,'administration/Homepage.html')
          
     


#///////////////////////////////////////////////////////api//////////////////////////////////////////#

from django.shortcuts import render
from .models import *
# Create your views here.
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *  
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

class UserReg_api(APIView):
    def post(self, request):
        print("###################", request.data)

        user_serial = User_Serializer(data=request.data)
        login_serial = Login_Serializer(data=request.data)

        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            login_profile = login_serial.save(UserType='USER')

            # Assign the login profile to the UserTable and save the UserTable
            user_serial.save(LOGINID=login_profile)

            # Return the serialized user data in the response
            return Response({'message':'Registration successful'}, status=status.HTTP_201_CREATED)

        return Response({
            'login_error': login_serial.errors if not login_valid else None,
            'user_error': user_serial.errors if not data_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginPageAPI(APIView):
    def post(self, request):
        print("####################")
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")
        print("$$$$$$$$$$$$$$",username)
        # Validate input

        if not username or not password:
            response_dict["message"] = "Invalid Username or Password"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginModel.objects.filter(Username=username, Password=password).first()
        print("%%%%%%%%%%%%%%%%%%%%", t_user)

        if not t_user:
            response_dict["message"] = "Credentials invalid please check Username and Password"
            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        else:
            response_dict["message"] = "success"
            response_dict["login_id"] = t_user.id
            response_dict["UserType"] = t_user.UserType

            return Response(response_dict, status=HTTP_200_OK)
        
# from textblob import TextBlob  
# from transformers import pipeline  # install: pip install transformers torch
# import re
# import speech_recognition as sr
# from pydub import AudioSegment
# import tempfile
# import os
# from io import BytesIO


# # -----------------------------
# # Initialize Emotion Analyzer
# # -----------------------------
# # Load emotion analysis model once
# emotion_analyzer = pipeline(
#     "text-classification",
#     model="j-hartmann/emotion-english-distilroberta-base",
#     return_all_scores=True
# )


# class AddDailyActivity(APIView):
#     def post(self, request, lid):
#         print("Incoming Data:", request.data)

#         # 1️⃣ Get the user
#         try:
#             user = UserModel.objects.get(LOGINID__id=lid)
#         except UserModel.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

#         # 2️⃣ Extract the description safely
#         description = ""
#         if "Description" in request.data:
#             desc_data = request.data["Description"]
#             if isinstance(desc_data, list):
#                 description = desc_data[0] if len(desc_data) > 0 else ""
#             elif isinstance(desc_data, str):
#                 description = desc_data
#         elif "transactions" in request.data:
#             tx = request.data.get("transactions", [])
#             if isinstance(tx, list) and len(tx) > 0:
#                 description = tx[0]
#             elif isinstance(tx, str):
#                 description = tx

#         print("Extracted description:", description)

#         # 3️⃣ Predict mood
#         mood = self.predict_mood(description)
#         print("Predicted mood:", mood)

#         # 4️⃣ Extract salary if present
#         salary_amount = self.extract_salary(description)
#         if salary_amount:
#             SalaryTable.objects.create(USERID=user, salary=salary_amount)
#             print(f"💰 Salary detected and saved: {salary_amount}")

#         # 5️⃣ Prepare data for saving activity
#         data = {
#             "Description": description,
#             "mood": mood,
#             "Title": request.data.get("Title", "Daily Log"),
#             "Day": request.data.get("Day", datetime.now().strftime("%d/%m/%Y"))
#         }

#         serializer = Activity_Serializer(data=data)
#         if serializer.is_valid():
#             serializer.save(USERID=user)
#             return Response({
#                 'message': "Activity added successfully",
#                 'predicted_mood': mood,
#                 'salary_detected': salary_amount
#             }, status=status.HTTP_200_OK)
#         else:
#             print("Serializer Errors:", serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # -----------------------------
#     # Emotion Prediction Logic
#     # -----------------------------
#     def predict_mood(self, text):
#         """Predict emotion using transformer model + rule-based refinement."""
#         if not isinstance(text, str) or not text.strip():
#             return "neutral"

#         text_lower = text.lower()

#         # Base model prediction
#         try:
#             results = emotion_analyzer(text)[0]
#             top_emotion = sorted(results, key=lambda x: x['score'], reverse=True)[0]
#             emotion = top_emotion['label']
#         except Exception as e:
#             print("Error in mood prediction:", str(e))
#             emotion = "neutral"

#         # 🎯 Custom rule-based refinement
#         positive_keywords = ["salary", "bonus", "jackpot", "promotion", "reward", "won", "winning", "gift"]
#         sad_keywords = ["loss", "fine", "penalty", "deducted", "tax", "lost", "less salary", "reduced", "cut", "unpaid"]
#         disappointment_keywords = ["only", "less", "just", "barely", "not enough", "little"]
#         negation_words = ["no", "not", "don't", "didn't", "never", "without", "cant", "cannot", "won't"]

#         # Check for negative emotions first
#         if any(word in text_lower for word in sad_keywords) or any(word in text_lower for word in disappointment_keywords):
#             emotion = "sad"
#         elif any(word in text_lower for word in positive_keywords):
#             # detect negation near positive keywords
#             if any(n in text_lower for n in negation_words):
#                 emotion = "sad"
#             else:
#                 emotion = "happy"

#         # Extra nuance for other emotions
#         if "angry" in text_lower or "irritated" in text_lower or "frustrated" in text_lower:
#             emotion = "angry"
#         elif "depressed" in text_lower or "hopeless" in text_lower:
#             emotion = "depressed"
#         elif "excited" in text_lower or "amazing" in text_lower or "great" in text_lower:
#             emotion = "excited"

#         return emotion


#     # -----------------------------
#     # Salary Extraction Logic
#     # -----------------------------
#     def extract_salary(self, text):
#         """Extract numeric salary from text."""
#         if not isinstance(text, str):
#             return None
#         pattern = r'\b(?:salary|bonus|jackpot|income|amount)\s*(?:is|was|of|=|:)?\s*(\d+(?:\.\d{1,2})?)\b'
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             try:
#                 return float(match.group(1))
#             except ValueError:
#                 return None
#         return None

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from transformers import pipeline
import whisper
import tempfile
import os
import re
from word2number import w2n  


# Initialize Emotion Analyzer once globally
emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

# Load Whisper model globally (for better speed)
whisper_model = whisper.load_model("base")


class AddDailyActivity(APIView):
    def get(self, request, lid):
        c = DailyActivities.objects.filter(USERID__LOGINID__id = lid)
        d = Activity_Serializer(c, many=True)
        return Response(d.data, status=HTTP_200_OK)
    
    def post(self, request, lid):
        print("Incoming Data:", request.data)

        # 1️⃣ Get the user
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Extract description safely
        description = ""
        if "Description" in request.data:
            desc_data = request.data["Description"]
            if isinstance(desc_data, list):
                description = desc_data[0] if len(desc_data) > 0 else ""
            elif isinstance(desc_data, str):
                description = desc_data
        elif "transactions" in request.data:
            tx = request.data.get("transactions", [])
            if isinstance(tx, list) and len(tx) > 0:
                description = tx[0]
            elif isinstance(tx, str):
                description = tx

        # 3️⃣ Handle voice file upload (if present)
        if "voice" in request.FILES:
            voice_file = request.FILES["voice"]
            print(f"🎙 Received voice file: {voice_file.name}")
            description = self.voice_to_text(voice_file)
            print(f"Converted text: {description}")

        print("Extracted description:", description)

        # 4️⃣ Predict mood
        mood = self.predict_mood(description)
        print("Predicted mood:", mood)

        # 5️⃣ Extract salary if present
        salary_amount = self.extract_salary(description)
        if salary_amount:
            try:
                # Get Day from frontend
                day_value = request.data.get("Day")
                if isinstance(day_value, list):
                    day_value = day_value[0]

                # Convert string date (e.g. "29/10/2025") to date object
                try:
                    day_obj = datetime.strptime(day_value, "%d/%m/%Y").date()
                except Exception:
                    day_obj = datetime.now().date()

                # ✅ Save salary info to database
                SalaryTable.objects.create(
                    USERID=user,
                    salary=salary_amount,
                    Description=description,
                    Day=day_obj
                )
                print(f"💰 Salary detected and saved: {salary_amount}")
            except Exception as e:
                  print("❌ Error saving salary record:", e)

        # 6️⃣ Prepare data for saving activity
        data = {
            "Description": description,
            "mood": mood,
            "Title": request.data.get("Title", "Daily Log"),
            "Day": request.data.get("Day", datetime.now().strftime("%d/%m/%Y"))
        }

        serializer = Activity_Serializer(data=data)
        if serializer.is_valid():
            serializer.save(USERID=user)
            return Response({
                'message': "Activity added successfully",
                'predicted_mood': mood,
                'salary_detected': salary_amount,
                'converted_text': description
            }, status=status.HTTP_200_OK)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # -----------------------------
    # 🎧 Whisper Voice-to-Text
    # -----------------------------
    def voice_to_text(self, voice_file):
        """Convert uploaded voice file (mp3/wav/webm/m4a) → English text using Whisper."""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(voice_file.name)[1]) as temp_audio:
                for chunk in voice_file.chunks():
                    temp_audio.write(chunk)
                temp_audio_path = temp_audio.name

            print("🎧 Whisper: Processing audio file", temp_audio_path)

            # Transcribe using Whisper (assume English speech)
            result = whisper_model.transcribe(
                temp_audio_path,
                task="transcribe",      # only transcribe (no translation)
                language="en"           # force English recognition
            )
            text = result.get("text", "").strip()
            print("🗣️ Whisper Transcription (English speech):", text)
            return text

        except Exception as e:
            print("❌ Whisper transcription failed:", e)
            return ""
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)



    # -----------------------------
    # 🎭 Emotion Prediction Logic
    # -----------------------------
    def predict_mood(self, text):
        """Predict emotion using transformer model + rule-based refinement."""
        if not isinstance(text, str) or not text.strip():
            return "neutral"

        text_lower = text.lower()

        # Base model prediction
        try:
            results = emotion_analyzer(text)[0]
            top_emotion = sorted(results, key=lambda x: x['score'], reverse=True)[0]
            emotion = top_emotion['label']
        except Exception as e:
            print("Error in mood prediction:", str(e))
            emotion = "neutral"

        # 🎯 Rule-based refinement
        positive_keywords = ["salary", "bonus", "jackpot", "promotion", "reward", "won", "winning", "gift"]
        sad_keywords = ["loss", "fine", "penalty", "deducted", "tax", "lost", "less salary", "reduced", "cut", "unpaid"]
        disappointment_keywords = ["only", "less", "just", "barely", "not enough", "little"]
        negation_words = ["no", "not", "don't", "didn't", "never", "without", "cant", "cannot", "won't"]

        if any(word in text_lower for word in sad_keywords) or any(word in text_lower for word in disappointment_keywords):
            emotion = "sad"
        elif any(word in text_lower for word in positive_keywords):
            if any(n in text_lower for n in negation_words):
                emotion = "sad"
            else:
                emotion = "happy"

        if any(w in text_lower for w in ["angry", "irritated", "frustrated"]):
            emotion = "angry"
        elif any(w in text_lower for w in ["depressed", "hopeless"]):
            emotion = "depressed"
        elif any(w in text_lower for w in ["excited", "amazing", "great"]):
            emotion = "excited"
        elif any(w in text_lower for w in ["fear", "afraid", "scared", "worried", "terrified", "nervous"]):
            emotion = "fear"

        return emotion


    # -----------------------------
    # 💰 Salary Extraction Logic
    # -----------------------------
    def extract_salary(self, text):
        """Extract numeric salary amount from text (supports lakh, crore, thousand, k, word-based numbers)."""
        if not isinstance(text, str):
            return None

        text = text.lower()

        # 1️⃣ Detect key salary phrases
        salary_pattern = r'\b(?:salary|package|income|bonus|credited|got|received)\b.*?\b([\w\s.,]+(?:lakh|lakhs|crore|crores|thousand|k)?)\b'
        match = re.search(salary_pattern, text, re.IGNORECASE)
        if not match:
            return None

        amount_str = match.group(1).strip().lower()
        amount_str = amount_str.replace(",", "")

        multiplier = 1
        if "lakh" in amount_str:
            multiplier = 100000
            amount_str = re.sub(r"lakh[s]?", "", amount_str)
        elif "crore" in amount_str:
            multiplier = 10000000
            amount_str = re.sub(r"crore[s]?", "", amount_str)
        elif "thousand" in amount_str:
            multiplier = 1000
            amount_str = re.sub(r"thousand", "", amount_str)
        elif "k" in amount_str:
            multiplier = 1000
            amount_str = re.sub(r"k", "", amount_str)

        amount_str = amount_str.strip()

        # 2️⃣ Try to convert word-based numbers (like "one", "fifty")
        try:
            # Try converting word to number (like "one lakh" → 1 * 100000)
            numeric_part = None
            try:
                numeric_part = w2n.word_to_num(amount_str)
            except Exception:
                # Fallback if number is already numeric (like "1", "50.5")
                numeric_part = float(re.findall(r"[\d.]+", amount_str)[0]) if re.findall(r"[\d.]+", amount_str) else None

            if numeric_part:
                salary_value = numeric_part * multiplier
                return salary_value
        except Exception as e:
            print("❌ Salary parse failed:", e)
            return None

        return None




        

class AddExpenceAPI(APIView):
    def post(self, request, lid):
        print("Incoming Data:", request.data)

        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = Expense_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(USERID=user)
            return Response({'message': "Added Successfully"}, status=status.HTTP_200_OK)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ViewExpensesApi(APIView):
    def get(self, request, lid):
        c = ExpenseTable.objects.filter(USERID__LOGINID__id=lid)
        ser = Expense_Serializer(c, many=True)
        return Response(ser.data, status=HTTP_200_OK)
    
    def delete(self, request, lid):
        try:
            c = ExpenseTable.objects.get(id=lid)
        except ExpenseTable.DoesNotExist:
            return Response({"error": "Expense not found"}, status=HTTP_400_BAD_REQUEST)
        c.delete()
        return Response({"message":"Deleted Successfully"}, status=HTTP_200_OK)
    
    def put(self, request, lid):
        print("Incoming data:", request.data)
        try:
            expense = ExpenseTable.objects.get(id=lid)
        except ExpenseTable.DoesNotExist:
            return Response({"error": "Expense not found"}, status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()

        day = data.get('Day')
        if day and "/" in day:
            try:
                data['Day'] = datetime.strptime(day, "%d/%m/%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use DD/MM/YYYY."}, status=HTTP_400_BAD_REQUEST)

        serializer = Expense_Serializer(expense, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Expense updated successfully", "data": serializer.data}, status=HTTP_200_OK)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

class ViewProfile(APIView):
    def get(self, request, lid):
        c = UserModel.objects.get(LOGINID__id = lid)
        ser = User_Serializer(c)
        return  Response(ser.data, status = HTTP_200_OK)
    def put(self, request, lid):
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = User_Serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

from django.db.models import Sum

class ViewIncome(APIView):
    def get(self, request, lid):
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        total_income = SalaryTable.objects.filter(
            USERID__LOGINID__id=lid
        ).aggregate(total=Sum('salary'))['total'] or 0

        total_expense = ExpenseTable.objects.filter(
            USERID__LOGINID__id=lid
        ).aggregate(total=Sum('Amount'))['total'] or 0

        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }, status=HTTP_200_OK)


class AddIncomeAPI(APIView):
    def post(self, request, lid):
        print("=======================>",request.data) 
        c = UserModel.objects.get(LOGINID__id = lid)
        d = IncomeSerializer(data=request.data)
        if d.is_valid():
            d.save(USERID=c)
            return Response({"message":"Income Added Successfully"}, status=HTTP_200_OK)
        

class ViewUserHistory(APIView):
    """
    📊 Fetch combined user history:
    - Daily Activities (mood tracking)
    - Salary entries
    - Expense entries
    """

    def get(self, request, lid):
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 🗓 Fetch data from each table
        salary_data = SalaryTable.objects.filter(USERID=user).order_by('-Day')
        expense_data = ExpenseTable.objects.filter(USERID=user).order_by('-Day')
        activity_data = DailyActivities.objects.filter(USERID=user).order_by('-Day')

        # 🧾 Serialize manually to keep it simple
        salary_list = [
            {
                "day": s.Day.strftime("%d/%m/%Y") if s.Day else None,
                "amount": s.salary,
                "description": s.Description,
            }
            for s in salary_data
        ]

        expense_list = [
            {
                "day": e.Day.strftime("%d/%m/%Y") if e.Day else None,
                "amount": e.Amount,
                "type": e.ExpenseType,
                "description": e.Description,
            }
            for e in expense_data
        ]

        activity_list = [
            {
                "day": a.Day.strftime("%d/%m/%Y") if a.Day else None,
                "mood": a.mood,
                "description": a.Description,
            }
            for a in activity_data
        ]

        # 📦 Combine everything under different keys
        response_data = {
            "salary_history": salary_list,
            "expense_history": expense_list,
            "activity_history": activity_list
        }

        print("📊 Combined history fetched successfully for user:", lid)
        return Response(response_data, status=status.HTTP_200_OK)
    

class ViewDailyActivityGraph(APIView):
    """
    📊 Return separate mood and description history for graph visualization
    """

    def get(self, request, lid):
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        activities = DailyActivities.objects.filter(USERID=user).order_by('Day')

        if not activities.exists():
            return Response({'message': 'No daily activities found'}, status=status.HTTP_200_OK)

        # 🎭 Convert moods to numeric values for charting
        mood_mapping = {
            'happy': 5,
            'excited': 4,
            'neutral': 3,
            'sad': 2,
            'angry': 1,
            'fear': 1.5,
            'depressed': 0.5
        }

        mood_graph = []
        description_graph = []

        for act in activities:
            date_str = act.Day.strftime("%Y-%m-%d") if act.Day else ""
            mood_text = act.mood if act.mood else "Unknown"
            mood_value = mood_mapping.get(mood_text.lower(), 0)
            description = act.Description if act.Description else ""

            # Separate data for both graphs
            mood_graph.append({
                "date": date_str,
                "mood": mood_text,
                "mood_value": mood_value
            })

            description_graph.append({
                "date": date_str,
                "description": description
            })

        response = {
            "mood_graph": mood_graph,
            "description_graph": description_graph
        }

        print(f"✅ Graph data for user {lid}: {response}")
        return Response(response, status=status.HTTP_200_OK)
    

# class AddReminder(APIView):
#     def post(self, request, lid):
#         print("Incoming Reminder Data:", request.data)

#         try:
#             user = UserModel.objects.get(LOGINID__id=lid)
#         except UserModel.DoesNotExist:
#             return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)

#         serializer = ReminderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(USERID=user)
#             return Response({"message": "Reminder Added Successfully"}, status=HTTP_200_OK)
#         else:
#             print("Serializer Errors:", serializer.errors)
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
#     def get(self, request, lid):
#         c = ReminderModel.objects.filter(USERID__LOGINID__id = lid)
#         serializer = ReminderSerializer(c, many=True)
#         print(serializer.data)
#         return Response(serializer.data, status=HTTP_200_OK)
    

class AddReminder(APIView):
    def post(self, request, lid):
        print("Incoming Reminder Data:", request.data)

        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)

        serializer = ReminderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(USERID=user)
            print("✅ Reminder added successfully")

            # 🧹 After adding, remove expired reminders automatically
            self.delete_expired_reminders(user)
            return Response({"message": "Reminder Added Successfully"}, status=HTTP_200_OK)

        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request, lid):
        try:
            user = UserModel.objects.get(LOGINID__id=lid)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)

        # 🧹 Before fetching, delete old reminders
        self.delete_expired_reminders(user)

        # ✅ Fetch current (active) reminders
        reminders = ReminderModel.objects.filter(USERID=user)
        serializer = ReminderSerializer(reminders, many=True)
        print("Active Reminders:", serializer.data)

        return Response(serializer.data, status=HTTP_200_OK)

    # 🧠 Helper function to delete expired reminders
    def delete_expired_reminders(self, user):
        now = datetime.now()
        expired = ReminderModel.objects.filter(USERID=user).filter(
            Date__lt=now.date()
        ) | ReminderModel.objects.filter(
            USERID=user, Date=now.date(), Time__lt=now.time()
        )
        deleted_count = expired.delete()[0]
        if deleted_count > 0:
            print(f"🧹 Deleted {deleted_count} expired reminders for user {user.id}")
            

class FeedBackAPI(APIView):
    def post(self, request, lid):
        c= UserModel.objects.get(LOGINID__id = lid)
        serializers = FeedbackSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save(USERID=c)
            return Response(serializers.data, status=HTTP_200_OK)
        
class ComplaintAPI(APIView):
    def get(self, request, lid):
        c = complaintsModel.objects.filter(USERID__LOGINID__id = lid)
        ser= ComplaintSerializer(c, many=True)
        return Response(ser.data, HTTP_200_OK)
    def post(self, request, lid):
        c = UserModel.objects.get(LOGINID__id = lid)
        ser = ComplaintSerializer(data=request.data)
        if ser.is_valid():
            ser.save(USERID = c)
            return Response({"message":"Complaint added successfully"}, status=HTTP_200_OK)