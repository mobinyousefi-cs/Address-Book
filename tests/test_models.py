#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: test_models.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================
"""
from __future__ import annotations

import pytest
from address_book.models import Contact


def test_contact_validation_ok():
    c = Contact(id=None, name="Alice", phone="+1-555-1234", email="a@b.com")
    c.validate()  # should not raise


def test_contact_validation_requires_name():
    with pytest.raises(ValueError):
        Contact(id=None, name=" ").validate()


def test_contact_validation_email():
    with pytest.raises(ValueError):
        Contact(id=None, name="Alice", email="bad@@example").validate()


def test_contact_validation_phone():
    with pytest.raises(ValueError):
        Contact(id=None, name="Alice", phone="abc").validate()
