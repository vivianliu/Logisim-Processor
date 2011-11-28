#!/usr/bin/env python

import os
import os.path
import tempfile
import subprocess
import time
import signal
import re
import sys
import shutil

file_locations = os.path.expanduser(os.getcwd())
logisim_location = os.path.join(os.getcwd(),"logisim-generic-2.7.1.jar")

def student_reference_match_unbounded(student_out, reference_out):
  while True:
    line1 = student_out.readline()
    line2 = reference_out.readline()
    if line2 == '':
      break
    if line1 != line2:
      return False
  return True

def fraction_lines_match_unbounded(student_out,reference_out):
  total_lines = 0
  matched_lines = 0
  while True:
    line1 = student_out.readline()
    line2 = reference_out.readline()
    if line2 == '':
      break
    if line1 == line2:
      matched_lines += 1
    total_lines += 1
  return float(matched_lines)/float(total_lines)
      

class TestCase(object):
  def __init__(self,circfile,tracefile,points):
    self.circfile  = circfile
    self.tracefile = tracefile
    self.points = points

class AbsoluteTestCase(TestCase):
  """
  All-or-nothing test case.
  """
  def __call__(self):
    output = tempfile.TemporaryFile(mode='r+')
    proc = subprocess.Popen(["java","-jar",logisim_location,"-tty","table",os.path.join('.',os.path.basename(self.circfile))],
                            stdin=open('/dev/null'),
                            stdout=subprocess.PIPE)
    try:
      reference = open(self.tracefile)
      passed = student_reference_match_unbounded(proc.stdout,reference)
    finally:
      os.kill(proc.pid,signal.SIGTERM)
    if passed:
      return (self.points,"Matched expected output")
    else:
      return (0,"Did not match expected output")

class FractionalTestCase(TestCase):
  """
  Fractional test case.
  """
  def __call__(self):
    output = tempfile.TemporaryFile(mode='r+')
    shutil.copy(self.circfile,'.')
    proc = subprocess.Popen(["java","-jar",logisim_location,"-tty","table",os.path.join('.',os.path.basename(self.circfile))],
                            stdin=open('/dev/null'),
                            stdout=subprocess.PIPE)
    try:
      reference = open(self.tracefile)
      fraction = fraction_lines_match_unbounded(proc.stdout,reference)
    finally:
      #prevent runaway jvms
      os.kill(proc.pid,signal.SIGTERM)
    if fraction == 1:
      return (self.points,"Matched expected output")
    elif fraction > 0:
      return (fraction * self.points, "Part did not match expected output")
    else:
      return (0,"No lines matched expected output")

def test_submission(name,outfile,tests):
  # actual submission testing code
  print "Testing submission for %s..." % name
  total_points = 0
  total_points_received = 0
  tests_passed = 0
  tests_partially_passed = 0
  tests_failed = 0
  test_results = []
  for description,test,points_received,reason in ((description,test) + test() for description,test in tests): # gross
    points = test.points
    assert points_received <= points
    if points_received == points:
      print "\t%s PASSED test: %s" % (name, description)
      total_points += points
      total_points_received += points
      tests_passed += 1
      test_results.append("\tPassed test \"%s\" worth %d points." % (description,points))
    elif points_received > 0:
      print "\t%s PARTIALLY PASSED test: %s" % (name,description)
      total_points += points
      total_points_received += points_received
      tests_partially_passed += 1
      test_results.append("\tPartially passed test \"%s\" worth %d points (received %d)" % (description, points, points_received))
    else:
      print "\t%s FAILED test: %s" % (name, description)
      total_points += points
      tests_failed += 1
      test_results.append("\tFailed test \"%s\" worth %d points. Reason: %s" % (description, points, reason))
  
  print "\tScore for %s: %d/%d (%d/%d tests passed, %d partially)" %\
    (name, total_points_received, total_points, tests_passed, 
     tests_passed + tests_failed + tests_partially_passed, tests_partially_passed)
  print >> outfile, "%s: %d/%d (%d/%d tests passed, %d partially)" %\
    (name, total_points_received, total_points, tests_passed,
     tests_passed + tests_failed + tests_partially_passed, tests_partially_passed)
  for line in test_results:
    print >> outfile, line
  
  return points_received

def extract_and_test(login,outfile,warnings,tests):
  if subprocess.Popen(['lookat',login]).wait() != 0:
    print >> warnings, "Warning: trying to look at %s failed." % login
    return
  os.chdir('LOOK')
  val = test_submission(login,outfile,tests)
  os.chdir('..')
  return val

name_regex = re.compile(r'(?P<login>cs61c-[a-z][a-z])\.\d{12}')

def get_all_logins():
  logins = set()
  for login in [name_regex.match(l).groupdict()['login'] for l in os.listdir('.') if name_regex.match(l)]:
    logins.add(login)
  return logins

def run_tests(tests):
  outfile = open('GRADING_OUTPUT','w')
  warnings = open('GRADING_WARNINGS','w')
  logins = get_all_logins()
  scores = {}
  for login in logins:
    score = extract_and_test(login,outfile,warnings,tests)
    if score not in scores:
      scores[score] = 1
    else:
      scores[score] += 1
  print scores

def main(tests):
  if len(sys.argv) == 2:
    if sys.argv[1] == '-here':
      test_submission('here',sys.stdout,tests)
    else:
      print >> sys.stderr, "Incorrect usage!"
  elif len(sys.argv) == 3:
    if sys.argv[1] == '-login':
      extract_and_test(sys.args[2],sys.stdout,tests)
    else:
      print >> sys.stderr, "Incorrect usage!"
  elif len(sys.argv) == 1:
    run_tests(tests)
    sys.exit(0)
  else:
    print >> sys.stderr, "Incorrect usage!"
  sys.exit(1)
    
