"""
Generate 2000 synthetic NDT/Colcheck JSON entries for testing.

Creates realistic variations of street lighting column inspection data
matching the exact text format that pdf_to_json.py produces.
"""

import json
import random
import uuid
from pathlib import Path

STREETS = [
    "GIPSY HILL", "CAMDEN HILL ROAD", "BRIXTON ROAD", "NORWOOD ROAD",
    "TULSE HILL", "HERNE HILL", "DULWICH ROAD", "RAILTON ROAD",
    "COLDHARBOUR LANE", "EFFRA ROAD", "ACRE LANE", "STOCKWELL ROAD",
    "CLAPHAM ROAD", "STREATHAM HIGH ROAD", "LEIGHAM VALE",
    "THURLOW PARK ROAD", "CROXTED ROAD", "HALF MOON LANE",
    "MILKWOOD ROAD", "LOUGHBOROUGH ROAD", "SHAKESPEARE ROAD",
    "LOWDEN ROAD", "PALACE ROAD", "BEULAH HILL", "CHURCH ROAD",
    "KNIGHT'S HILL", "CENTRAL HILL", "ELDER ROAD", "ROSENDALE ROAD",
    "TRINITY RISE",
]

WARDS = [
    "L1 Gipsy Hill", "L2 Thurlow Park", "L3 Herne Hill",
    "L4 Tulse Hill", "L5 Brixton Hill", "L6 Coldharbour",
    "L7 Stockwell", "L8 Clapham Town", "L9 Streatham Hill",
    "L10 Knight's Hill",
]

COLUMN_TYPES = [
    "CD - Decorative", "CS - Standard", "CT - Tubular",
    "CF - Fluted", "CO - Ornamental",
]

MATERIALS = ["S1 - Steel", "S2 - Aluminium", "C1 - Cast Iron", "S3 - Stainless Steel"]

CONDITIONS = ["Good", "Fair", "Poor"]

FIXING_TYPES = ["Planted", "Flanged", "Root Planted"]

HERITAGE = ["Y", "N"]

LISTED_STATUSES = ["Functional", "Listed Grade II", "Locally Listed", "Not Listed"]

SEVERITY_GRADES = ["A", "B", "C", "D", "E"]

GN22_COMMENTS = {
    "base external": [
        "damaged paint surface/signs of minor corrosion",
        "heavy corrosion/section loss visible",
        "paint intact/no visible defects",
        "surface rust forming at ground level",
        "minor impact damage/paint chipped",
        "significant corrosion at base plate",
    ],
    "base internal": [
        "signs of minor corrosion/base is filled with water",
        "signs of minor corrosion",
        "heavy corrosion/water ingress evident",
        "dry/minor surface rust",
        "standing water present/corrosion advancing",
        "no access for inspection",
    ],
    "door": [
        "damaged paint surface",
        "door missing/cable exposed",
        "door secure/minor rust",
        "hinge broken/door loose",
        "door sealed/no access",
        "paint peeling/surface corrosion",
    ],
    "embellishment": [
        "damaged paint surface/signs of minor corrosion",
        "decorative elements corroding",
        "paint intact",
        "missing decorative band",
        "surface rust on embellishments",
        "embellishments in good condition",
    ],
    "foundation": [
        "discernible movement when pushed/pavement surface cracks",
        "foundation stable/no movement",
        "slight movement detected",
        "significant lean observed/monitoring required",
        "pavement heave around base",
        "[AMBER] discernible movement/cracking in surrounding pavement",
    ],
    "lantern": [
        "",
        "lantern secure",
        "lantern bracket corroding",
        "lantern tilted slightly",
        "bracket paint peeling",
    ],
    "shaft external": [
        "damaged paint surface",
        "paint peeling/surface corrosion",
        "good condition/paint intact",
        "impact damage at 2m height",
        "significant corrosion mid-shaft",
        "minor scratches/paint chipped",
    ],
    "shaft internal": [
        "",
        "minor surface corrosion",
        "corrosion visible through door opening",
        "unable to inspect fully",
    ],
    "shoulder": [
        "",
        "minor corrosion at shoulder joint",
        "paint cracking at shoulder",
        "good condition",
    ],
}

INSPECTOR_COMMENTS = [
    "",
    "",
    "",
    "- Column leaning slightly, monitor at next inspection",
    "- Vehicle impact damage noted on south side",
    "- Recommend repainting within 12 months",
    "- Water pooling at base, drainage issue",
    "- Column adjacent to construction site, monitor for damage",
    "- Previous repair visible at base, holding well",
    "- Bird nesting in lantern bracket",
    "- Graffiti on shaft, otherwise good condition",
    "- Column leaning 2 degrees north | - Foundation cracks widening since last inspection",
    "- Cable exposure at door, urgent repair needed",
]


