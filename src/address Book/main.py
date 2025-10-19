#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Address Book (Tkinter + SQLite)
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-19
Updated: 2025-10-19
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Module entry point. Bootstraps Tkinter app and runs the main event loop.
"""
from __future__ import annotations

import tkinter as tk
from .gui import AddressBookApp


def run() -> None:
    root = tk.Tk()
    # Use ttk theme if available
    try:
        import tkinter.ttk as ttk
        if "clam" in ttk.Style().theme_names():
            ttk.Style().theme_use("clam")
    except Exception:
        pass
    AddressBookApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
