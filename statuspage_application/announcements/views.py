from django.shortcuts import render
from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})
# Create your views here.
