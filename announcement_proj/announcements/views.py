from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, Comment
from .forms import CommentForm

# View to list announcements
def announcement_list(request):
    announcements = Announcement.objects.filter(sent=True).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

# View to see announcement details
def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    comments = announcement.comments.all()
    form = CommentForm()  # Add this line to pass the empty form to the template
    return render(request, 'announcements/announcement_detail.html', {
        'announcement': announcement,
        'comments': comments,
        'form': form  # Include the form in the context
    })

# View to add a comment
def add_comment(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.announcement = announcement
            comment.user = request.user
            comment.save()
            return redirect('announcement_detail', id=announcement.id)
    else:
        form = CommentForm()  # This renders an empty form on GET requests
    return render(request, 'announcements/announcement_detail.html', {
        'announcement': announcement,
        'comments': announcement.comments.all(),
        'form': form
    })
