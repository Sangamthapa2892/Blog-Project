from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Contact

class ContactModelTest(TestCase):
    def test_str_representation(self):
        contact = Contact(name="Sangam")
        self.assertEqual(str(contact), "Sangam")