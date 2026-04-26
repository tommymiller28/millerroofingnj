from dataclasses import dataclass
from typing import Dict


@dataclass
class LineItem:
    name: str
    unit: str
    unit_price: float


PRICE_CATALOG: Dict[str, LineItem] = {
    # labor / base charges
    "labor_0_7_per_sq": LineItem("Labor (0-7 pitch)", "SQ", 200.00),
    "labor_8_11_per_sq": LineItem("Labor (8-11 pitch)", "SQ", 230.00),
    "labor_12_16_per_sq": LineItem("Labor (12-16 pitch)", "SQ", 260.00),
    "disposal_per_sq": LineItem("Disposal", "SQ", 23.00),
    "roll_off_fee": LineItem("Roll Off Fee", "EACH", 300.00),
    "delivery_fee": LineItem("Delivery", "EACH", 25.00),
    "cricket_each": LineItem("Cricket", "EACH", 100.00),

    # shingles
    "hdz_per_sq": LineItem("GAF Timberline HDZ", "SQ", 134.29),
    "uhdz_per_sq": LineItem("GAF Timberline UHDZ", "SQ", 140.17),

    # caps
    "seal_a_ridge_bundle": LineItem("Seal-A-Ridge Caps (25')", "BUNDLE", 76.51),
    "timbertex_bundle": LineItem("TimberTex Caps (20')", "BUNDLE", 82.39),
    "caps_labor_bundle": LineItem("Caps Labor", "BUNDLE", 25.00),

    # starter / drip
    "starter_bundle": LineItem("GAF WeatherBlocker Starter Strip (120')", "BUNDLE", 72.23),
    "drip_edge_piece": LineItem("Drip Edge (10' piece)", "PIECE", 16.80),

    # underlayment
    "feltbuster_roll": LineItem("FeltBuster Underlayment (10 SQ)", "ROLL", 134.82),
    "tigerpaw_roll": LineItem("Tiger Paw Underlayment (10 SQ)", "ROLL", 233.26),
    "deckarmor_roll": LineItem("Deck Armor Underlayment (10 SQ)", "ROLL", 313.51),

    # ice shield
    "generic_ice_roll": LineItem("Generic Ice & Water Shield (2 SQ)", "ROLL", 77.04),
    "weatherwatch_roll": LineItem("WeatherWatch Ice & Water Shield (2 SQ)", "ROLL", 100.05),

    # ventilation
    "ridge_runner_roll": LineItem("Cobra Ridge Runner (30' Roll)", "ROLL", 157.83),

    # accessories
    "pipe_flange_each": LineItem("GAF Pivot Pipe Flange", "EACH", 96.30),
    "bath_vent_each": LineItem("Bath Vent", "EACH", 25.68),
    "kitchen_vent_each": LineItem("Kitchen Vent", "EACH", 55.64),
    "power_fan_each": LineItem("Power Fan", "EACH", 225.77),
    "louver_each": LineItem("Louver Vent", "EACH", 22.16),

    # plywood
    "plywood_half_each": LineItem('1/2" Plywood', "EACH", 42.80),
    "plywood_half_labor_each": LineItem("Plywood Labor", "EACH", 20.00),

    # nails
    "coil_nails_box": LineItem('1.25" Coil Nail Box', "BOX", 42.80),

    # misc flashing / sealing
    "step_flashing_bundle": LineItem("Aluminum Step Flashing Bundle", "BUNDLE", 40.66),
    "skylight_flashing_each": LineItem("Skylight Flashing", "EACH", 50.00),
    "chimney_flashing_labor_each": LineItem("Chimney Flashing Labor", "EACH", 150.00),
    "solar_seal_each": LineItem("Solar Seal", "EACH", 10.70),

    # warranties
    "system_plus_flat": LineItem("System Plus Warranty", "EACH", 80.00),
    "silver_pledge_flat": LineItem("Silver Pledge Warranty", "EACH", 170.00),
    "golden_pledge_per_sq": LineItem("Golden Pledge Warranty", "SQ", 9.00),
}


PACKAGE_RULES = {
    "good": {
        "shingle_key": "hdz_per_sq",
        "shingle_name": "GAF Timberline HDZ",
        "caps_key": "seal_a_ridge_bundle",
        "caps_coverage_ft": 25.0,
        "underlayment_key": "feltbuster_roll",
        "ice_key": "generic_ice_roll",
        "ice_rolls_per_sq": 3.0 / 14.0,
        "warranty_type": "System Plus",
        "warranty_key": "system_plus_flat",
        "warranty_is_flat": True,
    },
    "better": {
        "shingle_key": "hdz_per_sq",
        "shingle_name": "GAF Timberline HDZ",
        "caps_key": "seal_a_ridge_bundle",
        "caps_coverage_ft": 25.0,
        "underlayment_key": "tigerpaw_roll",
        "ice_key": "weatherwatch_roll",
        "ice_rolls_per_sq": 3.0 / 14.0,
        "warranty_type": "Silver Pledge",
        "warranty_key": "silver_pledge_flat",
        "warranty_is_flat": True,
    },
    "best": {
        "shingle_key": "uhdz_per_sq",
        "shingle_name": "GAF Timberline UHDZ",
        "caps_key": "timbertex_bundle",
        "caps_coverage_ft": 20.0,
        "underlayment_key": "deckarmor_roll",
        "ice_key": "weatherwatch_roll",
        "ice_rolls_per_sq": 3.0 / 14.0,
        "warranty_type": "Golden Pledge",
        "warranty_key": "golden_pledge_per_sq",
        "warranty_is_flat": False,
    },
}