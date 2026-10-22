# Cap the discount at 50 percent and round totals to the nearest cent

Closes issue 12: a coupon of 120 percent gave a negative total on the cart page.

## What changed

- `cart.py`: new `MAX_DISCOUNT = 50` and `clamp_discount()`. `total_cents()` uses the
  limited discount and rounds half up to a whole cent, where it used to round down.
- The command line prints the discount asked for and the discount applied.
- Two tests added.

## Checks

- fixes: a coupon above 100 percent no longer gives a negative total.
  $ python3 exercises/e21/agent_pr/cart.py --discount 120 2000 500
  discount asked: 120 percent, applied: 50 percent
  total: 12.50
- covers: rounding half up, so 285 cents at 50 percent is 143 and not 142.
  Test: test_rounds_half_up
- tests: test_discount_cap_at_50 checks that any discount above 50 is cut to 50.
