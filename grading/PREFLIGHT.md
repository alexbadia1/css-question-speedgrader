# Preflight

## Usage

Assuming the zip file is in the root of `preflight` directory, the following commands will unzip the submissions, filter the submissions, and generate the buttons.
```bash
# Syntax
#   python unzip.py <path_to_zip_file> --dest_dir <extracted_zip_contents_dir>
#   python filter.py <extracted_zip_contents_dir> --dest_dir <filtered_submissions_dir>
#   python buttons.py <filtered_submissions_dir>/css
#
# Example
cd grading
python unzip.py submissions.zip --dest_dir .data/raw
python filter.py .data/raw --dest_dir .data/filtered
python buttons.py .data/filtered/css
```
