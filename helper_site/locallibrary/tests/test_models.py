from django.test import TestCase
from locallibrary.models import Author

# class AuthorModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         """Set up non-modified objects used by all test methods."""
#         Author.objects.create(first_name='Big', last_name='Bob')
#
#     def test_first_name_label(self):
#         author = Author.objects.get(id=1)
#         field_label = author._meta.get_field('first_name').verbose_name
#         self.assertEqual(field_label, 'first name')
#
#     def test_last_name_label(self):
#         author = Author.objects.get(id=1)
#         field_label = author._meta.get_field('last_name').verbose_name
#         self.assertEqual(field_label, 'last name')
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)