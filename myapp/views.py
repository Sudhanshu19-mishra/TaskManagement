from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import *
from .serializer import Adminserializer,Staffserializer,ClientSerializer,TaskSerializer,IncomeTaxSerializer,GstSerializer,KycSerializer,TdsSerializer,OtherDocsSerializer


# ✅ Login API

class AdminLogin(APIView):
    
    def get(self, request, pk=None):
        if pk:
            admin = Admin.objects.filter(pk=pk).first()
            if admin:
                serializer = Adminserializer(admin)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=200)
            else:
                return Response({
                    "status": "error",
                    "message": "Admin not found."
                }, status=404)
        else:
            admins = Admin.objects.all()
            serializer = Adminserializer(admins, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=200)

    def post(self, request):
        email = request.data.get('Email', '').strip().lower()
        password = request.data.get('Password', '').strip()

        if not email:
            return Response({"status": "error", "field": "email", "message": "Email is required."}, status=400)

        if not password:
            return Response({"status": "error", "field": "password", "message": "Password is required."}, status=400)

        admin = Admin.objects.filter(Email=email).first()

        if not admin:
            return Response({
                "status": "error",
                "field": "email",
                "message": "Invalid email."
            }, status=401)

        if admin.Password != password:
            return Response({
                "status": "error",
                "field": "password",
                "message": "Incorrect password."
            }, status=401)

        return Response({
            "status": "success",
            "message": "Login successful.",
            "data": {
                "id": admin.id, 
                "Email": admin.Email,
                "Password": admin.Password
            }
        }, status=200)

 
    
        

class StaffViews(APIView):

    def get(self, request, pk=None):
        if pk:
            staf = Staff.objects.filter(pk=pk).first()
            if staf:
                serializer = Staffserializer(staf)
                return Response({"status": "success", "data": serializer.data})
            return Response({"status": "error", "message": "Staff not found"}, status=404)

        staf = Staff.objects.all().order_by('-pk')
        serializer = Staffserializer(staf, many=True)
        return Response({'status': "success", "data": serializer.data})
    def post(self, request):
        serializer = Staffserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        
        staf = Staff.objects.filter(pk=pk).first()
        if not staf:
            return Response({"status": "error", "message": "Staff not found"}, status=404)

        serializer = Staffserializer(staf, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)

        staf = Staff.objects.filter(pk=pk).first()
        if not staf:
            return Response({"status": "error", "message": "Staff not found"}, status=404)

        staf.delete()
        return Response({"status": "deleted", "message": "Staff was deleted successfully"})
    

# stafflogin

class StaffLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '').strip()

        if not email:
            return Response({"status": "error", "field": "email", "message": "Email is required."}, status=400)

        if not password:
            return Response({"status": "error", "field": "password", "message": "Password is required."}, status=400)

        staff = Staff.objects.filter(email=email).first()

        if not staff:
            return Response({"status": "error", "field": "email", "message": "Invalid email."}, status=401)

        if staff.password != password:
            return Response({"status": "error", "field": "password", "message": "Incorrect password."}, status=401)

        # Successful login
        return Response({
            "status": "success",
            "message": "Login successful.",
            "data": {
                "id":staff.id,
                "name": staff.name,
                "email": staff.email,
                "mobile_No": staff.mobile_No
            }
        }, status=200)



