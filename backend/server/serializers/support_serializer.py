from rest_framework import serializers
from server.models import SupportQuery, SupportReply

class SupportReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportReply
        fields = ['id', 'message', 'is_staff', 'created_at']

class SupportQuerySerializer(serializers.ModelSerializer):
    replies = SupportReplySerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportQuery
        fields = ['id', 'subject', 'message', 'status', 'created_at', 'updated_at', 
                 'customer_name', 'customer_email', 'replies']
    
    def get_customer_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    
    def get_customer_email(self, obj):
        return obj.user.email