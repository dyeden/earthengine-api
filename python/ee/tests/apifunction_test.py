#!/usr/bin/env python
"""Tests for the ee.apifunction module."""



import types

import unittest

import ee

from ee import apitestcase


class ApiFunctionTest(apitestcase.ApiTestCase):

  def testAddFunctions(self):
    """Verifies that addition of static and instance API functions."""

    # Check instance vs static functions, and trampling of
    # existing functions.
    class TestClass(object):
      def pre_addBands(self):  # pylint: disable-msg=g-bad-name
        pass

    self.assertFalse(hasattr(TestClass, 'pre_load'))
    self.assertFalse(hasattr(TestClass, 'select'))
    self.assertFalse(hasattr(TestClass, 'pre_select'))
    self.assertTrue(hasattr(TestClass, 'pre_addBands'))
    self.assertFalse(hasattr(TestClass, '_pre_addBands'))

    ee.ApiFunction.importApi(TestClass, 'Image', 'Image', 'pre_')
    self.assertFalse(isinstance(TestClass.pre_load, types.MethodType))
    self.assertFalse(hasattr(TestClass, 'select'))
    self.assertTrue(isinstance(TestClass.pre_select, types.MethodType))
    self.assertTrue(isinstance(TestClass.pre_addBands, types.MethodType))
    self.assertFalse(hasattr(TestClass, '_pre_addBands'))

    ee.ApiFunction.clearApi(TestClass)
    self.assertFalse(hasattr(TestClass, 'pre_load'))
    self.assertFalse(hasattr(TestClass, 'select'))
    self.assertFalse(hasattr(TestClass, 'pre_select'))
    self.assertTrue(hasattr(TestClass, 'pre_addBands'))
    self.assertFalse(hasattr(TestClass, '_pre_addBands'))

  def testAddFunctions_Inherited(self):
    """Verifies that inherited non-client functions can be overriden."""

    class Base(object):

      def ClientOverride(self):
        pass

    class Child(Base):
      pass

    ee.ApiFunction.importApi(Base, 'Image', 'Image')
    ee.ApiFunction.importApi(Child, 'Image', 'Image')
    self.assertEquals(Base.ClientOverride, Child.ClientOverride)
    self.assertNotEquals(Base.addBands, Child.addBands)


if __name__ == '__main__':
  unittest.main()