# client views

    
class ClientView(APIView):
    def get(self, request, pk=None):
        if pk:
            client = Client.objects.filter(pk=pk).first()
            if not client:
                return Response({"status": "error", "message": "Client not found"}, status=404)
            serializer = ClientSerializer(client)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=200)
        else:
            clients = Client.objects.all().order_by('-pk')
            serializer = ClientSerializer(clients, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=200)
    def post(self, request):
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request, pk):
        client = Client.objects.filter(pk=pk).first()
        if not client:
            return Response({"error": "Client not found"}, status=404)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method 
    def delete(self, request, pk):
        client = Client.objects.filter(pk=pk).first()
        if not client:
            return Response({"error": "Client not found"}, status=404)
        client.delete()
        return Response({"message": "Client deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class ClientAPIView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '').strip()

        if not email:
            return Response({"status": "error", "field": "email", "message": "Email is required."}, status=400)

        if not password:
            return Response({"status": "error", "field": "password", "message": "Password is required."}, status=400)

        client = Client.objects.filter(email=email).first()  # Adjust model name if needed

        if not client:
            return Response({"status": "error", "field": "email", "message": "Invalid email."}, status=401)

        if client.password != password:
            return Response({"status": "error", "field": "password", "message": "Incorrect password."}, status=401)

        return Response({
            "status": "success",
            "message": "Login successful.",
            "data": {
                "id": client.id, 
                "email": client.email,
                
                "name": getattr(client, 'name', '')  # if you add a 'name' field later
            }
        }, status=200)
    



class TaskAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():  # ✅ this is important (with parentheses)
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({"status": "success", "message": "Task deleted"}, status=status.HTTP_200_OK)




class IncomeTaxAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            tax = IncomeTax.objects.filter(pk=pk).first()
            if not tax:
                return Response({"status": "error", "message": "IncomeTax record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = IncomeTaxSerializer(tax)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        taxes = IncomeTax.objects.all().order_by('-pk')
        serializer = IncomeTaxSerializer(taxes, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IncomeTaxSerializer(data=request.data)
        if serializer.is_valid():
            income_tax = serializer.save()
            return Response({"status": "success", "data": IncomeTaxSerializer(income_tax).data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        
        tax = IncomeTax.objects.filter(pk=pk).first()
        if not tax:
            return Response({"status": "error", "message": "IncomeTax record not found"}, status=404)

        serializer = IncomeTaxSerializer(tax, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)

        tax = IncomeTax.objects.filter(pk=pk).first()
        if not tax:
            return Response({"status": "error", "message": "IncomeTax record not found"}, status=404)

        tax.delete()
        return Response({"status": "success", "message": "IncomeTax record deleted successfully"}, status=204)



class GstAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            gst = Gst.objects.filter(pk=pk).first()
            if not gst:
                return Response({"status": "error", "message": "GST record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = GstSerializer(gst)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        gsts = Gst.objects.all().order_by('-pk')
        serializer = GstSerializer(gsts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GstSerializer(data=request.data)
        if serializer.is_valid():
            gst = serializer.save()
            return Response({"status": "success", "data": GstSerializer(gst).data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        
        gst = Gst.objects.filter(pk=pk).first()
        if not gst:
            return Response({"status": "error", "message": "GST record not found"}, status=404)

        serializer = GstSerializer(gst, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)

        gst = Gst.objects.filter(pk=pk).first()
        if not gst:
            return Response({"status": "error", "message": "GST record not found"}, status=404)

        gst.delete()
        return Response({"status": "success", "message": "GST record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class KycAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            kyc = Kyc.objects.filter(pk=pk).first()
            if not kyc:
                return Response({"status": "error", "message": "Kyc record not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = KycSerializer(kyc)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        kycs = Kyc.objects.all().order_by('-pk')
        serializer = KycSerializer(kycs, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = KycSerializer(data=request.data)
        if serializer.is_valid():
            kyc = serializer.save()
            return Response({"status": "success", "data": KycSerializer(kyc).data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        
        kyc = Kyc.objects.filter(pk=pk).first()
        if not kyc:
            return Response({"status": "error", "message": "Kyc record not found"}, status=404)

        serializer = KycSerializer(kyc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)

        kyc = Kyc.objects.filter(pk=pk).first()
        if not kyc:
            return Response({"status": "error", "message": "Kyc record not found"}, status=404)

        kyc.delete()
        return Response({"status": "success", "message": "Kyc record deleted successfully"}, status=204)



class TdsAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            tds = Tds.objects.filter(pk=pk).first()
            if not tds:
                return Response({"status": "error", "message": "TDS record not found"}, status=404)
            serializer = TdsSerializer(tds)
            return Response({"status": "success", "data": serializer.data})
        tds_list = Tds.objects.all().order_by('-pk')
        serializer = TdsSerializer(tds_list, many=True)
        return Response({"status": "success", "data": serializer.data})

    def post(self, request):
        serializer = TdsSerializer(data=request.data)
        if serializer.is_valid():
            tds = serializer.save()
            return Response({"status": "success", "data": TdsSerializer(tds).data}, status=201)
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        tds = Tds.objects.filter(pk=pk).first()
        if not tds:
            return Response({"status": "error", "message": "TDS record not found"}, status=404)
        serializer = TdsSerializer(tds, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)
        tds = Tds.objects.filter(pk=pk).first()
        if not tds:
            return Response({"status": "error", "message": "TDS record not found"}, status=404)
        tds.delete()
        return Response({"status": "success", "message": "TDS record deleted successfully"}, status=204)





class OtherDocsAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            doc = OtherDoc.objects.filter(pk=pk).first()
            if not doc:
                return Response({"status": "error", "message": "Document not found"}, status=404)
            serializer = OtherDocsSerializer(doc)
            return Response({"status": "success", "data": serializer.data})
        all_docs = OtherDoc.objects.all().order_by('-pk')
        serializer = OtherDocsSerializer(all_docs, many=True)
        return Response({"status": "success", "data": serializer.data})

    def post(self, request):
        serializer = OtherDocsSerializer(data=request.data)
        if serializer.is_valid():
            doc = serializer.save()
            return Response({"status": "success", "data": OtherDocsSerializer(doc).data}, status=201)
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for patch"}, status=400)
        doc = OtherDoc.objects.filter(pk=pk).first()
        if not doc:
            return Response({"status": "error", "message": "Document not found"}, status=404)
        serializer = OtherDocsSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "Primary key (pk) is required for delete"}, status=400)
        doc = OtherDoc.objects.filter(pk=pk).first()
        if not doc:
            return Response({"status": "error", "message": "Document not found"}, status=404)
        doc.delete()
        return Response({"status": "success", "message": "Document deleted successfully"}, status=204)
