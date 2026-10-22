# E8 Spec: shipping price

`shipping_cents(weight_g, distance_km, express=False)` returns the price of one parcel in
whole cents. Money is never a float. The rules, in order:

1. Weight price. Up to and including 2000 g: 400 cents. Over 2000 g, up to and including
   10000 g: 750 cents. Over 10000 g, up to and including 30000 g: 1200 cents.
2. A weight above 30000 g, a weight of 0 or less, or a distance below 0 raises `ValueError`.
3. Distance charge. The first 100 km are free. Each further km adds 3 cents.
4. Subtotal = weight price + distance charge.
5. Round the subtotal up to the next multiple of 5 cents. A subtotal that already is a
   multiple of 5 stays as it is.
6. Express delivery adds 25 percent of the ROUNDED subtotal, rounded up to whole cents.
7. The price is the rounded subtotal plus the express charge (0 for standard delivery).
