# Address Book (Tkinter + SQLite)

A clean, production‑ready Python project for a desktop Address Book built with Tkinter (GUI) and SQLite (persistence). Add, view, edit, delete, and search contacts with a simple, responsive interface.

> **Stack**: Python 3.9+, Tkinter/ttk, SQLite (stdlib), pytest, Ruff, Black, GitHub Actions CI.

---

## ✨ Features
- Create, view, update, and delete contacts
- Search by name, phone, or email
- SQLite storage (file DB) with auto‑migration
- Lightweight, no external runtime deps
- Tests for models and storage
- Dev tooling preconfigured: Ruff + Black + pytest + CI

---

## 📦 Project Structure
```
address-book/
├── src/
│   └── address_book/
│       ├── __init__.py
│       ├── main.py
│       ├── gui.py
│       ├── models.py
│       └── storage.py
├── tests/
│   ├── test_models.py
│   └── test_storage.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── LICENSE
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🔧 Installation
```bash
# Clone
git clone https://github.com/your-username/address-book.git
cd address-book

# (Optional) Create a venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# Install (runtime deps are stdlib; dev deps via extras)
pip install -e .[dev]
```

> Tkinter ships with most CPython installs. On some Linux distros: `sudo apt-get install python3-tk`.

---

## ▶️ Run the App
```bash
python -m address_book
```
This launches the Tkinter GUI and creates `address_book.db` in the project folder on first run.

---

## 🧪 Run Tests
```bash
pytest -q
```

---

## 🧰 Developer Tooling
- **Format**: `black .`
- **Lint**: `ruff check .`
- **Type check (optional)**: `pyright` (add if desired)
- **CI**: GitHub Actions runs lint + tests on every push/PR to `main`.

---

## 💾 Data Model
- `Contact`: `id`, `name`, `phone`, `email`, `address`, `created_at`
- SQLite auto‑migrates schema via `storage.init_db()` on startup.

---

## 🖥️ Screens (quick tour)
- **Toolbar**: Add, Edit, Delete, Refresh, Search
- **Grid**: Sortable `ttk.Treeview` of contacts
- **Dialog**: Add/Edit contact with validation

---

## 📜 License
MIT — see [LICENSE](./LICENSE).

---

## 👤 Author
**Mobin Yousefi** — [GitHub](https://github.com/mobinyousefi-cs)

---

## 🚀 Roadmap (nice‑to‑haves)
- Import/Export CSV
- Undo/redo stack
- Multi‑select delete
- Tagging & advanced filters
- Theming (ttk themes / ttkbootstrap)

