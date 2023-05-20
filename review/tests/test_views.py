from django.test import TestCase, Client
from django.shortcuts import render
from django.urls import reverse
from django.contrib.messages import get_messages
from accounts.models import CustomUser
from review.models import Contact, Subject, Review
from review.forms import ContactForm

class IndexTest(TestCase):

    def test_get_index(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class TermsTest(TestCase):
    def test_get_terms(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)

class PrivacyTest(TestCase):
    def test_get_privacy(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)

class ContactsTest(TestCase):
    def setUp(self):
        self.url = reverse('contacts')
        self.form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message.'
        }

    def test_contacts_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contacts_form_valid(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].cleaned_data['name'], 'John Doe')
        self.assertEqual(response.context['form'].cleaned_data['email'], 'johndoe@example.com')
        self.assertEqual(response.context['form'].cleaned_data['message'], 'This is a test message.')

    def test_contacts_form_invalid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Short'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'message', 'お問い合わせ内容が短すぎます')

class ContactsConfirmTest(TestCase):
    def setUp(self):
        self.url = reverse('contacts_confirm')
        self.form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message.'
        }

    def test_contacts_confirm_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)  # Getアクセス禁止

    def test_contacts_confirm_form_valid(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts_confirm.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].cleaned_data['name'], 'John Doe')
        self.assertEqual(response.context['form'].cleaned_data['email'], 'johndoe@example.com')
        self.assertEqual(response.context['form'].cleaned_data['message'], 'This is a test message.')

    def test_contacts_confirm_form_invalid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Short'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'message', 'お問い合わせ内容が短すぎます')

class ContactCreateTest(TestCase):
    def setUp(self):
        self.url = reverse('contacts_create')
        self.form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message.'
        }

    def test_contact_create_form_valid(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contacts_complete'))
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'johndoe@example.com')
        self.assertEqual(contact.message, 'This is a test message.')

    def test_contact_create_form_invalid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Short'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'message', 'お問い合わせ内容が短すぎます')

class ContactsCompleteTest(TestCase):
    def test_contacts_complete_view(self):
        response = self.client.get(reverse('contacts_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/contacts_complete.html')

class SearchTest(TestCase):
    def test_get_privacy(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)


class LectureTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.subject = Subject.objects.create(code='GA13501', name='Test Subject')

    def test_get_lecture_view(self):
        url = reverse('lecture', kwargs={'pk': self.subject.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/lecture.html')

    def test_post_valid_form(self):
        url = reverse('lecture', kwargs={'pk': self.subject.pk})
        form_data = {
            'title': 'Test Review',
            'year': 2023,
            'rating': 5,
            'grade': 'A',
            'overall': 'This is a test review.',
            'difficulty': 'The difficulty level was moderate.',
            'kadai': 'The assignments were challenging.',
            'evaluation': 'I highly recommend this subject.'
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lecture', kwargs={'pk': self.subject.pk}))

        # Verify that the review is created
        review = Review.objects.all().first()
        self.assertIsNotNone(review)
        self.assertEqual(review.year, 2023)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.grade, 'A')
        self.assertEqual(review.overall, 'This is a test review.')
        self.assertEqual(review.difficulty, 'The difficulty level was moderate.')
        self.assertEqual(review.kadai, 'The assignments were challenging.')
        self.assertEqual(review.evaluation, 'I highly recommend this subject')
        self.assertEqual(review.lecture, self.subject)
        self.assertEqual(review.sender_name, 'testuser')

    def test_post_invalid_form(self):
        url = reverse('lecture', kwargs={'pk': self.subject.pk})
        form_data = {
            'title': 'T',  # Invalid title (less than 2 characters)
            'year': 2023,
            'rating': 5,
            'grade': 'A',
            'overall': 'This is a test review.',
            'difficulty': 'The difficulty level was moderate.',
            'kadai': 'The assignments were challenging.',
            'evaluation': 'I highly recommend this subject.'
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/lecture.html')
        self.assertFormError(response, 'form', 'title', 'タイトルが短すぎます')

        # Verify that the review is not created
        review = Review.objects.filter(title='Test Review').first()
        self.assertIsNone(review)