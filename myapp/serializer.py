from rest_framework import serializers
from .models import *


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

    # id = serializers.IntegerField(read_only=True)  
    # name = serializers.CharField(max_length=200)
    # email = serializers.EmailField(max_length=100)
    # password = serializers.CharField(max_length=150)
    # mobile_No = serializers.IntegerField()

    # def create(self, validated_data):
    #     # Create and return a new Staff instance
    #     return Staff.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     # Update and return an existing Staff instance
        
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.mobile_No = validated_data.get('mobile_No', instance.mobile_No)
    #     instance.save()
    #     return instance



class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'

class ClientNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'name','mobile_No']        


class IncomeTaxSerializer(serializers.ModelSerializer):
    # Nested serializers for read (output)
    # staff = Staffserializer(read_only=True)
    client = ClientSerializer(read_only=True)
    
    # Write-only fields for input (accept just the IDs)
    # staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), source='staff', write_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    
    class Meta:
        model = IncomeTax
        fields = ['id', 'year', 'document', 'client', 'client_id']


class TaskSerializer(serializers.ModelSerializer):
    client = ClientNestedSerializer(read_only=True)  # Show client (without password)
    
    # Removed: staff = StaffNestedSerializer(read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)
    

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'status', 'client', 'client_id'
        ]
        read_only_fields = ['start_date']
        

class GstSerializer(serializers.ModelSerializer):
    client = ClientNestedSerializer(read_only=True)  # ✔ no password
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = Gst
        fields = ['id', 'year', 'document', 'client', 'client_id']

class KycSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = Kyc
        fields = ['id', 'year', 'document', 'client', 'client_id']


class TdsSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = Tds
        fields = ['id', 'year', 'document', 'client', 'client_id']

class OtherDocsSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client', write_only=True)

    class Meta:
        model = OtherDoc
        fields = ['id', 'year', 'document', 'client', 'client_id']