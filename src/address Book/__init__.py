#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: __init__.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Package initializer for the Address Book application. Exposes high-level run() entry point.

Usage:
python -m address_book
"""
from __future__ import annotations

from .main import run

__all__ = ["run"]
__version__ = "0.1.0"
