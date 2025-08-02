# # tickets/serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from .models import UserProfile, Category, Ticket, TicketComment, TicketVote

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
    
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'role', 'phone', 'department', 'created_at']

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)
#     password_confirm = serializers.CharField(write_only=True)
#     role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='end_user')
#     phone = serializers.CharField(max_length=20, required=False)
#     department = serializers.CharField(max_length=100, required=False)
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role', 'phone', 'department']
    
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password_confirm']:
#             raise serializers.ValidationError("Passwords don't match")
#         return attrs
    
#     def create(self, validated_data):
#         password_confirm = validated_data.pop('password_confirm')
#         role = validated_data.pop('role', 'end_user')
#         phone = validated_data.pop('phone', '')
#         department = validated_data.pop('department', '')
        
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(
#             user=user,
#             role=role,
#             phone=phone,
#             department=department
#         )
#         return user

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
    
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
        
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise serializers.ValidationError('Invalid credentials')
#             if not user.is_active:
#                 raise serializers.ValidationError('User account is disabled')
#             attrs['user'] = user
#         else:
#             raise serializers.ValidationError('Must include username and password')
        
#         return attrs

# class CategorySerializer(serializers.ModelSerializer):
#     created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description', 'created_by', 'created_by_name', 'created_at', 'is_active']
#         read_only_fields = ['created_by', 'created_at']

# class TicketCommentSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.get_full_name', read_only=True)
#     user_username = serializers.CharField(source='user.username', read_only=True)
    
#     class Meta:
#         model = TicketComment
#         fields = ['id', 'comment', 'user', 'user_name', 'user_username', 'is_internal', 'created_at', 'attachment']
#         read_only_fields = ['user', 'created_at']

# class TicketVoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketVote
#         fields = ['id', 'vote_type', 'created_at']
#         read_only_fields = ['created_at']

# class TicketListSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
#     assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
#     reply_count = serializers.IntegerField(read_only=True)
    
#     class Meta:
#         model = Ticket
#         fields = [
#             'id', 'subject', 'category', 'category_name', 'status', 'priority',
#             'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name',
#             'created_at', 'updated_at', 'upvotes', 'downvotes', 'reply_count'
#         ]

# class TicketDetailSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
#     assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
#     comments = TicketCommentSerializer(many=True, read_only=True)
#     user_vote = serializers.SerializerMethodField()
#     reply_count = serializers.IntegerField(read_only=True)
    
#     class Meta:
#         model = Ticket
#         fields = [
#             'id', 'subject', 'description', 'category', 'category_name', 
#             'status', 'priority', 'created_by', 'created_by_name',
#             'assigned_to', 'assigned_to_name', 'created_at', 'updated_at',
#             'resolved_at', 'closed_at', 'attachment', 'upvotes', 'downvotes',
#             'comments', 'user_vote', 'reply_count'
#         ]
    
#     def get_user_vote(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             vote = TicketVote.objects.filter(ticket=obj, user=request.user).first()
#             return vote.vote_type if vote else None
#         return None

# class TicketCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['subject', 'description', 'category', 'priority', 'attachment']
    
#     def create(self, validated_data):
#         validated_data['created_by'] = self.context['request'].user
#         return super().create(validated_data)

# class TicketUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['subject', 'description', 'category', 'priority', 'status', 'assigned_to']
    
#     def validate_status(self, value):
#         """Validate status transition according to workflow"""
#         if self.instance:
#             current_status = self.instance.status
#             valid_transitions = {
#                 'open': ['in_progress', 'closed'],
#                 'in_progress': ['resolved', 'open'],
#                 'resolved': ['closed', 'in_progress'],
#                 'closed': []  # Closed tickets cannot be changed
#             }
            
#             if current_status == 'closed' and value != 'closed':
#                 raise serializers.ValidationError("Closed tickets cannot be reopened")
            
#             if value not in valid_transitions.get(current_status, []) and value != current_status:
#                 raise serializers.ValidationError(
#                     f"Invalid status transition from {current_status} to {value}"
#                 )
        
#         return value


# from rest_framework import serializers
# from .models import Category, Ticket, TicketComment, TicketVote
# from custom_auth.models import UserProfile
# from django.contrib.auth.models import User

# # Serializer for category data
# class CategorySerializer(serializers.ModelSerializer):
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description', 'created_by_name', 'created_at', 'is_active']
#         read_only_fields = ['created_by', 'created_at']

# # Serializer for ticket list display
# class TicketListSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)
#     assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
#     reply_count = serializers.IntegerField(read_only=True)
#     user_vote = serializers.SerializerMethodField()

#     class Meta:
#         model = Ticket
#         fields = [
#             'id', 'subject', 'category_name', 'status', 'priority', 'created_by_name', 
#             'assigned_to_name', 'created_at', 'updated_at', 'reply_count', 'upvotes', 'downvotes', 'user_vote'
#         ]

#     def get_user_vote(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             try:
#                 vote = obj.votes.get(user=request.user)
#                 return vote.vote_type
#             except TicketVote.DoesNotExist:
#                 return None
#         return None

# # Serializer for ticket detail view
# class TicketDetailSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)
#     assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
#     comments = TicketCommentSerializer(many=True, read_only=True)
#     reply_count = serializers.IntegerField(read_only=True)
#     user_vote = serializers.SerializerMethodField()

#     class Meta:
#         model = Ticket
#         fields = [
#             'id', 'subject', 'description', 'category', 'category_name', 'status', 'priority', 
#             'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name', 
#             'created_at', 'updated_at', 'resolved_at', 'closed_at', 'attachment', 
#             'upvotes', 'downvotes', 'reply_count', 'comments', 'user_vote'
#         ]

#     def get_user_vote(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             try:
#                 vote = obj.votes.get(user=request.user)
#                 return vote.vote_type
#             except TicketVote.DoesNotExist:
#                 return None
#         return None

# # Serializer for creating tickets
# class TicketCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['subject', 'description', 'category', 'priority', 'attachment']

# # Serializer for updating tickets
# class TicketUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['status', 'assigned_to']

# # Serializer for ticket comments
# class TicketCommentSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.username', read_only=True)
#     user_role = serializers.CharField(source='user.userprofile.role', read_only=True)
    
#     class Meta:
#         model = TicketComment
#         fields = ['id', 'ticket', 'user', 'user_name', 'user_role', 'comment', 'is_internal', 'created_at', 'attachment']
#         read_only_fields = ['user', 'ticket', 'created_at']

# # Serializer for ticket votes
# class TicketVoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketVote
#         fields = ['ticket', 'user', 'vote_type', 'created_at']

from rest_framework import serializers
from .models import Category, Ticket, TicketComment, TicketVote
from custom_auth.models import UserProfile
from django.contrib.auth.models import User

# Serializer for category data
class CategorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_by_name', 'created_at', 'is_active']
        read_only_fields = ['created_by', 'created_at']

# Serializer for ticket comments
class TicketCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.CharField(source='user.userprofile.role', read_only=True)
    
    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'user', 'user_name', 'user_role', 'comment', 'is_internal', 'created_at', 'attachment']
        read_only_fields = ['user', 'ticket', 'created_at']

# Serializer for ticket votes
class TicketVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketVote
        fields = ['ticket', 'user', 'vote_type', 'created_at']

# Serializer for ticket list display
class TicketListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'subject', 'category_name', 'status', 'priority', 'created_by_name', 
            'assigned_to_name', 'created_at', 'updated_at', 'reply_count', 'upvotes', 'downvotes', 'user_vote'
        ]

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                vote = obj.votes.get(user=request.user)
                return vote.vote_type
            except TicketVote.DoesNotExist:
                return None
        return None

# Serializer for ticket detail view
class TicketDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'subject', 'description', 'category', 'category_name', 'status', 'priority', 
            'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name', 
            'created_at', 'updated_at', 'resolved_at', 'closed_at', 'attachment', 
            'upvotes', 'downvotes', 'reply_count', 'comments', 'user_vote'
        ]

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                vote = obj.votes.get(user=request.user)
                return vote.vote_type
            except TicketVote.DoesNotExist:
                return None
        return None

# Serializer for creating tickets
class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'category', 'priority', 'attachment']

# Serializer for updating tickets
class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to']