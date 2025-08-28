from rest_framework import serializers
from .models import Lawyer, LawyerVerification, Case


class LawyerSerializer(serializers.ModelSerializer):
    """
    Serializer for Lawyer model
    """
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    total_cases = serializers.ReadOnlyField()
    won_cases = serializers.ReadOnlyField()
    win_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Lawyer
        fields = [
            'id', 'full_name', 'email', 'bar_id', 'specialization', 
            'location', 'experience_years', 'is_verified', 'verification_date',
            'bio', 'contact_phone', 'office_address', 'consultation_fee',
            'total_cases', 'won_cases', 'win_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'verification_date', 'created_at', 'updated_at']


class VerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for LawyerVerification model
    """
    lawyer_name = serializers.CharField(source='lawyer.user.get_full_name', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    
    class Meta:
        model = LawyerVerification
        fields = [
            'id', 'lawyer_name', 'method', 'method_display', 'status', 'status_display',
            'extracted_data', 'confidence_score', 'admin_comments', 
            'reviewed_by_name', 'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CaseSerializer(serializers.ModelSerializer):
    """
    Serializer for Case model
    """
    lawyer_name = serializers.CharField(source='lawyer.user.get_full_name', read_only=True)
    case_type_display = serializers.CharField(source='get_case_type_display', read_only=True)
    outcome_display = serializers.CharField(source='get_outcome_display', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Case
        fields = [
            'id', 'lawyer_name', 'title', 'description', 'case_type', 'case_type_display',
            'outcome', 'outcome_display', 'date_filed', 'date_resolved', 'court_name',
            'case_number', 'client_name', 'opposing_party', 'case_value', 'legal_fees',
            'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LawyerSearchSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for lawyer search results
    """
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    win_rate = serializers.ReadOnlyField()
    total_cases = serializers.ReadOnlyField()
    
    class Meta:
        model = Lawyer
        fields = [
            'id', 'full_name', 'specialization', 'location', 'experience_years',
            'win_rate', 'total_cases', 'consultation_fee', 'is_verified'
        ]