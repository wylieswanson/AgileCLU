#!/usr/bin/env python

import unittest
import AgileCLU

class AgileCLUTestCase(unittest.TestCase):
  def test_epwbasekey(self):
    hash=AgileCLU.epwbasekey('test', 'test', 'test.example.com', '/')
    self.assertEqual(hash, 'AbiDicIBaEuvafIuegJWVP8j')

  def test_e_pw_hash(self):
    hash=AgileCLU.e_pw_hash('teststr', 'test', 'test', 'test.example.com', '/')
    self.assertEqual(hash, 'jyH0M5b9OyM=')

  def test_e_pw_dehash(self):
    hash=AgileCLU.e_pw_dehash('teststr', 'test', 'test', 'test.example.com', '/')
    self.assertEqual(hash, '87654321')

if __name__ == "__main__":
  unittest.main()
