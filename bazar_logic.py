ITEMS = [
    {"name": "Rice", "A": 120, "B": 115},
    {"name": "Oil", "A": 150, "B": 145},
    {"name": "Lentils", "A": 95, "B": 100},
    {"name": "Eggs", "A": 80, "B": 85},
    {"name": "Vegetables", "A": 70, "B": 65},
]


def discounted_price(price, use_coupon):
    """Returns round(price * 0.90, 2) if coupon is applied; otherwise returns price."""
    if use_coupon:
        return round(price * 0.90, 2)
    return price


def can_buy(remaining, cost):
    """Returns True only when remaining >= cost."""
    return remaining >= cost


def remaining_budget(remaining, cost):
    """Returns the nonnegative new budget after a valid purchase."""
    if can_buy(remaining, cost):
        return round(remaining - cost, 2)
    return remaining


def calculate_savings(reference_total, paid):
    """Returns round(reference_total - paid, 2)."""
    return round(reference_total - paid, 2)


def has_affordable_option(item, remaining, coupon_available):
    """Checks if at least one combination of shop + coupon is affordable."""
    for shop in ("A", "B"):
        base_price = item[shop]
        if can_buy(remaining, base_price):
            return True
        if coupon_available and can_buy(remaining, discounted_price(base_price, True)):
            return True
    return False


def run_market():
    """Uses a for loop over five items and handles retry/coupon use."""
    budget = 505.0
    coupon_available = True
    total_paid = 0.0
    reference_total = sum(max(item["A"], item["B"]) for item in ITEMS)

    print("=== BAZAR BOSS: BUDGET SHOPPING ===")
    print(f"Starting Budget: {budget:.2f} BDT | 10% Coupon Available: Yes\n")
    print("Item List:")
    for item in ITEMS:
        print(f" - {item['name']}: Shop A = {item['A']} BDT | Shop B = {item['B']} BDT")
    print("-" * 45)

    for item in ITEMS:
        # Check if game can continue before prompting
        if not has_affordable_option(item, budget, coupon_available):
            print(f"\n[GAME OVER] Cannot afford {item['name']} with {budget:.2f} BDT left.")
            return

        while True:
            print(f"\nBuying: {item['name']} (Shop A: {item['A']} | Shop B: {item['B']})")
            print(f"Remaining Budget: {budget:.2f} BDT | Coupon Available: {'Yes' if coupon_available else 'No'}")

            shop = input("Choose shop (A/B): ").strip().upper()
            if shop not in ("A", "B"):
                print("Invalid choice. Please enter A or B.")
                continue

            use_coupon = False
            if coupon_available:
                c_input = input("Apply 10% discount coupon? (y/n): ").strip().lower()
                if c_input not in ("y", "n"):
                    print("Invalid choice. Please enter y or n.")
                    continue
                use_coupon = (c_input == "y")

            cost = discounted_price(item[shop], use_coupon)

            if can_buy(budget, cost):
                budget = remaining_budget(budget, cost)
                total_paid = round(total_paid + cost, 2)
                if use_coupon:
                    coupon_available = False
                print(f"Purchased {item['name']} from Shop {shop} for {cost:.2f} BDT.")
                break
            else:
                print(f"Rejected! {cost:.2f} BDT exceeds remaining budget ({budget:.2f} BDT). Try another option.")

    savings = calculate_savings(reference_total, total_paid)
    print("\n" + "=" * 45)
    print("CONGRATULATIONS! All 5 items purchased.")
    print(f"Total Paid:      {total_paid:.2f} BDT")
    print(f"Budget Left:     {budget:.2f} BDT")
    print(f"Total Savings:   {savings:.2f} BDT (vs {reference_total:.2f} BDT max benchmark)")
    print("=" * 45)


if __name__ == "__main__":
    run_market()