import csv
from pathlib import Path


def export_to_csv(job, estimate, selling_price, output_dir="outputs"):
    Path(output_dir).mkdir(exist_ok=True)

    safe_name = job.customer_name.lower().replace(" ", "_")
    safe_package = estimate.package_name.lower()
    filename = f"{safe_name}_{safe_package}_estimate.csv"
    path = Path(output_dir) / filename

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["MILLER ROOFING"])
        writer.writerow(["Roofing Estimate Export"])
        writer.writerow([])

        writer.writerow(["Customer Name", job.customer_name])
        writer.writerow(["Property Address", job.address])
        writer.writerow(["Selected Package", estimate.package_name])
        writer.writerow(["Shingle System", estimate.shingle_name])
        writer.writerow(["Warranty", estimate.warranty_name])
        writer.writerow([])

        writer.writerow(["ROOF SUMMARY"])
        writer.writerow(["Squares 0-7", job.squares_0_7])
        writer.writerow(["Squares 8-11", job.squares_8_11])
        writer.writerow(["Squares 12-16", job.squares_12_16])
        writer.writerow(["Total Squares", estimate.total_squares])
        writer.writerow(["Eaves Feet", job.eaves_feet])
        writer.writerow(["Rakes Feet", job.rakes_feet])
        writer.writerow(["Ridge Vent Feet", job.ridge_vent_feet])
        writer.writerow([])

        writer.writerow(["ESTIMATE BREAKDOWN"])
        writer.writerow(["Item", "Quantity", "Unit", "Unit Price", "Line Total"])

        for line in estimate.lines:
            writer.writerow([
                line.name,
                line.quantity,
                line.unit,
                f"${line.unit_price:,.2f}",
                f"${line.total:,.2f}",
            ])

        writer.writerow([])
        writer.writerow(["COST", "", "", "", f"${estimate.subtotal:,.2f}"])
        writer.writerow(["SELLING PRICE", "", "", "", f"${selling_price:,.2f}"])
        writer.writerow(["PROFIT", "", "", "", f"${selling_price - estimate.subtotal:,.2f}"])

    return str(path)