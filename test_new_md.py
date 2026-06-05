import os
import glob
from main import run_manual_demo


def test_law_data_processing() -> None:
    """Test that the manual demo can process all markdown files in the Law Transportation data directory.

    The test collects all .md files under `data/Data_Law_Transportation` and invokes
    `run_manual_demo` with those files as the sample input. It asserts that the function
    exits with code 0, indicating successful loading, embedding, and retrieval steps.
    """
    # Resolve the absolute path to the data directory relative to this script
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "Data_Law_Transportation"))
    md_files = glob.glob(os.path.join(base_dir, "*.md"))
    # Ensure we have at least one markdown file to test against
    assert md_files, f"No markdown files found in {base_dir}"
    # Run the manual demo with the collected files
    exit_code = run_manual_demo(sample_files=md_files)
    assert exit_code == 0, f"run_manual_demo returned non-zero exit code: {exit_code}"
