from .models import Customer, Invoice, InvoiceItem
from django.utils import timezone
from datetime import date
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'created_at']
        read_only_fields = ['created_at']


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total']
        read_only_fields = ['total']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity has to be at least 1")
        return value

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Unit price has to be greater than 0")
        return value
    

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    total_amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            'id', 'customer', 'issue_date', 'due_date', 
            'status', 'created_at', 'items', 'total_amount'
        ]
        read_only_fields = ['created_at', 'total_amount']

    def validate(self, data):
        # Validate due_date >= issue_date
        if data['due_date'] < data['issue_date']:
            raise serializers.ValidationError(
                "Due date must be on or after issue date"
            )
        
        # Validate at least one line item
        if 'items' in data and len(data['items']) == 0:
            raise serializers.ValidationError(
                "Invoice must have at least one item"
            )
            
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
            
        return invoice


class InvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['status']