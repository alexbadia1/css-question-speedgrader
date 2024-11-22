import csv
import json
import re

def move_context_to_front(s):
    # Regular expression to match any context in brackets at the end of the string
    match = re.search(r'(.*)(\[[^\]]*\])$', s)
    if match:
        main_text = match.group(1).strip()
        context = match.group(2).strip()
        return f"{context} {main_text}"
    return s



with open('grades.json', 'r') as json_file:
    data: dict = json.load(json_file)

csv_data = [['Canvas ID', 'Full Name', 'Implementation Points', 'Visual Points', 'Total Points', 'Comments', 'CSS Filename']]

for css_file_name, obj in data.items():
    canvas_id = obj['canvas_id']
    full_name = obj['full_name']
    implementation_points = obj['implementationPoints']
    visual_points = obj['visualPoints']
    total_points = obj['totalPoints']

    # Visualize comments before implementation comments
    comments = sorted(obj['comments'], key=lambda s: (s.startswith("Missing"), s))
    comments = [move_context_to_front(c) for c in comments]
    comments = '\n'.join(comments)
    csv_data.append([canvas_id, full_name, implementation_points, visual_points, total_points, comments, css_file_name])

print('Number of students:', len(csv_data) - 1)

with open('grades.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(csv_data)
