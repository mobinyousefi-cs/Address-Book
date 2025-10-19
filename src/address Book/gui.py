#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: gui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Tkinter GUI: main window, toolbar, grid (ttk.Treeview), dialogs for add/edit, and a search bar.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from dataclasses import asdict
from datetime import datetime

from .models import Contact
from .storage import (
    open_db,
    add_contact,
    update_contact,
    delete_contact,
    list_contacts,
    search_contacts,
)


class ContactDialog(simpledialog.Dialog):
    def __init__(self, parent, title: str, contact: Contact | None = None):
        self._contact = contact
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Name *").grid(row=0, column=0, sticky=tk.W, padx=6, pady=6)
        ttk.Label(master, text="Phone").grid(row=1, column=0, sticky=tk.W, padx=6, pady=6)
        ttk.Label(master, text="Email").grid(row=2, column=0, sticky=tk.W, padx=6, pady=6)
        ttk.Label(master, text="Address").grid(row=3, column=0, sticky=tk.W, padx=6, pady=6)

        self.name_var = tk.StringVar(value=self._contact.name if self._contact else "")
        self.phone_var = tk.StringVar(value=self._contact.phone if self._contact else "")
        self.email_var = tk.StringVar(value=self._contact.email if self._contact else "")
        self.address_var = tk.StringVar(value=self._contact.address if self._contact else "")

        ttk.Entry(master, textvariable=self.name_var, width=40).grid(row=0, column=1, padx=6, pady=6)
        ttk.Entry(master, textvariable=self.phone_var, width=40).grid(row=1, column=1, padx=6, pady=6)
        ttk.Entry(master, textvariable=self.email_var, width=40).grid(row=2, column=1, padx=6, pady=6)
        ttk.Entry(master, textvariable=self.address_var, width=40).grid(row=3, column=1, padx=6, pady=6)
        return master

    def validate(self):
        try:
            c = Contact(
                id=self._contact.id if self._contact else None,
                name=self.name_var.get().strip(),
                phone=self.phone_var.get().strip(),
                email=self.email_var.get().strip(),
                address=self.address_var.get().strip(),
            )
            c.validate()
            self._validated = c
            return True
        except Exception as e:
            messagebox.showerror("Validation error", str(e), parent=self)
            return False

    def apply(self):
        self.result = self._validated


class AddressBookApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master.title("Address Book")
        self.master.geometry("800x480")
        self.master.minsize(720, 420)
        self.pack(fill=tk.BOTH, expand=True)

        self._build_toolbar()
        self._build_search()
        self._build_tree()
        self.refresh()

    # --- UI builders ---
    def _build_toolbar(self):
        bar = ttk.Frame(self)
        bar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(bar, text="Add", command=self.on_add).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(bar, text="Edit", command=self.on_edit).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(bar, text="Delete", command=self.on_delete).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(bar, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=4, pady=4)

    def _build_search(self):
        row = ttk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(row, text="Search:").pack(side=tk.LEFT, padx=6)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(row, textvariable=self.search_var)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6, pady=4)
        ent.bind("<Return>", lambda _e: self.on_search())
        ttk.Button(row, text="Go", command=self.on_search).pack(side=tk.LEFT, padx=4)
        ttk.Button(row, text="Clear", command=self.on_clear_search).pack(side=tk.LEFT, padx=4)

    def _build_tree(self):
        cols = ("id", "name", "phone", "email", "address", "created_at")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")
        self.tree.heading("address", text="Address")
        self.tree.heading("created_at", text="Created")

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=180)
        self.tree.column("phone", width=120)
        self.tree.column("email", width=200)
        self.tree.column("address", width=240)
        self.tree.column("created_at", width=160, anchor=tk.CENTER)

        yscroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    # --- actions ---
    def refresh(self):
        self.populate(list_contacts)

    def populate(self, source_fn, *args):
        for row in self.tree.get_children():
            self.tree.delete(row)
        with open_db() as conn:
            for c in source_fn(conn, *args):
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        c.id,
                        c.name,
                        c.phone,
                        c.email,
                        c.address,
                        c.created_at.strftime("%Y-%m-%d %H:%M"),
                    ),
                )

    def selected_contact_id(self) -> int | None:
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0]) if values else None

    def on_add(self):
        dlg = ContactDialog(self.master, "Add Contact")
        if dlg.result:
            with open_db() as conn:
                new_id = add_contact(conn, dlg.result)
            self.refresh()
            messagebox.showinfo("Added", f"Contact added with ID {new_id}")

    def on_edit(self):
        cid = self.selected_contact_id()
        if cid is None:
            messagebox.showwarning("No selection", "Please select a contact to edit.")
            return
        # Load current values from row
        cur = self.tree.item(self.tree.selection()[0], "values")
        contact = Contact(
            id=int(cur[0]),
            name=cur[1],
            phone=cur[2],
            email=cur[3],
            address=cur[4],
        )
        dlg = ContactDialog(self.master, "Edit Contact", contact)
        if dlg.result:
            with open_db() as conn:
                update_contact(conn, dlg.result)
            self.refresh()
            messagebox.showinfo("Updated", "Contact updated successfully.")

    def on_delete(self):
        cid = self.selected_contact_id()
        if cid is None:
            messagebox.showwarning("No selection", "Please select a contact to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete selected contact?"):
            with open_db() as conn:
                delete_contact(conn, cid)
            self.refresh()

    def on_search(self):
        q = self.search_var.get().strip()
        if not q:
            self.refresh()
            return
        self.populate(search_contacts, q)

    def on_clear_search(self):
        self.search_var.set("")
        self.refresh()
