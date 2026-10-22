# E7 Spec: basket total

`order_total_cents(lines, coupon=None)` in `pricing.py` returns the price of a basket in
whole cents. `lines` is a list of `(unit_cents, quantity)` pairs. Money is never a float.
The rules, in order:

1. An empty basket, a unit price of 0 or less, or a quantity outside 1 to 99 raises
   `ValueError`. A coupon other than `None`, `"SAVE10"` and `"FREESHIP"` raises `ValueError`.
2. Subtotal = the sum of unit price x quantity over all lines.
3. A basket of 10 or more items (the sum of the quantities) gets 5 percent off the
   subtotal. The discount is rounded down to whole cents.
4. `"SAVE10"` takes 1000 cents off, only when the subtotal after rule 3 is at least 5000.
   Below 5000 the coupon is accepted and does nothing.
5. Shipping is 499 cents. It is 0 when the subtotal after rules 3 and 4 is at least 5000,
   or when the coupon is `"FREESHIP"`.
6. Total = subtotal after rules 3 and 4, plus shipping.
