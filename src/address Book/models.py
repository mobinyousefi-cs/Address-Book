#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: models.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Domain models and validation helpers for the Address Book application.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+]?([0-9][\s-]?){7,15}$")


@dataclass(slots=True)
class Contact:
    id: int | None
    name: str
    phone: str = ""
    email: str = ""
    address: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Name is required.")
        if self.email and not EMAIL_RE.match(self.email):
            raise ValueError("Invalid email format.")
        if self.phone and not PHONE_RE.match(self.phone):
            raise ValueError("Invalid phone format.")


__all__ = ["Contact", "EMAIL_RE", "PHONE_RE"]
