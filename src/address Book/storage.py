#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: storage.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
SQLite persistence layer with automatic schema migration and CRUD operations.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
import sqlite3
from typing import Iterable, Iterator, Optional

from .models import Contact


DEFAULT_DB_PATH = "address_book.db"


def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            address TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


@contextmanager
def open_db(path: str = DEFAULT_DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(path)
    try:
        init_db(conn)
        yield conn
    finally:
        conn.close()


def _row_to_contact(row: sqlite3.Row) -> Contact:
    return Contact(
        id=row[0],
        name=row[1],
        phone=row[2],
        email=row[3],
        address=row[4],
        created_at=datetime.fromisoformat(row[5]),
    )


def add_contact(conn: sqlite3.Connection, contact: Contact) -> int:
    contact.validate()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone, email, address, created_at) VALUES (?, ?, ?, ?, ?)",
        (
            contact.name.strip(),
            contact.phone.strip(),
            contact.email.strip(),
            contact.address.strip(),
            contact.created_at.isoformat(),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def update_contact(conn: sqlite3.Connection, contact: Contact) -> None:
    if contact.id is None:
        raise ValueError("Cannot update contact without id")
    contact.validate()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
        (
            contact.name.strip(),
            contact.phone.strip(),
            contact.email.strip(),
            contact.address.strip(),
            contact.id,
        ),
    )
    conn.commit()


def delete_contact(conn: sqlite3.Connection, contact_id: int) -> None:
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()


def get_contact(conn: sqlite3.Connection, contact_id: int) -> Optional[Contact]:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, phone, email, address, created_at FROM contacts WHERE id=?",
        (contact_id,),
    )
    row = cur.fetchone()
    return _row_to_contact(row) if row else None


def list_contacts(conn: sqlite3.Connection) -> list[Contact]:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, phone, email, address, created_at FROM contacts ORDER BY name COLLATE NOCASE"
    )
    rows = cur.fetchall()
    return [_row_to_contact(r) for r in rows]


def search_contacts(conn: sqlite3.Connection, query: str) -> list[Contact]:
    q = f"%{query.strip()}%"
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, name, phone, email, address, created_at
        FROM contacts
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        ORDER BY name COLLATE NOCASE
        """,
        (q, q, q),
    )
    rows = cur.fetchall()
    return [_row_to_contact(r) for r in rows]


__all__ = [
    "DEFAULT_DB_PATH",
    "open_db",
    "init_db",
    "add_contact",
    "update_contact",
    "delete_contact",
    "get_contact",
    "list_contacts",
    "search_contacts",
]
