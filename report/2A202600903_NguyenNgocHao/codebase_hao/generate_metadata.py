"""
Script to automatically generate metadata from legal document filenames.

This script parses Vietnamese legal document filenames and extracts metadata
such as law type, status, year, law number, and draft version.
"""

import re
from pathlib import Path
from typing import Dict, Optional


def parse_filename_metadata(filename: str) -> Dict[str, any]:
    """
    Parse a legal document filename and extract metadata.

    Args:
        filename: Name of the markdown file (without path)

    Returns:
        Dictionary containing metadata fields
    """
    # Remove .md extension
    name = filename.replace('.md', '')

    metadata = {
        "doc_name": name,  # Tên văn bản đầy đủ
        "doc_type_name": None,  # Loại văn bản: "Luật", "Dự thảo"
        "chunk_length": None,  # Sẽ được set khi chunking
        "filename": filename
    }

    # Determine doc_type_name
    if name.startswith("Dự thảo"):
        metadata["doc_type_name"] = "Dự thảo"
    elif name.startswith("Luật"):
        metadata["doc_type_name"] = "Luật"
    else:
        metadata["doc_type_name"] = "Khác"

    return metadata


def generate_metadata_for_all_documents(data_dir: str = "data/Data_Law_Transportation") -> Dict[str, Dict]:
    """
    Generate metadata for all documents in the data directory.

    Args:
        data_dir: Path to the directory containing legal documents

    Returns:
        Dictionary mapping filename to metadata
    """
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"Error: Directory {data_dir} does not exist")
        return {}

    all_metadata = {}

    for md_file in data_path.glob("*.md"):
        filename = md_file.name
        metadata = parse_filename_metadata(filename)
        all_metadata[filename] = metadata

    return all_metadata


def print_metadata_summary(all_metadata: Dict[str, Dict]) -> None:
    """Print a formatted summary of all extracted metadata."""

    print("=" * 80)
    print("METADATA EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"\nTotal documents: {len(all_metadata)}")
    print()

    # Group by doc_type_name
    by_type = {}
    for filename, meta in all_metadata.items():
        doc_type = meta["doc_type_name"]
        if doc_type not in by_type:
            by_type[doc_type] = []
        by_type[doc_type].append(filename)

    print("Documents by Type:")
    for doc_type, files in sorted(by_type.items()):
        print(f"  - {doc_type}: {len(files)} documents")
    print()

    # Detailed list
    print("=" * 80)
    print("DETAILED METADATA")
    print("=" * 80)
    print()

    for filename, meta in sorted(all_metadata.items()):
        print(f"File: {filename}")
        print(f"   doc_name:      {meta['doc_name']}")
        print(f"   doc_type_name: {meta['doc_type_name']}")
        print(f"   chunk_length:  {meta['chunk_length']} (will be set during chunking)")
        print()


def export_metadata_json(all_metadata: Dict[str, Dict], output_file: str = "metadata_mapping.json") -> None:
    """Export metadata to JSON file."""
    import json

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, ensure_ascii=False, indent=2)

    print(f"Metadata exported to {output_file}")


def main():
    """Main function to generate and display metadata."""
    import sys
    import io

    # Set UTF-8 encoding for stdout to handle Vietnamese characters
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Scanning legal documents and extracting metadata...\n")

    # Generate metadata
    all_metadata = generate_metadata_for_all_documents()

    if not all_metadata:
        print("No documents found or error occurred")
        return

    # Print summary
    print_metadata_summary(all_metadata)

    # Export to JSON
    export_metadata_json(all_metadata, "codebase_hao/metadata_mapping.json")

    print("\n" + "=" * 80)
    print("Metadata generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()