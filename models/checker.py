# coding:utf-8
import requests
from os.path import exists
from checker_url import CheckerUrl

class Checker():

  TIMEOUT         = 2
  ALLOW_REDIRECTS = True


  def __init__(self, urls_file="sites.txt"):
    self.urls_file     = urls_file
    self.urls          = self.get_urls()
    self.total_urls    = len(self.urls)
    self.total_ok      = 0
    self.total_fail    = 0
    self.total_timeout = 0



  def check(self):
    result = []

    for item in self.urls:
      try:
        response = requests.get(item.url, timeout=self.TIMEOUT, auth=item.auth, allow_redirects=self.ALLOW_REDIRECTS)
      except Exception, e:
        print "URL [%s] TIMEOUT [%s]" % (item.url, e)
        result.append((item.url, response, 'timeout'))
        self.total_timeout += 1
      else:
        if response.status_code == 200:
          result.append((item.url, response, 'ok'))
          self.total_ok += 1
        else:
          print "URL [%s] FAIL [%s]" % (item.url, response.status_code)
          result.append((item.url, response, 'fail'))
          self.total_fail += 1

    return result

  def get_urls(self):
    if exists(self.urls_file):
      with open(self.urls_file) as f:
        return [self.get_url_and_auth(line.strip()) for line in f.readlines() if line.strip()]

    return []

  def get_url_and_auth(self, line):
    if ' ' in line:
      url, auth      = line.rsplit(' ', 1)
      user, password = auth.rsplit(':', 1)
      return CheckerUrl(url, (user, password))
    else:
      return CheckerUrl(line, None)

