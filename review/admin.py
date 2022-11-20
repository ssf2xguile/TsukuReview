from django.contrib import admin
from .models import Subject, Review

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'schools', 'colleges')
    list_display_links = ('code', 'name')
    list_filter = ('schools', 'colleges')

class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'title', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(Review, ReviewModelAdmin)