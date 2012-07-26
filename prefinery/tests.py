from django.test import TestCase
from django.test.utils import override_settings
from django.http import HttpResponse
import prefinery_lib as utils
import os

def callback(request, tester):
    return HttpResponse()

_keys = ['PREFINERY_URL', 'PREFINERY_KEY', 'PREFINERY_BETA_ID', 'PREFINERY_USE_SHORT_CODES']
_settings = {'PREFINERY_CALLBACK': callback}
_settings.update({ k: os.environ[k] for k in _keys if k in os.environ })

TEST_EMAIL = 'django-prefinery@test.com'

@override_settings(**_settings)
class BaseTest(TestCase):
    def setUp(self):
      self.tester_email = TEST_EMAIL
      resp = utils.create_tester(self.tester_email, 'invited')
      self.assertEqual(resp.status, 201, resp)
      self.tester_id = utils.get_tester_id_by_email(self.tester_email)
      self.assertTrue(self.tester_id)
    
    def tearDown(self):
      resp = utils.delete_tester(self.tester_id)
      self.assertEqual(resp.status, 200)
    

class LibTest(BaseTest):
    def test_get_code(self):
        code = utils.get_tester_code(self.tester_id)
        self.assertTrue(code)

    def test_check_code_of_tester(self):
        code = utils.get_tester_code(self.tester_id)
        resp = utils.verify_code(self.tester_id, code)
        self.assertFalse(resp is None)

    def test_check_fake_code_of_tester(self):
        resp = utils.verify_code(self.tester_id, 'aasdfadsf')
        self.assertTrue(resp is None)

    def test_activate_user(self):
        resp = utils.set_tester_status(self.tester_id, 'active')
        self.assertTrue(resp)
        
        
class SignUpTest(BaseTest):
    urls = 'prefinery.urls'
      
    def test_signup(self):
        code = utils.get_tester_code(self.tester_id)
        url = '/signup?email=%s&code=%s' % (TEST_EMAIL, code)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    
    def test_signup_bad_code(self):
        code = 'bad-code'
        url = '/signup?email=%s&code=%s' % (TEST_EMAIL, code)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)