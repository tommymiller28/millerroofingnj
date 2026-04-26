import math
from dataclasses import dataclass, field
from typing import List
from pricing import PRICE_CATALOG, PACKAGE_RULES


@dataclass
class JobInput:
    customer_name: str
    address: str
    customer_phone: str
    customer_email: str

    salesperson_name: str
    salesperson_email: str
    salesperson_phone: str

    squares_0_7: float
    squares_8_11: float
    squares_12_16: float

    eaves_feet: float
    rakes_feet: float
    ridge_vent_feet: float

    pipe_flanges: int
    bath_vents: int
    kitchen_vents: int
    power_fans: int
    louvers: int

    plywood_half: int
    step_flashing_bundles: int
    skylight_flashings: int
    chimney_flashings: int
    solar_seal_tubes: int
    crickets: int

    roll_off_needed: bool
    delivery_needed: bool
    promotion_discount: float

    selected_package: str = "good"


@dataclass
class EstimateLine:
    name: str
    quantity: float
    unit: str
    unit_price: float
    total: float


@dataclass
class EstimateResult:
    package_name: str
    shingle_name: str
    warranty_name: str
    total_squares: float
    lines: List[EstimateLine] = field(default_factory=list)
    subtotal: float = 0.0


def _round(value):
    return round(value, 2)


def _ceil_div(x, y):
    return math.ceil(x / y) if x > 0 else 0


def add(result, name, qty, key):
    if qty <= 0:
        return
    item = PRICE_CATALOG[key]
    total = _round(qty * item.unit_price)
    result.lines.append(EstimateLine(name, qty, item.unit, item.unit_price, total))


def calculate_total_squares(job):
    return job.squares_0_7 + job.squares_8_11 + job.squares_12_16


def calculate_labor(result, job):
    add(result, "Labor (0-7)", job.squares_0_7, "labor_0_7_per_sq")
    add(result, "Labor (8-11)", job.squares_8_11, "labor_8_11_per_sq")
    add(result, "Labor (12-16)", job.squares_12_16, "labor_12_16_per_sq")


def calculate_disposal(result, total_squares):
    add(result, "Disposal", total_squares, "disposal_per_sq")


def calculate_starter_and_drip(result, job):
    total_ft = job.eaves_feet + job.rakes_feet
    starter = _ceil_div(total_ft, 120)
    drip = _ceil_div(total_ft, 10)

    add(result, "Starter Strip", starter, "starter_bundle")
    add(result, "Drip Edge", drip, "drip_edge_piece")


def calculate_caps(result, job, package):
    bundles = _ceil_div(job.ridge_vent_feet, package["caps_coverage_ft"])
    add(result, PRICE_CATALOG[package["caps_key"]].name, bundles, package["caps_key"])
    add(result, "Caps Labor", bundles, "caps_labor_bundle")


def calculate_underlayment(result, total_squares, package):
    rolls = _ceil_div(total_squares, 10)
    add(result, PRICE_CATALOG[package["underlayment_key"]].name, rolls, package["underlayment_key"])


def calculate_ice(result, total_squares, package):
    rolls = math.ceil(total_squares * package["ice_rolls_per_sq"]) if total_squares > 0 else 0
    add(result, PRICE_CATALOG[package["ice_key"]].name, rolls, package["ice_key"])


def calculate_ridge_vent(result, job):
    rolls = _ceil_div(job.ridge_vent_feet, 30)
    add(result, "Cobra Ridge Runner", rolls, "ridge_runner_roll")


def calculate_coil_nails(result, total_squares):
    boxes = _ceil_div(total_squares, 15)
    add(result, "Coil Nails", boxes, "coil_nails_box")


def calculate_warranty(result, total_squares, package):
    if package["warranty_is_flat"]:
        add(result, package["warranty_type"], 1, package["warranty_key"])
    else:
        add(result, package["warranty_type"], total_squares, package["warranty_key"])


def build_estimate(job: JobInput) -> EstimateResult:
    package = PACKAGE_RULES[job.selected_package]
    total_squares = calculate_total_squares(job)

    result = EstimateResult(
        package_name=job.selected_package.capitalize(),
        shingle_name=package["shingle_name"],
        warranty_name=package["warranty_type"],
        total_squares=total_squares,
    )

    calculate_labor(result, job)
    calculate_disposal(result, total_squares)

    if job.roll_off_needed:
        add(result, "Roll Off", 1, "roll_off_fee")
    if job.delivery_needed:
        add(result, "Delivery", 1, "delivery_fee")

    add(result, package["shingle_name"], total_squares, package["shingle_key"])

    calculate_caps(result, job, package)
    calculate_starter_and_drip(result, job)
    calculate_underlayment(result, total_squares, package)
    calculate_ice(result, total_squares, package)
    calculate_ridge_vent(result, job)
    calculate_coil_nails(result, total_squares)

    add(result, "Pipe Flanges", job.pipe_flanges, "pipe_flange_each")
    add(result, "Bath Vents", job.bath_vents, "bath_vent_each")
    add(result, "Kitchen Vents", job.kitchen_vents, "kitchen_vent_each")
    add(result, "Power Fans", job.power_fans, "power_fan_each")
    add(result, "Louvers", job.louvers, "louver_each")

    add(result, '1/2" Plywood', job.plywood_half, "plywood_half_each")
    add(result, "Plywood Labor", job.plywood_half, "plywood_half_labor_each")
    add(result, "Step Flashing", job.step_flashing_bundles, "step_flashing_bundle")
    add(result, "Skylight Flashing", job.skylight_flashings, "skylight_flashings_each" if False else "skylight_flashing_each")
    add(result, "Chimney Flashing", job.chimney_flashings, "chimney_flashing_labor_each")
    add(result, "Solar Seal", job.solar_seal_tubes, "solar_seal_each")
    add(result, "Cricket", job.crickets, "cricket_each")

    calculate_warranty(result, total_squares, package)

    result.subtotal = _round(sum(line.total for line in result.lines))

    if job.promotion_discount > 0:
        result.subtotal = _round(result.subtotal - job.promotion_discount)

    return result


def build_all_package_estimates(job):
    results = {}
    for pkg in ["good", "better", "best"]:
        j = JobInput(**vars(job))
        j.selected_package = pkg
        results[pkg] = build_estimate(j)
    return results


def apply_pricing_strategy(estimates, markup_percent):
    results = {}
    for key, est in estimates.items():
        cost = est.subtotal
        price = cost * (1 + markup_percent / 100)
        profit = price - cost
        margin = (profit / price) * 100 if price > 0 else 0

        results[key] = {
            "package": est.package_name,
            "cost": round(cost, 2),
            "price": round(price, 2),
            "profit": round(profit, 2),
            "margin": round(margin, 2),
            "estimate": est,
        }
    return results