def generate_entry(asset_id: int, index: int) -> tuple[str, dict]:
    """Generate a single synthetic NDT/Colcheck JSON entry."""
    street = random.choice(STREETS)
    street_slug = street.replace(" ", "-").replace("'", "")
    col_num = f"C{random.randint(100, 9999):04d}-{random.randint(1, 30):02d}"
    ward = random.choice(WARDS)
    col_type = random.choice(COLUMN_TYPES)
    height = random.choice([5, 6, 8, 10, 12])
    material = random.choice(MATERIALS)
    fixing = random.choice(FIXING_TYPES)
    heritage = random.choice(HERITAGE)
    listed = random.choice(LISTED_STATUSES)
    commission_year = random.randint(1990, 2023)
    commission_date = f"{commission_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    ose = random.randint(520000, 540000)
    osn = random.randint(165000, 180000)

    thickness_max = round(random.uniform(4.0, 8.0), 2)
    thickness_min = round(thickness_max - random.uniform(0.05, 1.5), 2)
    thickness_ave = round((thickness_max + thickness_min) / 2, 2)
    loss_max = random.randint(0, 40)
    loss_ave = random.randint(0, loss_max) if loss_max > 0 else 0

    condition = random.choice(CONDITIONS)
    cciav = random.randint(20, 100)
    ccicrt = random.randint(10, 80)
    arl = random.choice([str(random.randint(1, 25)), "--"])

    test_year = random.randint(2024, 2026)
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 28)
    test_date = f"{test_year}-{test_month:02d}-{test_day:02d}"
    next_test = f"{test_year + 6}-{test_month:02d}-{test_day:02d}"

    road_number = str(random.randint(10000, 99999))

    # Build GN22 elements text
    gn22_text = ""
    for element in ["base external", "base internal", "door", "embellishment",
                     "foundation", "lantern", "shaft external", "shaft internal", "shoulder"]:
        severity = random.choice(SEVERITY_GRADES)
        extent = random.randint(1, 5)
        comment = random.choice(GN22_COMMENTS[element])
        if comment:
            gn22_text += f"{element}\n{severity}\n{extent}\n{comment}\n"
        else:
            gn22_text += f"{element}\n{severity}\n{extent}\n"

    inspector_comment = random.choice(INSPECTOR_COMMENTS)
    comments_section = f"{inspector_comment}\n" if inspector_comment else ""

    page1_text = (
        f"{uuid.uuid4()}\n"
        f"NDT/Colcheck report\n"
        f"0629_001_Equans\n"
        f"Column Name\n"
        f"{street}-{col_num}\n"
        f"Next test\n"
        f"{next_test}\n"
        f"Central asset Id\n"
        f"{asset_id}\n"
        f"Asset Number\n"
        f"Column Height (m)\n"
        f"{height}\n"
        f"Street\n"
        f"{street}\n"
        f"Id\n"
        f"{col_num}\n"
        f"Thickness Max (mm) {thickness_max:.2f}\n"
        f"Road Number\n"
        f"{road_number}\n"
        f"Column type\n"
        f"{col_type}\n"
        f"% Loss Max\n"
        f"{loss_max} %\n"
        f"Ward\n"
        f"{ward}\n"
        f"Material\n"
        f"{material}\n"
        f"Thickness (mm) Min {thickness_min:.2f}\n"
        f"Commission Date\n"
        f"{commission_date}\n"
        f"Heritage Y/N\n"
        f"{heritage}\n"
        f"% Loss Ave (PL)\n"
        f"{loss_ave} %\n"
        f"OSE,OSN\n"
        f"{ose},{osn}\n"
        f"Listed status\n"
        f"{listed}\n"
        f"Thickness Ave (mm)\n"
        f"{thickness_ave:.2f}\n"
        f"Fixing type\n"
        f"{fixing}\n"
        f"Condition\n"
        f"{condition}\n"
        f"CCIav\n"
        f"{cciav}\n"
        f"CCIcrt\n"
        f"{ccicrt}\n"
        f"ARL (years)\n"
        f"{arl}\n"
        f"{gn22_text}"
        f"Column Information\n"
        f"Test date\n"
        f"{test_date}\n"
        f"Element Description (GN22)\n"
        f"Severity\n"
        f"Extent\n"
        f"Comment\n"
        f"Comments\n"
        f"{comments_section}"
    )

    filename = f"{asset_id}-GN22-{test_date}-0629NDT-001-COL-{street_slug}-_-{col_num}-rPec-report.pdf"

    total_pages = random.randint(7, 10)
    pages = [{"page_number": 1, "text": page1_text}]
    pages.append({"page_number": 2, "text": f"NDT/Colcheck report\n0629_001_Equans\nColumn name: {street} _ {col_num}\n"})
    for p in range(3, total_pages + 1):
        pages.append({"page_number": p, "text": ""})

    return filename, {
        "filename": filename,
        "total_pages": total_pages,
        "pages": pages,
    }


def main() -> None:
    """Generate 2000 synthetic entries and merge with existing data."""
    script_dir = Path(__file__).parent
    json_path = script_dir / "output.json"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Existing entries: {len(data)}")

    starting_id = 400000
    for i in range(2000):
        asset_id = starting_id + i
        filename, entry = generate_entry(asset_id, i)
        data[filename] = entry

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Total entries now: {len(data)}")
    print(f"Saved to: {json_path}")


if __name__ == "__main__":
    main()
