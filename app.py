import streamlit as st
import os

from estimator import JobInput, build_all_package_estimates, apply_pricing_strategy
from contract_generator import save_contract
from exporter import export_to_csv
from salespeople import SALESPERSONS


st.set_page_config(page_title="Miller Roofing Estimator", layout="wide")


def get_salesperson_options():
    options = {}
    for key, value in SALESPERSONS.items():
        if key != "default":
            options[value["display_name"]] = value
    return options


# Session state setup
if "pricing" not in st.session_state:
    st.session_state.pricing = None
if "job" not in st.session_state:
    st.session_state.job = None
if "selected_package" not in st.session_state:
    st.session_state.selected_package = "good"


# Title
st.title("🏠 Miller Roofing Estimate & Proposal Generator")
st.markdown("Enter project details below to generate pricing, compare packages, and create a proposal.")


salesperson_options = get_salesperson_options()


# FORM
with st.form("roofing_estimate_form"):
    st.header("Customer Information")
    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        address = st.text_input("Property Address")
        customer_phone = st.text_input("Customer Phone")

    with col2:
        customer_email = st.text_input("Customer Email")
        salesperson_name = st.selectbox("Salesperson", list(salesperson_options.keys()))
        markup_percent = st.number_input("Desired Markup %", min_value=0.0, value=20.0, step=1.0)

    st.header("Roof Squares by Pitch")
    col3, col4, col5 = st.columns(3)

    with col3:
        squares_0_7 = st.number_input("Squares (0-7 pitch)", min_value=0.0, value=0.0, step=0.5)
    with col4:
        squares_8_11 = st.number_input("Squares (8-11 pitch)", min_value=0.0, value=0.0, step=0.5)
    with col5:
        squares_12_16 = st.number_input("Squares (12-16 pitch)", min_value=0.0, value=0.0, step=0.5)

    st.header("Linear Measurements")
    col6, col7, col8 = st.columns(3)

    with col6:
        eaves_feet = st.number_input("Eaves Feet", min_value=0.0, value=0.0, step=1.0)
    with col7:
        rakes_feet = st.number_input("Rakes Feet", min_value=0.0, value=0.0, step=1.0)
    with col8:
        ridge_vent_feet = st.number_input("Ridge Vent Feet", min_value=0.0, value=0.0, step=1.0)

    st.header("Accessories")
    col9, col10, col11, col12, col13 = st.columns(5)

    with col9:
        pipe_flanges = st.number_input("Pipe Flanges", min_value=0, value=0)
    with col10:
        bath_vents = st.number_input("Bath Vents", min_value=0, value=0)
    with col11:
        kitchen_vents = st.number_input("Kitchen Vents", min_value=0, value=0)
    with col12:
        power_fans = st.number_input("Power Fans", min_value=0, value=0)
    with col13:
        louvers = st.number_input("Louvers", min_value=0, value=0)

    st.header("Repairs / Flashing / Misc.")
    col14, col15, col16 = st.columns(3)

    with col14:
        plywood_half = st.number_input('1/2" Plywood Sheets', min_value=0, value=0)
        step_flashing_bundles = st.number_input("Step Flashing Bundles", min_value=0, value=0)
        skylight_flashings = st.number_input("Skylight Flashings", min_value=0, value=0)

    with col15:
        chimney_flashings = st.number_input("Chimney Flashings", min_value=0, value=0)
        solar_seal_tubes = st.number_input("Solar Seal Tubes", min_value=0, value=0)
        crickets = st.number_input("Crickets", min_value=0, value=0)

    with col16:
        roll_off_needed = st.checkbox("Roll Off Needed")
        delivery_needed = st.checkbox("Delivery Needed")
        promotion_discount = st.number_input("Promotion Discount", min_value=0.0, value=0.0)

    submitted = st.form_submit_button("Generate Estimate Options")


# PROCESS FORM
if submitted:
    selected_salesperson = salesperson_options[salesperson_name]

    job = JobInput(
        customer_name=customer_name,
        address=address,
        customer_phone=customer_phone,
        customer_email=customer_email,
        salesperson_name=selected_salesperson["display_name"],
        salesperson_email=selected_salesperson["email"],
        salesperson_phone=selected_salesperson["phone"],
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

    st.session_state.job = job
    st.session_state.pricing = pricing


# DISPLAY RESULTS
if st.session_state.pricing is not None:
    pricing = st.session_state.pricing
    job = st.session_state.job

    st.success("Estimate options generated successfully.")

    st.header("Package Comparison")

    comparison_rows = []
    for key in ["good", "better", "best"]:
        p = pricing[key]
        comparison_rows.append({
            "Package": p["package"],
            "Cost": f"${p['cost']:,.2f}",
            "Selling Price": f"${p['price']:,.2f}",
            "Profit": f"${p['profit']:,.2f}",
            "Margin %": f"{p['margin']:.2f}%",
            "Warranty": p["estimate"].warranty_name,
            "Shingle": p["estimate"].shingle_name,
        })

    st.dataframe(comparison_rows, width="stretch")

    selected_package = st.selectbox(
        "Select Package to Finalize",
        ["good", "better", "best"],
        index=["good", "better", "best"].index(st.session_state.selected_package),
    )

    st.session_state.selected_package = selected_package

    selected_data = pricing[selected_package]
    selected_estimate = selected_data["estimate"]
    selected_price = selected_data["price"]

    st.subheader("Selected Package Summary")
    st.write(f"**Package:** {selected_estimate.package_name}")
    st.write(f"**Selling Price:** ${selected_price:,.2f}")
    st.write(f"**Profit:** ${selected_data['profit']:,.2f}")
    st.write(f"**Margin:** {selected_data['margin']:.2f}%")

    # FINAL BUTTONS
    if st.button("Generate Proposal & CSV"):
        contract_path = save_contract(job, selected_estimate, selected_price)
        csv_path = export_to_csv(job, selected_estimate, selected_price)

        st.success("Files generated successfully.")

        # Download Proposal
        with open(contract_path, "rb") as f:
            st.download_button(
                "📄 Download Proposal",
                f,
                file_name=os.path.basename(contract_path)
            )

        # Download CSV
        with open(csv_path, "rb") as f:
            st.download_button(
                "📊 Download CSV",
                f,
                file_name=os.path.basename(csv_path)
            )

        # Breakdown Table
        st.subheader("Estimate Breakdown")

        line_rows = []
        for line in selected_estimate.lines:
            line_rows.append({
                "Item": line.name,
                "Qty": line.quantity,
                "Unit": line.unit,
                "Unit Price": f"${line.unit_price:,.2f}",
                "Total": f"${line.total:,.2f}",
            })

        st.dataframe(line_rows, width="stretch")