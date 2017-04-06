import sys
import unittest

sys.path.append('../')
from checker.models import Checker

class CheckerTest(unittest.TestCase):
  def test_can_instanciate(self):
    checker = Checker()
    self.assertNotEqual(None, checker)

  def test_can_set_urls_file(self):
    checker = Checker('tests/sites_test.txt')
    self.assertEqual(checker.urls_file, 'tests/sites_test.txt')

  def test_can_has_initial_urls_file(self):
    checker = Checker()
    self.assertEqual(checker.urls_file, 'sites.txt')

  def test_can_get_urls_from_urls_file(self):
    # for this test, you must have a file called sites.txt
    checker = Checker('tests/sites_test.txt')
    self.assertEqual(checker.urls[0].url, 'http://google.com.br')
    self.assertEqual(checker.urls[0].auth, None)
    self.assertEqual(checker.urls[1].url, 'http://httpbin.org/basic-auth/user/passwd')
    self.assertEqual(checker.urls[1].auth, ('user', 'passwd'))
    self.assertEqual(checker.urls[2].url, 'http://failurl')
    self.assertEqual(checker.urls[2].auth, None)
    self.assertEqual(checker.urls[3].url, 'http://dmenezes.com.br/404')
    self.assertEqual(checker.urls[3].auth, None)

  def test_must_test_urls(self):
    checker = Checker('tests/sites_test.txt')
    result  = checker.check()
    self.assertEqual(len(result), 4)

  def test_must_get_timeout_on_wrong_url(self):
    checker = Checker('tests/sites_test.txt')
    result  = checker.check()
    self.assertEqual(result[2].count('timeout'), 1)

  def test_must_have_total_of_sites_to_check(self):
    checker = Checker('tests/sites_test.txt')
    self.assertEqual(checker.total_urls, 4)

  def test_must_have_total_ok(self):
    checker = Checker('tests/sites_test.txt')
    checker.check()
    self.assertEqual(checker.total_ok, 2)

  def test_must_have_total_fail(self):
    checker = Checker('tests/sites_test.txt')
    checker.check()
    self.assertEqual(checker.total_fail, 1)

  def test_must_have_total_timeout(self):
    checker = Checker('tests/sites_test.txt')
    checker.check()
    self.assertEqual(checker.total_timeout, 1)

  def test_must_get_fail_on_not_found_url(self):
    checker = Checker('tests/sites_test.txt')
    result  = checker.check()
    self.assertEqual(result[3].count('fail'), 1)


if __name__ == '__main__':
    unittest.main()
