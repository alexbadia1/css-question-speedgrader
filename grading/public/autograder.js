window.onload = function () {
  // Count total submission
  const buttons = document.querySelectorAll('button');
  document.getElementById('total').innerText = `(${buttons.length})`;
};

const VALID_WALL_POINTS = 0.5;
const VALID_ROW_1_POINTS = 0.5;
const VALID_ROW_2_POINTS = 0.5;
const VALID_ROW_3_POINTS = 0.5;

// Default computed styles, if no styles are provided
const DEFAULT_BACKGROUND_COLOR = 'rgba(0, 0, 0)';
const DEFAULT_BORDER = '0px none rgb(0, 0, 0)';

function equals(args, grade) {
  const { computedStyles, property, expected, points, parent } = args;
  if (computedStyles[property] === expected) {
    grade.implementationPoints += points;
  } else {
    grade.implementationComments.push(`[-${points} point] Missing "${property}: ${expected};" in ${parent}`);
  }
}

function not_equals(args, grade) {
  const { computedStyles, property, excluded, points, parent } = args;
  if (computedStyles[property] !== excluded) {
    grade.implementationPoints += points;
  } else {
    grade.implementationComments.push(`[-${points} point]Missing "${property}: ${excluded};" in ${parent}`);
  }
}

function validate_wall(computedStyles, grade) {
  const points = VALID_WALL_POINTS;
  const parent = '.wall';
  equals({
    computedStyles,
    property: 'display',
    expected: 'flex',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'flexDirection',
    expected: 'column',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'justifyContent',
    expected: 'space-evenly',
    points,
    parent
  }, grade);
  not_equals({
    computedStyles,
    property: 'backgroundColor',
    excluded: DEFAULT_BACKGROUND_COLOR,
    points,
    parent
  }, grade);
  not_equals({
    computedStyles,
    property: 'border',
    excluded: DEFAULT_BORDER,
    points,
    parent
  }, grade);
}

function validate_row_1(computedStyles, grade) {
  const points = VALID_ROW_1_POINTS;
  const parent = '.row:nth-child(1)';
  equals({
    computedStyles,
    property: 'display',
    expected: 'flex',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'flexDirection',
    expected: 'row',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'justifyContent',
    expected: 'space-around',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'alignItems',
    expected: 'center',
    points,
    parent
  }, grade);
  not_equals({
    computedStyles,
    property: 'backgroundColor',
    excluded: DEFAULT_BACKGROUND_COLOR,
    points,
    parent
  }, grade);
}

function validate_row_2(computedStyles, grade) {
  const points = VALID_ROW_2_POINTS;
  const parent = '.row:nth-child(2)';
  equals({
    computedStyles,
    property: 'display',
    expected: 'flex',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'flexDirection',
    expected: 'row',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'justifyContent',
    expected: 'space-between',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'alignItems',
    expected: 'center',
    points,
    parent
  }, grade);
  not_equals({
    computedStyles,
    property: 'backgroundColor',
    excluded: DEFAULT_BACKGROUND_COLOR,
    points,
    parent
  }, grade);
}

function validate_row_3(computedStyles, grade) {
  const points = VALID_ROW_3_POINTS;
  const parent = '.row:nth-child(3)';
  equals({
    computedStyles,
    property: 'display',
    expected: 'flex',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'flexDirection',
    expected: 'row-reverse',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'justifyContent',
    expected: 'center',
    points,
    parent
  }, grade);
  equals({
    computedStyles,
    property: 'alignItems',
    expected: 'center',
    points,
    parent
  }, grade);
  not_equals({
    computedStyles,
    property: 'backgroundColor',
    excluded: DEFAULT_BACKGROUND_COLOR,
    points,
    parent
  }, grade);
}

function calculate_implementation_grade() {
  const implementationGrade = {
    implementationPoints: 0,
    implementationComments: [],
  }

  const wall = document.querySelector('.wall');
  const wallComputedStyles = window.getComputedStyle(wall);
  validate_wall(wallComputedStyles, implementationGrade);

  const row1 = document.querySelector('.wall .row:nth-child(1)');
  const row1ComputedStyles = window.getComputedStyle(row1);
  validate_row_1(row1ComputedStyles, implementationGrade);

  const row2 = document.querySelector('.wall .row:nth-child(2)');
  const row2ComputedStyles = window.getComputedStyle(row2);
  validate_row_2(row2ComputedStyles, implementationGrade);

  const row3 = document.querySelector('.wall .row:nth-child(3)');
  const row3ComputedStyles = window.getComputedStyle(row3);
  validate_row_3(row3ComputedStyles, implementationGrade);

  return implementationGrade;
}

function calculate_visual_grade() {
  const form = document.getElementById('visual-grade-rubric');
  const checkboxes = form.querySelectorAll('input[type="checkbox"]');

  const visualGrade = {
    visualPoints: 0,
    visualComments: [],
  }

  checkboxes.forEach((checkbox) => {
    const points = parseFloat(checkbox.getAttribute('data-visual-points'));
    const errorMessage = checkbox.getAttribute('data-error-message');
    const label = form.querySelector(`label[for="${checkbox.id}"]`);

    if (checkbox.checked) {
      visualGrade.visualPoints += points;
    } else {
      visualGrade.visualComments.push(
        `[-${points} point${points > 1 ? 's' : ''}] ${errorMessage}`
      );
    }
  });

  return visualGrade;
}

function grade() {
  // Prevent form submission
  event.preventDefault();

  // 1. Grade implementation and visual
  const iGrade = calculate_implementation_grade();
  const vGrade = calculate_visual_grade();

  // 2. Aggregate results
  const comments = vGrade.visualComments.concat(iGrade.implementationComments);
  const totalPoints = iGrade.implementationPoints + vGrade.visualPoints;

  // 3. Save display results
  const active = document.getElementById('active');
  const { canvas_full_name, canvas_id, css_file_name } = JSON.parse(active.dataset.jsonString);

  const header = [
    `Name: ${canvas_full_name}`,
    `Total Points: ${totalPoints}`,
  ];

  const textarea = document.getElementById('autograde-feedback');
  textarea.value = header.concat(comments).join('\n');

  // 4. Save results to local storage
  localStorage.setItem(
    css_file_name,
    JSON.stringify({
      full_name: canvas_full_name,
      canvas_id,
      css_file_name,
      implementationPoints: iGrade.implementationPoints,
      visualPoints: vGrade.visualPoints,
      totalPoints,
      comments,
    })
  );
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function gradeAll() {
  const buttons = document.getElementsByClassName('submission_button');
  for (let i = 0; i < buttons.length; i++) {
    const button = buttons[i];
    button.click();
    await sleep(100);
    grade();
  }
}

// TODO: Make a pop up with a link to download the grades
function download() {
  const css_filenames = Object.keys(localStorage);
  css_filenames.sort();

  const result = {};

  for (let i = 0; i < css_filenames.length; i++) {
    const k = css_filenames[i];
    const data = JSON.parse(localStorage.getItem(k));
    result[k] = data;
  }

  console.log(JSON.stringify(result));

  alert(
    'Copy JSON data from the console and manually paste into into grades.json file'
  );
}
