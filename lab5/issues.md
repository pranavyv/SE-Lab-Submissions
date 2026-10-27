# Issues Found — warehouse_stock_manager.py

Baseline: Pylint 4.48/10, Bandit 5 findings (1 High, 2 Medium, 2 Low), Flake8 19 findings.
Final: Pylint 10.00/10, Bandit 0, Flake8 0. Line numbers refer to the **original** file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval` on supervisor formula (Bandit B307 Medium, Pylint W0123) | Security | 62 | `eval(formula, ...)` lets anyone with the password run arbitrary Python (`__import__('os').system(...)`); the `{"current": ...}` globals dict is not a sandbox. | Replaced with `_safe_eval`: parses with `ast` and only allows numbers, `current`, `+ - * / // %` and unary +/-. Anything else raises `ValueError`. Negative results are rejected. |
| `eval` for a print call (Bandit B307 Medium, Pylint W0123) | Security | 80 | `eval("print('stock audit complete')")` is pointless and dangerous. | Replaced with a plain `print(...)`. |
| MD5 for SKU fingerprint (Bandit B324 **High**) | Security | 31 | `hashlib.md5(...)` flagged as weak for security use. It is only a label fingerprint, so a different hash would change every printed bin label. | `hashlib.md5(..., usedforsecurity=False)` plus a comment stating it is not a security control. Labels stay identical (`a616ce`, `4f4adc`). |
| Hardcoded password (Bandit B105 Low) | Security | 10 | `SUPERVISOR_PASSWORD = "wh-admin-1234"` in source, and the same literal repeated in `main()`. | Read from the `WAREHOUSE_SUPERVISOR_PASSWORD` environment variable; compared with `hmac.compare_digest`. If unset, adjustments are denied. |
| Bare `except: pass` (Bandit B110 Low, Pylint W0702, Flake8 E722) | Bug | 23-24 | Swallows every error silently, so `removeStock("GHOST-9", 1)` fails with no trace. | Removed the try/except. `remove_stock` raises `KeyError` for unknown SKUs; the caller logs it. |
| Mutable default argument (Pylint W0102) | Bug | 12 | `history=[]` is shared across all calls, so history leaks between unrelated calls. | Default is `None`; a fresh list is created per call and returned. |
| Negative / invalid quantity accepted (no tool flags it) | Bug | 15, 69 | `addStock("WID-002", -4)` stored -4 units and showed it in the demo output. | `add_stock` rejects non-positive or non-integer quantities with `ValueError`. |
| Non-string SKU accepted (no tool flags it) | Bug | 15, 70 | `addStock(404, 15)` stored an int key; after a JSON save/load the key would silently become `"404"`. | `add_stock` requires a non-empty `str` SKU. |
| Over-removal silently deletes stock (no tool flags it) | Bug | 20-22, 73 | Removing 500 from a SKU holding 28 drove it negative, then deleted it with no error. | `remove_stock` raises `ValueError` if `qty` exceeds stock; the SKU is deleted only at exactly 0. |
| Non-snake_case function names (Pylint C0103 x8) | Style | 12-67 | `addStock`, `removeStock`, `getStock`, `skuChecksum`, `loadStock`, `saveStock`, `printReport`, `checkReorder`, `applyAdjustment`. | Renamed to snake_case. |
| Missing docstrings (Pylint C0114, C0116 x9) | Style | 1, 12-67 | No module or function docstrings. | Added a docstring to the module and every function. |
| Files opened without `with` / encoding (Pylint R1732, W1514) | Bug | 34, 40, 63 | Handles leak if an exception occurs before `close()`; encoding is platform-dependent. | `with open(..., encoding="utf-8")` everywhere. |
| `global` statement (Pylint W0603) | Design | 35 | `loadStock` rebinds the module global. | Load into a local, then `clear()` + `update()` the existing dict. |
| Unused variable `total_units` (Pylint W0612, Flake8 F841) | Dead code | 54 | Computed and never used. | Removed; `check_reorder` is now a list comprehension. |
| Unused imports `logging`, `os` (Pylint W0611, Flake8 F401) | Dead code | 2, 4 | Imported and never used. | Both are now genuinely used (`logging` for warnings, `os` for the env var). |
| `%` string formatting (Pylint C0209) | Style | 16 | Old-style formatting. | f-strings. |
| Trailing whitespace (Pylint C0303, Flake8 W291) | Style | 54 | Whitespace after the statement. | Line removed during refactor. |
| Line too long (Pylint C0301, Flake8 E501 x3) | Style | 16, 47, 64 | Lines over 79 characters. | Wrapped to 79 characters. |
| Blank lines around functions (Flake8 E302 x9, E305) | Style | 12-82 | One blank line instead of two between top-level definitions and before the module-level call. | Two blank lines everywhere. |
| `main()` runs on import (no tool flags it) | Design | 82 | Importing the module executes the demo. | Wrapped in `if __name__ == "__main__":`. |
