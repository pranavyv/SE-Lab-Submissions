"""Warehouse stock manager: receive, issue, report and adjust stock per SKU."""
import ast
import hashlib
import hmac
import json
import logging
import operator
import os
from datetime import datetime

warehouse_stock = {}
AUDIT_FILE = "warehouse_audit.log"
SUPERVISOR_ENV_KEY = "WAREHOUSE_SUPERVISOR_PASSWORD"

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def add_stock(sku, qty, history=None):
    """Receive `qty` units of `sku`; reject bad SKUs and qty <= 0."""
    if not isinstance(sku, str) or not sku:
        raise ValueError(f"invalid SKU: {sku!r}")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError(f"quantity must be a positive integer, got {qty!r}")
    if history is None:
        history = []
    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty
    history.append(f"{datetime.now()}: Received {qty} units of {sku}")
    return history


def remove_stock(sku, qty):
    """Issue `qty` units of `sku`; never lets stock go below zero."""
    if sku not in warehouse_stock:
        raise KeyError(f"unknown SKU: {sku!r}")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError(f"quantity must be a positive integer, got {qty!r}")
    if qty > warehouse_stock[sku]:
        raise ValueError(
            f"cannot remove {qty} of {sku}: "
            f"only {warehouse_stock[sku]} in stock")
    warehouse_stock[sku] -= qty
    if warehouse_stock[sku] == 0:
        del warehouse_stock[sku]


def get_stock(sku):
    """Return units on hand for `sku` (0 if the SKU is not stocked)."""
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """Short fingerprint for printed bin labels (not a security control)."""
    return hashlib.md5(sku.encode(), usedforsecurity=False).hexdigest()[:6]


def load_stock(file="warehouse.json"):
    """Replace the in-memory stock with the contents of a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    warehouse_stock.clear()
    warehouse_stock.update(data)


def save_stock(file="warehouse.json"):
    """Write the in-memory stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(warehouse_stock, handle)


def print_report():
    """Print every SKU with its quantity and label checksum."""
    print("Warehouse Stock Report")
    for sku, units in warehouse_stock.items():
        print(sku, "->", units, "units  [chk:", sku_checksum(str(sku)) + "]")


def check_reorder(threshold=10):
    """Return the SKUs whose stock is below `threshold`."""
    return [sku for sku, units in warehouse_stock.items() if units < threshold]


def _safe_eval(formula, current):
    """Evaluate a basic arithmetic formula in terms of `current` only."""
    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if (isinstance(node, ast.Constant)
                and isinstance(node.value, (int, float))
                and not isinstance(node.value, bool)):
            return node.value
        if isinstance(node, ast.Name) and node.id == "current":
            return current
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            return _BIN_OPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](walk(node.operand))
        raise ValueError("unsupported expression in formula")
    try:
        return walk(ast.parse(formula, mode="eval"))
    except (SyntaxError, ZeroDivisionError) as err:
        raise ValueError(f"bad formula {formula!r}: {err}") from err


def apply_adjustment(sku, formula, password):
    """Set `sku` to the result of `formula` (e.g. "current * 2").

    Supervisor only.

    Returns True if applied, False if the password was wrong or unset.
    """
    expected = os.environ.get(SUPERVISOR_ENV_KEY, "")
    if not expected or not hmac.compare_digest(
            password.encode(), expected.encode()):
        logging.warning("apply_adjustment: access denied")
        return False
    new_value = int(_safe_eval(formula, warehouse_stock.get(sku, 0)))
    if new_value < 0:
        raise ValueError(f"adjustment would make {sku} negative ({new_value})")
    warehouse_stock[sku] = new_value
    with open(AUDIT_FILE, "a", encoding="utf-8") as audit:
        audit.write(
            f"adjusted {sku} using formula {formula} at {datetime.now()}\n")
    return True


def main():
    """Run a short demo of the stock manager."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s")
    demo_steps = [
        (add_stock, ("WID-001", 40)),
        (add_stock, ("WID-002", -4)),     # rejected: negative quantity
        (add_stock, (404, 15)),           # rejected: SKU must be a string
        (remove_stock, ("WID-001", 12)),
        (remove_stock, ("GHOST-9", 1)),   # rejected: unknown SKU
        (remove_stock, ("WID-001", 500)),  # rejected: more than in stock
    ]
    for action, args in demo_steps:
        try:
            action(*args)
        except (ValueError, KeyError) as err:
            logging.warning("%s%s rejected: %s", action.__name__, args, err)
    print("WID-001 stock:", get_stock("WID-001"))
    print("Needs reorder:", check_reorder())
    try:
        apply_adjustment(
            "WID-002", "current + 25", os.environ.get(SUPERVISOR_ENV_KEY, ""))
    except ValueError as err:
        logging.warning("adjustment rejected: %s", err)
    save_stock()
    load_stock()
    print_report()
    print("stock audit complete")


if __name__ == "__main__":
    main()
