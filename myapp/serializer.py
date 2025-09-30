from rest_framework import serializers
from .models import *
from django.core.files.storage import default_storage

class Adminserializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'



class Staffserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=False)  # show password here

    class Meta:
        model = Staff
        fields = ['id', 'name', 'email', 'password', 'mobile_No']

class StaffNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'email', 'mobile_No']



class ClientSerializer_add(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

# class ClientSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Client
#         exclude = ['password']


from django.core.files.storage import default_storage
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):

    client = ClientSerializer(read_only=True)
    staff = Staffserializer(read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), source='staff', write_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'status',
            'client', 'staff', 'client_id', 'staff_id'
        ]
        read_only_fields = ['start_date']


class IncomeTaxSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = IncomeTax
        fields = [   'id',
            'ass_year',
            'final_year',
            'itr',
            'computation',
            'trading',
            'balance',
            'audit',
            'client',
            'client_id',
            ]



class GstSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # ✔ no password
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = Gst
        fields = ['id', 'year', 'other', 'client', 'client_id','sales','purchase','bank','other',]





class KycSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # shows id and name
    partners = serializers.JSONField(required=False, default=list, allow_null=True)

    class Meta:
        model = Kyc
        fields = ['id', 'client', 'partners']

    def create(self, validated_data):
        request = self.context.get("request")
        client_id = self.initial_data.get("client")  # client id from request
        client = Client.objects.get(pk=client_id)
        partners_list = validated_data.pop("partners", [])

        kyc_instance, created = Kyc.objects.get_or_create(client=client, defaults={'partners': []})
        updated_partners = list(kyc_instance.partners or [])

        if request and request.FILES:
            for i, partner_obj in enumerate(partners_list):
                file_key = f"partners_{i}_document"
                uploaded_file = request.FILES.get(file_key)
                file_url = None
                if uploaded_file:
                    file_path = default_storage.save(f"partners/{uploaded_file.name}", uploaded_file)
                    file_url = default_storage.url(file_path)

                if isinstance(partner_obj, dict):
                    partner_obj["document"] = file_url
                    updated_partners.append(partner_obj)
                else:
                    updated_partners.append({"name": str(partner_obj), "document": file_url})
        else:
            for partner_obj in partners_list:
                if isinstance(partner_obj, dict):
                    updated_partners.append(partner_obj)
                else:
                    updated_partners.append({"name": str(partner_obj), "document": None})

        kyc_instance.partners = updated_partners
        kyc_instance.save()
        return kyc_instance

    def update(self, instance, validated_data):
        request = self.context.get("request")
        partners_data = validated_data.pop("partners", None)
        instance.client = validated_data.get("client", instance.client)

        if partners_data is not None:
            # Loop through each partner info in the update payload
            for partner_info in partners_data:
                index = partner_info.get("index")
                action = partner_info.get("action", "update")  # default action is update

                if index is None or index >= len(instance.partners):
                    continue  # skip invalid indices

                if action == "delete":
                    # Remove partner at index
                    instance.partners.pop(index)
                else:  # update partner
                    partner = instance.partners[index]

                    # Update name/email/phone if provided
                    for field in ["name", "email", "phone"]:
                        if field in partner_info:
                            partner[field] = partner_info[field]

                    # Update file if uploaded
                    if request and request.FILES:
                        file_key = f"partners_{index}_document"  # same pattern as create
                        uploaded_file = request.FILES.get(file_key)
                        if uploaded_file:
                            # Optional: delete old file if exists
                            old_file = partner.get("document")
                            if old_file:
                                old_file_path = old_file.lstrip("/")
                                if default_storage.exists(old_file_path):
                                    default_storage.delete(old_file_path)

                            # Save new file
                            file_path = default_storage.save(f"partners/{uploaded_file.name}", uploaded_file)
                            partner["document"] = default_storage.url(file_path)

                    # Assign updated partner back
                    instance.partners[index] = partner

        instance.save()
        return instance



class TdsSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = Tds
        fields = ['id', 'year', 'document', 'client', 'client_id']


class OtherDocsSerializer(serializers.ModelSerializer):
    partners = serializers.JSONField(required=False, default=list, allow_null=True)

    class Meta:
        model = OtherDoc
        fields = ['id', 'client', 'partners']

    def create(self, validated_data):
        request = self.context.get("request")
        client = validated_data.get("client")
        partners_list = validated_data.pop("partners", [])

        # Check for existing record for the same client
        other_doc_instance = OtherDoc.objects.filter(client=client).first()

        if not other_doc_instance:
            # Create if not exists
            other_doc_instance = OtherDoc.objects.create(client=client, partners=[])

        updated_partners = list(other_doc_instance.partners or [])

        if request and request.FILES:
            for i, partner_obj in enumerate(partners_list):
                file_key = f"partners_{i}_document"
                uploaded_file = request.FILES.get(file_key)

                file_url = None
                if uploaded_file:
                    file_path = default_storage.save(f"partners/{uploaded_file.name}", uploaded_file)
                    file_url = default_storage.url(file_path)

                if isinstance(partner_obj, dict):
                    partner_obj["document"] = file_url
                    updated_partners.append(partner_obj)
                else:
                    updated_partners.append({"name": str(partner_obj), "document": file_url})
        else:
            for partner_obj in partners_list:
                if isinstance(partner_obj, dict):
                    updated_partners.append(partner_obj)
                else:
                    updated_partners.append({"name": str(partner_obj), "document": None})

        other_doc_instance.partners = updated_partners
        other_doc_instance.save()

        return other_doc_instance

    def update(self, instance, validated_data):
        request = self.context.get("request")
        partners_data = validated_data.pop("partners", None)

        instance.client = validated_data.get("client", instance.client)

        if partners_data is not None:
            if isinstance(partners_data, dict) and "name" in partners_data:
                partners_data = [partners_data]

            updated_partners = []

            for i, partner in enumerate(partners_data):
                file_key = f"partners_{i}_document"
                uploaded_file = request.FILES.get(file_key) if request else None

                if uploaded_file:
                    file_path = default_storage.save(f"partners/{uploaded_file.name}", uploaded_file)
                    partner['document'] = default_storage.url(file_path)
                else:
                    # Preserve old document if exists
                    if i < len(instance.partners):
                        partner['document'] = instance.partners[i].get('document')

                updated_partners.append(partner)

            instance.partners = updated_partners

        instance.save()
        return instance




