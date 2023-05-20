from django.test import TestCase
from review.models import Subject, Review, Contact

class SubjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Subject.objects.create(
            code='GA13501',
            name='Test Subject',
            unit='3',
            grade='3',
            semester='Spring',
            teachers='John Doe',
            overview='This is a test subject.',
            subtype='Science',
            schools='School of Engineering',
            colleges='College of Computer Science'
        )

    def test_name_label(self):
        subject = Subject.objects.get(code='GA13501')
        field_label = subject._meta.get_field('name').verbose_name
        self.assertEqual(field_label, '科目名')

    # 他のフィールドのテストも同様に追加する

    def test_str_method(self):
        subject = Subject.objects.get(code='GA13501')
        expected_str = subject.name
        self.assertEqual(str(subject), expected_str)

    # 他のメソッドのテストも同様に追加する

class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(
            code='GA13501',
            name='Test Subject',
            unit='3',
            grade='3',
            semester='Spring',
            teachers='John Doe',
            overview='This is a test subject.',
            subtype='Science',
            schools='School of Engineering',
            colleges='College of Computer Science'
        )
        Review.objects.create(
            lecture=subject,
            sender_name='John Smith',
            sender_college=1,
            title='Test Review',
            year=2022,
            rating=5,
            grade=5,
            overall='Great lecture.',
            difficulty='Moderate',
            kadai='Reasonable amount and quality of assignments.',
            evaluation='Fair evaluation.',
        )

    def test_sender_name_label(self):
        review = Review.objects.get(title='Test Review')
        field_label = review._meta.get_field('sender_name').verbose_name
        self.assertEqual(field_label, '投稿者名')

    # 他のフィールドのテストも同様に追加する

    def test_str_method(self):
        review = Review.objects.get(title='Test Review')
        expected_str = str(review.review_id)
        self.assertEqual(str(review), expected_str)

    # 他のメソッドのテストも同様に追加する

class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contact.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            message='Test message.'
        )

    def test_name_label(self):
        contact = Contact.objects.get(email='johndoe@example.com')
        field_label = contact._meta.get_field('name').verbose_name
        self.assertEqual(field_label, '名前')

    # 他のフィールドのテストも同様に追加する

    def test_str_method(self):
        contact = Contact.objects.get(email='johndoe@example.com')
        expected_str = contact.name
        self.assertEqual(str(contact), expected_str)

    # 他のメソッドのテストも同様に追加する

