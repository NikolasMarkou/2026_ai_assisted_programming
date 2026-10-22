## Order handling (`legacy.py`)

`process_orders()` turns a list of order dicts into invoice lines and a grand total in
cents. It calls `_price_items()` for the item subtotal, `_discount()` for a coupon and
`_bill_order()` for one order, which uses `quote_shipping()` for the delivery fee and
`check_country()` for the tax rate. `check_country()` returns the tax rate in percent
for the order's country, or -1 when the country is not in the tax table.

`load_coupons()` reads a coupon file: one code per line, blank lines and lines that
start with # are ignored, codes are upper-cased. `summary()` returns one sentence with
the number of billed orders and the total in euros.

Orders without items or with an unknown country are skipped and get a line that says
why. An item with a quantity or a price of 0 or less is skipped on its own. Output
mode is `text` (default) or `csv`.
