from django.test import TestCase
from django.contrib.auth.models import User
from .models import Announcement, Section, Comment
from django.utils import timezone
from django.urls import reverse

class AnnouncementModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username="testuser", password="password")
        self.section = Section.objects.create(name="Test Section")
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            content="This is a test announcement.",
            topic="General",
            scheduled_time=timezone.now(),
            author=self.user
        )
        self.announcement.sections.add(self.section)

    def test_announcement_creation(self):
        """Test that an announcement can be created and saved correctly."""
        self.assertEqual(self.announcement.title, "Test Announcement")
        self.assertEqual(self.announcement.content, "This is a test announcement.")
        self.assertEqual(self.announcement.topic, "General")
        self.assertEqual(self.announcement.author, self.user)
        self.assertIn(self.section, self.announcement.sections.all())

    def test_comment_creation(self):
        """Test that a comment can be created for an announcement."""
        comment = Comment.objects.create(
            announcement=self.announcement,
            user=self.user,
            content="This is a test comment."
        )
        self.assertEqual(comment.content, "This is a test comment.")
        self.assertEqual(comment.announcement, self.announcement)
        self.assertEqual(comment.user, self.user)

class AnnouncementViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.section = Section.objects.create(name="Test Section")
        self.announcement = Announcement.objects.create(
            title="Announcement 1",
            content="This is the first test announcement.",
            topic="Urgent",
            scheduled_time=timezone.now(),
            author=self.user,
            sent=True  # Set sent=True to ensure it appears in the list view
        )
        self.announcement.sections.add(self.section)
        self.client.login(username="testuser", password="password")
        
  def test_announcement_list_view(self):
      """Test that the announcement list view returns the correct announcements."""
        response = self.client.get(reverse("announcement_list"))
        self.assertEqual(response.status_code, 200)

    def test_announcement_detail_view(self):
        """Test that the announcement detail view displays the announcement and comments."""
        response = self.client.get(reverse("announcement_detail", args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the first test announcement.")

    def test_add_comment(self):
        """Test adding a comment to an announcement."""
        response = self.client.post(reverse("add_comment", args=[self.announcement.id]), {
            "content": "This is a comment on the announcement."
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after posting
        self.assertTrue(Comment.objects.filter(content="This is a comment on the announcement.").exists())
