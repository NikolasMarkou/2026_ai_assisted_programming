# E8 Spec examples

Three input and output pairs from the shop owner. They follow the rules in `spec.md`.
Work them out by hand once before you trust any code, yours or the agent's.

1. `shipping_cents(2000, 50)` returns `400`. A parcel of exactly 2000 g is in the lightest tier.
2. `shipping_cents(1500, 127, express=True)` returns `607`. Subtotal 400 + 27 x 3 = 481,
   rounded to 485, express charge 25 percent of 485 = 121.25, rounded up to 122.
3. `shipping_cents(5000, 100)` returns `750`.
