# # tickets/models.py
# from django.db import models
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings

# # class UserProfile(models.Model):
# #     ROLE_CHOICES = [
# #         ('end_user', 'End User'),
# #         ('support_agent', 'Support Agent'),
# #         ('admin', 'Admin'),
# #     ]
    
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='end_user')
# #     phone = models.CharField(max_length=20, blank=True)
# #     department = models.CharField(max_length=100, blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
    
# #     def __str__(self):
# #         return f"{self.user.username} - {self.role}"
    
# #     class Meta:
# #         db_table = 'user_profiles'
# #         indexes = [
# #             models.Index(fields=['role']),
# #         ]

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         db_table = 'categories'
#         verbose_name_plural = 'Categories'
#         ordering = ['name']

# class Ticket(models.Model):
#     STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('in_progress', 'In Progress'),
#         ('resolved', 'Resolved'),
#         ('closed', 'Closed'),
#     ]
    
#     PRIORITY_CHOICES = [
#         ('low', 'Low'),
#         ('medium', 'Medium'),
#         ('high', 'High'),
#         ('urgent', 'Urgent'),
#     ]
    
#     subject = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     resolved_at = models.DateTimeField(null=True, blank=True)
#     closed_at = models.DateTimeField(null=True, blank=True)
    
#     attachment = models.FileField(upload_to='ticket_attachments/', blank=True, null=True)
#     upvotes = models.PositiveIntegerField(default=0)
#     downvotes = models.PositiveIntegerField(default=0)
    
#     def __str__(self):
#         return f"#{self.id} - {self.subject}"
    
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None
#         old_status = None
        
#         if not is_new:
#             old_ticket = Ticket.objects.get(pk=self.pk)
#             old_status = old_ticket.status
        
#         super().save(*args, **kwargs)
        
#         # Send notification emails
#         if is_new:
#             self.send_creation_notification()
#         elif old_status and old_status != self.status:
#             self.send_status_update_notification()
    
#     def send_creation_notification(self):
#         subject = f"New Ticket Created: #{self.id}"
#         message = f"""
#         A new ticket has been created:
        
#         Subject: {self.subject}
#         Category: {self.category.name}
#         Created by: {self.created_by.get_full_name() or self.created_by.username}
        
#         Description:
#         {self.description}
#         """
        
#         recipients = [self.created_by.email]
#         if self.assigned_to and self.assigned_to.email:
#             recipients.append(self.assigned_to.email)
        
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=recipients,
#             fail_silently=True,
#         )
    
#     def send_status_update_notification(self):
#         subject = f"Ticket Status Updated: #{self.id}"
#         message = f"""
#         Your ticket status has been updated:
        
#         Ticket: #{self.id} - {self.subject}
#         New Status: {self.get_status_display()}
#         Updated by: {self.assigned_to.get_full_name() if self.assigned_to else 'System'}
#         """
        
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[self.created_by.email],
#             fail_silently=True,
#         )
    
#     @property
#     def reply_count(self):
#         return self.comments.count()
    
#     class Meta:
#         db_table = 'tickets'
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['status']),
#             models.Index(fields=['category']),
#             models.Index(fields=['created_at']),
#             models.Index(fields=['updated_at']),
#             models.Index(fields=['assigned_to']),
#             models.Index(fields=['created_by']),
#         ]

# class TicketComment(models.Model):
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField()
#     is_internal = models.BooleanField(default=False)  # For agent-only comments
#     created_at = models.DateTimeField(auto_now_add=True)
#     attachment = models.FileField(upload_to='comment_attachments/', blank=True, null=True)
    
#     def __str__(self):
#         return f"Comment on #{self.ticket.id} by {self.user.username}"
    
#     class Meta:
#         db_table = 'ticket_comments'
#         ordering = ['created_at']
#         indexes = [
#             models.Index(fields=['ticket', 'created_at']),
#         ]

# class TicketVote(models.Model):
#     VOTE_CHOICES = [
#         ('up', 'Upvote'),
#         ('down', 'Downvote'),
#     ]
    
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='votes')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = 'ticket_votes'
#         unique_together = ['ticket', 'user']  # One vote per user per ticket
#         indexes = [
#             models.Index(fields=['ticket', 'vote_type']),
#         ]

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    attachment = models.FileField(upload_to='ticket_attachments/', blank=True, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"#{self.id} - {self.subject}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_ticket = Ticket.objects.get(pk=self.pk)
            old_status = old_ticket.status
        
        super().save(*args, **kwargs)
        
        if is_new:
            self.send_creation_notification()
        elif old_status and old_status != self.status:
            self.send_status_update_notification()
    
    def send_creation_notification(self):
        subject = f"New Ticket Created: #{self.id}"
        message = f"""
        A new ticket has been created:
        
        Subject: {self.subject}
        Category: {self.category.name}
        Created by: {self.created_by.get_full_name() or self.created_by.username}
        
        Description:
        {self.description}
        """
        
        recipients = [self.created_by.email]
        if self.assigned_to and self.assigned_to.email:
            recipients.append(self.assigned_to.email)
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    
    def send_status_update_notification(self):
        subject = f"Ticket Status Updated: #{self.id}"
        message = f"""
        Your ticket status has been updated:
        
        Ticket: #{self.id} - {self.subject}
        New Status: {self.get_status_display()}
        Updated by: {self.assigned_to.get_full_name() if self.assigned_to else 'System'}
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.created_by.email],
            fail_silently=True,
        )
    
    @property
    def reply_count(self):
        return self.comments.count()
    
    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_by']),
        ]

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='comment_attachments/', blank=True, null=True)
    
    def __str__(self):
        return f"Comment on #{self.ticket.id} by {self.user.username}"
    
    class Meta:
        db_table = 'ticket_comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['ticket', 'created_at']),
        ]

class TicketVote(models.Model):
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ticket_votes'
        unique_together = ['ticket', 'user']
        indexes = [
            models.Index(fields=['ticket', 'vote_type']),
        ]