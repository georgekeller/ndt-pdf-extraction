"""
PDF to JSON Text Extractor

This script loops through all PDF files in a specified folder,
extracts the text content from each page (ignoring images),
and saves the combined results into a single JSON file.

Dependencies:
    pip install pymupdf
"""

import json
from pathlib import Path

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: Path) -> dict:
    """Extract all text content from a single PDF file.

    Opens the PDF, iterates through each page, and collects
    the text content while ignoring any images or graphics.

    Args:
        pdf_path: Path to the PDF file to process.

    Returns:
        A dictionary containing the filename, total page count,
        and a list of page objects with page numbers and text.
    """

    # Open the PDF document using PyMuPDF
    document = fitz.open(pdf_path)

    # Extract text from each page, storing page number and text content
    pages = []
    for page_number in range(len(document)):
        page = document[page_number]

        # get_text("text") extracts only text content, ignoring images
        text = page.get_text("text")

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    # Close the document to free resources
    document.close()

    return {
        "filename": pdf_path.name,
        "total_pages": len(pages),
        "pages": pages
    }


def process_pdf_folder(folder_path: Path) -> dict:
    """Process all PDF files in the given folder.

    Discovers every .pdf file in the folder, extracts text from each one,
    and combines the results into a single dictionary keyed by filename.

    Args:
        folder_path: Path to the folder containing PDF files.

    Returns:
        A dictionary mapping each PDF filename to its extracted data.
    """

    # Find all PDF files in the folder, sorted alphabetically
    pdf_files = sorted(folder_path.glob("*.pdf"))

    # Check if any PDFs were found
    if not pdf_files:
        print(f"No PDF files found in: {folder_path}")
        return {}

    print(f"Found {len(pdf_files)} PDF file(s) in: {folder_path}")
    print("-" * 60)

    # Process each PDF and collect results into a combined dictionary
    combined_results = {}
    total_pages = 0

    for index, pdf_file in enumerate(pdf_files, start=1):
        print(f"[{index}/{len(pdf_files)}] Processing: {pdf_file.name}")

        try:
            # Extract text from the current PDF
            result = extract_text_from_pdf(pdf_file)

            # Add to combined results, keyed by filename
            combined_results[pdf_file.name] = result

            total_pages += result["total_pages"]
            print(f"    -> Extracted {result['total_pages']} page(s)")

        except Exception as e:
            # Log the error but continue with the remaining PDFs
            print(f"    -> ERROR: Failed to process {pdf_file.name}: {e}")

    print("-" * 60)
    print(f"Finished: {len(combined_results)}/{len(pdf_files)} PDFs processed, {total_pages} total pages")

    return combined_results


def save_to_json(data: dict, output_path: Path) -> None:
    """Save the extracted data to a JSON file.

    Writes the dictionary to a JSON file with readable formatting.

    Args:
        data: The combined extraction results to save.
        output_path: Path where the JSON file will be written.
    """

    # Write the JSON file with indentation for readability
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print(f"Output saved to: {output_path}")


def main() -> None:
    """Main entry point for the PDF to JSON extraction script."""

    # Step 1: Define the folder containing the PDF files
    # Uses the same directory where this script is located
    pdf_folder = Path(__file__).parent

    # Step 2: Process all PDFs in the folder and extract text
    results = process_pdf_folder(pdf_folder)

    # Step 3: Save the combined results to a JSON file
    if results:
        output_file = pdf_folder / "output.json"
        save_to_json(results, output_file)
    else:
        print("No data to save.")


if __name__ == "__main__":
    main()
