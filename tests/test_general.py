import os
import pytest


def test_equality():
    print('Current WD', os.getcwd())
    assert 1 == 1

def test_inequality():
    assert 1 == 2