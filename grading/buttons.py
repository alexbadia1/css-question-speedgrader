import argparse
import os
import textwrap
from typing import List


def get_full_name(data: str) -> str:
    """
    Get the full name from the CSS file name

    CSS file name format:
        <name-nth-part>_<name-part2>_<name-part1><canvas-id>_question_<numbers>_<numbers>.css
    """

    # ["<name-part3>_<name-part2>_<name-part1><canvas-id>", "<numbers>_<numbers>.css"]
    parts = data.split('_question_')[0]

    # "<name-part3>_<name-part2>_<name-part1>"
    no_digits = ''.join([symbol for symbol in parts if not symbol.isdigit()])

    # ["<name-part1>", "<name-part2>", "<name-part3>"]
    corrected_order = no_digits.split('_')[::-1]

    # "<name-part1> <name-part2> <name-part3>"
    return ' '.join(corrected_order).title()


def get_canvas_id(data: str) -> str:
    """
    Get the canvas id from the CSS file name
    """
    return ''.join([symbol for symbol in data if symbol.isdigit()])


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Filter submission files')
    parser.add_argument(
        'source_directory',
        help='Directory containing the ONLY CSS submission files',
        type=str
    )
    return parser.parse_args()


if __name__ == '__main__':
    
    args: argparse.Namespace = parse_arguments()
    source_directory = args.source_directory

    file_names: List[str] = os.listdir(source_directory)
    file_names.sort()

    html: List[str] = []

    for file_name in file_names:
        data: List[str] = file_name.split('_question_')[0]
        button_id: int = len(html) + 1
        full_name: str = get_full_name(data)
        canvas_id: str = get_canvas_id(data)
        html.append(
            textwrap.dedent(f"""
            <button
                id=\"submission_button_{button_id}\"
                class=\"submission_button\" 
                onclick=\"swapStyle(this)\" 
                style=\"margin: 8px; width: 100%; height: 48px;\" 
                data-button-id=\"{button_id}\"
                data-canvas-full-name=\"{full_name}\"
                data-canvas-id=\"{canvas_id}\"
                data-css-file-name=\"{file_name}\"
            >
                {full_name}
            </button>
            """).strip()
        )

    with open('public/buttons.html', 'w') as buttons:
        for content in html:
            buttons.write(content + '\n')
