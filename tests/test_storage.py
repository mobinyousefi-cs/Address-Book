#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: test_storage.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================
"""
from __future__ import annotations

import sqlite3
from address_book.models import Contact
from address_book.storage import (
    init_db,
    add_contact,
    update_contact,
    delete_contact,
    get_contact,
    list_contacts,
    search_contacts,
)


def fresh_conn():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    return conn


def test_crud_cycle():
    conn = fresh_conn()
    c = Contact(id=None, name="Bob", phone="1234567", email="bob@example.com", address="Somewhere")
    new_id = add_contact(conn, c)

    got = get_contact(conn, new_id)
    assert got is not None and got.name == "Bob"

    got.name = "Bobby"
    update_contact(conn, got)
    got2 = get_contact(conn, new_id)
    assert got2 is not None and got2.name == "Bobby"

    delete_contact(conn, new_id)
    assert get_contact(conn, new_id) is None


def test_list_and_search():
    conn = fresh_conn()
    ids = []
    ids.append(add_contact(conn, Contact(None, "Alice", "111", "a@example.com", "A st")))
    ids.append(add_contact(conn, Contact(None, "Charlie", "222", "c@example.com", "C st")))

    rows = list_contacts(conn)
    assert len(rows) == 2

    res = search_contacts(conn, "ali")
    assert len(res) == 1 and res[0].name == "Alice"
