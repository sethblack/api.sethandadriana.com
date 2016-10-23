from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone
from snaapi import models

import json

global_client = Client()

class Tests(TestCase):
    def test_images(self):
        for x in xrange(0, 5):
            models.WeddingPicture(owner='Seth', picture='snaapi/test.png', capture_date=timezone.now()).save()

        response = global_client.get(reverse('wedding-pictures'))
        self.assertEqual(response.status_code, 200)

        response_decoded = json.loads(response.content)

        self.assertEqual(len(response_decoded['wedding_pictures']), 5)