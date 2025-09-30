from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from rest_framework.parsers import JSONParser ,MultiPartParser, FormParser
from .models import *
from .serializer import *

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




class ClientView(APIView):
    def get(self, request, pk=None):
        if pk:
            client = Client.objects.filter(pk=pk).first()
            if not client:
                return Response({"status": "error", "message": "Client not found"}, status=404)
            serializer = ClientSerializer_add(client)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=200)
        else:
            clients = Client.objects.all().order_by('-pk')
            serializer = ClientSerializer_add(clients, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=200)
    def post(self, request):
            serializer = ClientSerializer_add(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        client = Client.objects.filter(pk=pk).first()
        if not client:
            return Response({"error": "Client not found"}, status=404)
        serializer = ClientSerializer_add(client, data=request.data, partial=True)
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
                "name": getattr(client, 'name', '')
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

        tasks = Task.objects.all().order_by('-pk')
        serializer = TaskSerializer(tasks, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
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







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import KycSerializer
import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser


class KycAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        if pk:
            kyc = get_object_or_404(Kyc, pk=pk)
            serializer = KycSerializer(kyc)
            return Response({"status": "success", "data": serializer.data})

        kycs = Kyc.objects.all().order_by('-pk')
        serializer = KycSerializer(kycs, many=True)
        return Response({"status": "success", "data": serializer.data})

    def post(self, request):
        serializer = KycSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            kyc = serializer.save()
            return Response({"status": "success", "data": KycSerializer(kyc).data},
                          status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors},
                      status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "KYC ID required"},
                          status=status.HTTP_400_BAD_REQUEST)

        kyc = get_object_or_404(Kyc, pk=pk)
        serializer = KycSerializer(kyc, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})

        return Response({"status": "error", "errors": serializer.errors},
                      status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "KYC ID required"},
                          status=status.HTTP_400_BAD_REQUEST)

        kyc = get_object_or_404(Kyc, pk=pk)

        partner_index = request.query_params.get('partner_index')
        if partner_index is not None:
            try:
                partner_index = int(partner_index)
                partners = kyc.partners.copy() if kyc.partners else []

                if partner_index < 0 or partner_index >= len(partners):
                    return Response({"status": "error", "message": "Invalid partner index"},
                                  status=status.HTTP_400_BAD_REQUEST)

                # Delete associated file if exists
                partner = partners[partner_index]
                if partner and 'document' in partner:
                    try:
                        file_path = partner['document'].lstrip('/')
                        if default_storage.exists(file_path):
                            default_storage.delete(file_path)
                    except Exception:
                        pass

                partners.pop(partner_index)
                kyc.partners = partners
                kyc.save()
                return Response({"status": "success", "message": "Partner deleted"})

            except (IndexError, ValueError):
                return Response({"status": "error", "message": "Invalid partner index"},
                              status=status.HTTP_400_BAD_REQUEST)

        kyc.delete()
        return Response({"status": "success", "message": "KYC deleted"},
                      status=status.HTTP_204_NO_CONTENT)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UpdatePartnerAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, pk, index):
        print(f"DEBUG: PATCH request received for KYC {pk}, partner index {index}")
        print(f"DEBUG: Request data: {request.data}")
        print(f"DEBUG: Request FILES: {request.FILES}")

        try:
            kyc = get_object_or_404(Kyc, pk=pk)
            print(f"DEBUG: KYC found: {kyc.id}")

            partners = kyc.partners.copy() if kyc.partners else []
            print(f"DEBUG: Current partners: {partners}")
            print(f"DEBUG: Number of partners: {len(partners)}")

            # Validate index
            if index < 0 or index >= len(partners):
                print(f"DEBUG: Index {index} out of range (0-{len(partners)-1})")
                return Response({"status": "error", "message": "Partner index out of range"},
                              status=status.HTTP_400_BAD_REQUEST)

            partner = partners[index] or {}
            print(f"DEBUG: Current partner data: {partner}")

            # Update fields
            updated_fields = []
            if 'name' in request.data:
                partner['name'] = request.data['name']
                updated_fields.append('name')
                print(f"DEBUG: Updated name to: {request.data['name']}")

            if 'email' in request.data:
                partner['email'] = request.data['email']
                updated_fields.append('email')

            if 'phone' in request.data:
                partner['phone'] = request.data['phone']
                updated_fields.append('phone')

            # Handle file upload
            if 'document' in request.FILES:
                file = request.FILES['document']
                print(f"DEBUG: File received: {file.name}, size: {file.size}")

                # Delete old file if exists
                if 'document' in partner:
                    try:
                        old_file_path = partner['document'].lstrip('/')
                        if default_storage.exists(old_file_path):
                            default_storage.delete(old_file_path)
                    except Exception as e:
                        print(f"DEBUG: Error deleting old file: {e}")

                # Generate unique filename
                file_extension = os.path.splitext(file.name)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"

                # Save file
                path = default_storage.save(
                    os.path.join('partners', unique_filename),
                    ContentFile(file.read())
                )
                partner['document'] = '/' + path.replace('\\', '/')
                updated_fields.append('document')
                print(f"DEBUG: File saved to: {partner['document']}")

            if not updated_fields:
                print("DEBUG: No fields to update")
                return Response({"status": "error", "message": "No fields to update"},
                              status=status.HTTP_400_BAD_REQUEST)

            partners[index] = partner
            kyc.partners = partners
            kyc.save()
            print(f"DEBUG: KYC saved successfully")

            serializer = KycSerializer(kyc)
            return Response({
                "status": "success",
                "message": f"Updated fields: {', '.join(updated_fields)}",
                "data": serializer.data
            })

        except Exception as e:
            print(f"DEBUG: Exception occurred: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return Response({"status": "error", "message": f"An error occurred: {str(e)}"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, pk, index):
        try:
            kyc = get_object_or_404(Kyc, pk=pk)
            partners = kyc.partners.copy() if kyc.partners else []

            if index < 0 or index >= len(partners):
                return Response({"status": "error", "message": "Partner index out of range"},
                              status=status.HTTP_400_BAD_REQUEST)

            # Delete associated file if exists
            partner = partners[index]
            if partner and 'document' in partner:
                try:
                    file_path = partner['document'].lstrip('/')
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)
                except Exception:
                    pass

            partners.pop(index)
            kyc.partners = partners
            kyc.save()

            return Response({"status": "success", "message": "Partner deleted"},
                          status=status.HTTP_200_OK)  # Changed from 204 to 200 for better compatibility

        except Exception as e:
            return Response({"status": "error", "message": f"An error occurred: {str(e)}"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)





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
            tds = serializer.save().order_by('-id')
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



from .models import OtherDoc
from .serializer import OtherDocsSerializer

class OtherDocAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        if pk:
            doc = OtherDoc.objects.filter(pk=pk).first()
            if not doc:
                return Response(
                    {"status": "error", "message": "OtherDoc record not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = OtherDocsSerializer(doc)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        docs = OtherDoc.objects.all().order_by('-pk')
        serializer = OtherDocsSerializer(docs, many=True)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = OtherDocsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            doc = serializer.save()
            return Response(
                {"status": "success", "data": OtherDocsSerializer(doc).data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk=None):
        if not pk:
            return Response(
                {"status": "error", "message": "Primary key (pk) is required for patch"},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc = OtherDoc.objects.filter(pk=pk).first()
        if not doc:
            return Response(
                {"status": "error", "message": "OtherDoc record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OtherDocsSerializer(doc, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk=None):
        if not pk:
            return Response(
                {"status": "error", "message": "Primary key (pk) is required for delete"},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc = OtherDoc.objects.filter(pk=pk).first()
        if not doc:
            return Response(
                {"status": "error", "message": "OtherDoc record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        doc.delete()
        return Response(
            {"status": "success", "message": "OtherDoc record deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )