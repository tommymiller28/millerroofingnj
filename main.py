from datetime import date

from estimator import JobInput, build_all_package_estimates, apply_pricing_strategy
from contract_generator import save_contract
from exporter import export_to_csv
from salespeople import SALESPERSONS


def ask_string(prompt: str) -> str:
    return input(prompt).strip()


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip() or 0)
        except ValueError:
            print("Please enter a valid number.")


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip() or 0)
        except ValueError:
            print("Please enter a valid whole number.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Please enter y or n.")


def choose_salesperson():
    print("\nSelect salesperson:")
    print("1. Tommy Miller")
    print("2. Kayla Miller")
    print("3. Denise Miller")


    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        return SALESPERSONS["tommy"]
    elif choice == "2":
        return SALESPERSONS["rich"]
    return SALESPERSONS["default"]


def print_package_comparison(pricing):
    print("\nPACKAGE COMPARISON\n")

    for key in ["good", "better", "best"]:
        p = pricing[key]
        print(f"{p['package'].upper()}")
        print(f"  Cost: ${p['cost']:,.2f}")
        print(f"  Selling Price: ${p['price']:,.2f}")
        print(f"  Profit: ${p['profit']:,.2f}")
        print(f"  Margin: {p['margin']:.2f}%")
        print("-" * 45)


def main():
    print("\nROOFING ESTIMATE & PROPOSAL GENERATOR\n")

    salesperson = choose_salesperson()

    customer_name = ask_string("Customer name: ")
    address = ask_string("Property address: ")
    customer_phone = ask_string("Customer phone: ")
    customer_email = ask_string("Customer email: ")

    print("\nEnter roof squares by pitch group:")
    squares_0_7 = ask_float("Squares (0-7 pitch): ")
    squares_8_11 = ask_float("Squares (8-11 pitch): ")
    squares_12_16 = ask_float("Squares (12-16 pitch): ")

    print("\nEnter linear measurements:")
    eaves_feet = ask_float("Eaves feet: ")
    rakes_feet = ask_float("Rakes feet: ")
    ridge_vent_feet = ask_float("Ridge vent feet: ")

    print("\nEnter accessory counts:")
    pipe_flanges = ask_int("Pipe flanges: ")
    bath_vents = ask_int("Bath vents: ")
    kitchen_vents = ask_int("Kitchen vents: ")
    power_fans = ask_int("Power fans: ")
    louvers = ask_int("Louvers: ")

    print("\nEnter repair / flashing / misc counts:")
    plywood_half = ask_int('1/2" plywood sheets: ')
    step_flashing_bundles = ask_int("Step flashing bundles: ")
    skylight_flashings = ask_int("Skylight flashings: ")
    chimney_flashings = ask_int("Chimney flashings: ")
    solar_seal_tubes = ask_int("Solar Seal tubes: ")
    crickets = ask_int("Crickets: ")

    print("\nJob-level charges:")
    roll_off_needed = ask_yes_no("Roll off needed? (y/n): ")
    delivery_needed = ask_yes_no("Delivery needed? (y/n): ")
    promotion_discount = ask_float("Promotion discount amount (enter 0 if none): ")

    markup_percent = ask_float("Desired markup % (example 20): ")

    job = JobInput(
        customer_name=customer_name,
        address=address,
        customer_phone=customer_phone,
        customer_email=customer_email,
        salesperson_name=salesperson["display_name"],
        salesperson_email=salesperson["email"],
        salesperson_phone=salesperson["phone"],
        squares_0_7=squares_0_7,
        squares_8_11=squares_8_11,
        squares_12_16=squares_12_16,
        eaves_feet=eaves_feet,
        rakes_feet=rakes_feet,
        ridge_vent_feet=ridge_vent_feet,
        pipe_flanges=pipe_flanges,
        bath_vents=bath_vents,
        kitchen_vents=kitchen_vents,
        power_fans=power_fans,
        louvers=louvers,
        plywood_half=plywood_half,
        step_flashing_bundles=step_flashing_bundles,
        skylight_flashings=skylight_flashings,
        chimney_flashings=chimney_flashings,
        solar_seal_tubes=solar_seal_tubes,
        crickets=crickets,
        roll_off_needed=roll_off_needed,
        delivery_needed=delivery_needed,
        promotion_discount=promotion_discount,
    )

    estimates = build_all_package_estimates(job)
    pricing = apply_pricing_strategy(estimates, markup_percent)

    print_package_comparison(pricing)

    while True:
        selected = ask_string("Choose package (good / better / best): ").lower()
        if selected in pricing:
            break
        print("Invalid package. Please choose good, better, or best.")

    selected_data = pricing[selected]
    selected_estimate = selected_data["estimate"]
    selected_price = selected_data["price"]

    contract_path = save_contract(job, selected_estimate, selected_price)
    csv_path = export_to_csv(job, selected_estimate, selected_price)

    print(f"\nContract generated successfully: {contract_path}")
    print(f"Estimate CSV exported successfully: {csv_path}")


if __name__ == "__main__":
    main()