const form = document.querySelector("#gpa-calc-form");

//default values
let GPAScale = "4.0_12";
let inputType = "percentage";

const setGPAScale = (target) => {
  GPAScale = target.value;
  //remove the active class from other elements
  Array.from(target.parentElement.children).forEach((child) => {
    child.classList.remove("bg-info");
  });
  //add the active class
  target.classList.add("bg-info");
  //if scale is 4.0 show point result
  if (GPAScale === "4.0_12" || GPAScale === "4.0_10") {
    document
      .querySelector("#point")
      .parentElement.parentElement.classList.remove("d-none");
  } else {
    document
      .querySelector("#point")
      .parentElement.parentElement.classList.add("d-none");
  }
  //Change letter grad list on the dropdowns
  document.querySelectorAll(".letter-grade-list").forEach((list) => {
    list.innerHTML = generateGradeOptions(GPAScale);
  });
};

//used as id for semester and course
const getRandomString = () => Math.random().toString(36).slice(2);

const setInputType = (target) => {
  inputType = target.value;
  //remove the active class from other elements
  Array.from(target.parentElement.children).forEach((child) => {
    child.classList.remove("bg-info");
  });
  //add the active class
  target.classList.add("bg-info");
  handleInputTypeChange();
};

const handleInputTypeChange = () => {
  //Show/Hide Percentage or Letter Grade field
  document.querySelectorAll(".input-type-label").forEach((item) => {
    item.classList.add("d-none");
  });
  document
    .querySelectorAll(`.input-type-label.${inputType}-format`)
    .forEach((item) => {
      item.classList.remove("d-none");
    });
  document
    .querySelectorAll(`.input-type`)
    // item.parentElement.parentElement.dataset.id
    .forEach((item) => {
      let semesterID = item.parentElement.parentElement.dataset.id;
      let randomID = item.parentElement.dataset.id;
      item.innerHTML =
        inputType === "percentage"
          ? `<input
        class="form-control"
        type="number"
        name="percentage-${semesterID}-${randomID}"
        id="percentage-${semesterID}-${randomID}"
        min="0"
        max="100"
        required
      />`
          : `<select
        class="form-select letter-grade-list"
        name="grade-${semesterID}-${randomID}"
        id="grade-${semesterID}-${randomID}"
        required
      >
        ${generateGradeOptions(GPAScale)}
      </select>`;
    });
};

const addSemester = () => {
  let newSemesterID = 1;
  Array.from(document.querySelector("#semesters").children).forEach(
    (semester) =>
      parseInt(semester.dataset.id) >= newSemesterID &&
      (newSemesterID = parseInt(semester.dataset.id) + 1)
  );
  let randomID = getRandomString();
  let content = `<div
    class="m-2 p-3 row semester border rounded"
    data-id="${newSemesterID}"
  >
    <div class="row d-flex justify-content-between">
      <div class="col-md-6 textColour">
        <h4>Semester ${newSemesterID}</h4>
      </div>
      <div class="col-md-1">
        <button
          type="button"
          class="btn btn-light border border-danger btn-sm my-1"
          onclick="this.parentNode.parentNode.parentNode.remove()"
        >
          ❌
        </button>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-4 textColour"><b>Course Name</b></div>
      <div class="col-sm-4 textColour input-type-label percentage-format ${
        inputType === "percentage" ? "" : "d-none"
      }">
        <b>Percentage</b>
      </div>
      <div class="col-sm-4 textColour input-type-label letter-grade-format ${
        inputType === "percentage" ? "d-none" : ""
      }">
        <b>Letter Grade</b>
      </div>
      <div class="col-sm-3 textColour"><b>Credits</b></div>
      <div class="col-sm-1"></div>
    </div>
    <div class="course row my-1" data-id="${randomID}">
      <div class="col-sm-4">
        <input
          class="form-control"
          type="text"
          name="course-name-${newSemesterID}-${randomID}"
          id="course-name-${newSemesterID}-${randomID}"
        />
      </div>
      <div class="col-sm-4 input-type ${
        inputType === "percentage" ? "percentage-format" : "letter-grade-format"
      }">
        ${
          inputType === "percentage"
            ? `<input
          class="form-control"
          type="number"
          name="percentage-${newSemesterID}-${randomID}"
          id="percentage-${newSemesterID}-${randomID}"
          min="0"
          max="100"
          required
        />`
            : `<select
          class="form-select letter-grade-list"
          name="grade-${newSemesterID}-${randomID}"
          id="grade-${newSemesterID}-${randomID}"
          required
        >
          ${generateGradeOptions(GPAScale)}
        </select>`
        }
      </div>
      <div class="col-sm-3">
        <input
          class="form-control"
          type="number"
          name="credits-${newSemesterID}-${randomID}"
          id="credits-${newSemesterID}-${randomID}"
          required
        />
      </div>
      <div class="col-sm-1"></div>
    </div>

    <div class="col-md-4 my-2">
      <button
        type="button"
        class="btn btn-primary"
        onclick="addCourse(${newSemesterID}, this)"
      >
        Add Course
      </button>
    </div>
  </div>`;
  document.querySelector("#semesters").insertAdjacentHTML("beforeend", content);
};

const addCourse = (semesterID, referringElement) => {
  let randomID = getRandomString();
  let content = `<div class="course row my-1" data-id="${randomID}">
    <div class="col-sm-4">
      <input
        class="form-control"
        type="text"
        name="course-name-${semesterID}-${randomID}"
        id="course-name-${semesterID}-${randomID}"
      />
    </div>
    <div class="col-sm-4 input-type ${
      inputType === "percentage" ? "percentage-format" : "letter-grade-format"
    }">
      ${
        inputType === "percentage"
          ? `<input
        class="form-control"
        type="number"
        name="percentage-${semesterID}-${randomID}"
        id="percentage-${semesterID}-${randomID}"
        min="0"
        max="100"
        required
      />`
          : `<select
        class="form-select letter-grade-list"
        name="grade-${semesterID}-${randomID}"
        id="grade-${semesterID}-${randomID}"
        required
      >
        ${generateGradeOptions(GPAScale)}
      </select>`
      }
    </div>
    <div class="col-sm-3">
      <input
        class="form-control"
        type="number"
        name="credits-${semesterID}-${randomID}"
        id="credits-${semesterID}-${randomID}"
        required
      />
    </div>
      <div class="col-sm-1">
        <button
          type="button"
          class="btn btn-light border border-danger btn-sm my-1"
          onclick="this.parentNode.parentNode.remove()"
        >
          ❌
      </button>
    </div>
  </div>`;
  referringElement.parentElement.insertAdjacentHTML("beforebegin", content);
};

const generateGradeOptions = (scale) => {
  let content = `<option value="">&#8212;</option>`;
  GPA_SCALES[scale].forEach((grade) => {
    content += `<option value="${grade.letter}">${grade.letter} (${
      GPAScale === "4.33" ? grade.gpa.toFixed(2) : grade.gpa.toFixed(1)
    }) [${grade.percentage.min} - ${grade.percentage.max}]</option>`;
  });
  return content;
};

const calculate = () => {
  //check if all input is fulfilled (course name is not required)
  if (!form.reportValidity()) {
    return;
  }
  //get all input fields
  let inputs = Array.from(form.querySelectorAll("input, select"));
  //get all semester id's
  let allSemesterID = Array.from(
    document.querySelector("#semesters").children
  ).map((semester) => semester.dataset.id);
  //build semesters object
  let semesters = {};
  allSemesterID.forEach((id) => {
    semesters[id] = { courses: [] };
    Array.from(
      document.querySelectorAll(`.semester[data-id="${id}"] .course`)
    ).forEach((courseElem) => {
      let course = {
        name: getInputValue(
          inputs,
          `course-name-${id}-${courseElem.dataset.id}`
        ),
        percentage: parseFloat(
          getInputValue(inputs, `percentage-${id}-${courseElem.dataset.id}`)
        ),
        letter: getInputValue(inputs, `grade-${id}-${courseElem.dataset.id}`),
        credits: parseFloat(
          getInputValue(inputs, `credits-${id}-${courseElem.dataset.id}`)
        ),
      };
      semesters[id].courses.push(course);
    });
  });
  //now calculate the gpa and set the value
  let data = calculateGPA(semesters);
  document.querySelector("#gpa").innerText = data.gpa.toFixed(3);
  document.querySelector("#cumulative").innerText =
    allSemesterID.length > 1 ? data.cgpa.toFixed(3) : "N/A";
  document.querySelector("#current").innerText =
    data.currentSemester.toFixed(3);
};

const resetForm = () => {
  //reset GPAScale and inputType
  document.querySelector("#defaultGPAScale").click();
  document.querySelector("#defaultInputType").click();
  //reset the results
  document.querySelector("#gpa").innerText = "";
  document.querySelector("#cumulative").innerText = "";
  document.querySelector("#current").innerText = "";
  document.querySelector("#point").innerText = "";
  //set the current semester
  document.querySelector(
    "#semesters"
  ).innerHTML = `<div class="m-2 p-3 row semester border rounded" data-id="1">
  <div class="row d-flex justify-content-between">
    <div class="col-md-6 textColour">
      <h4>Current Semester</h4>
    </div>
    <div class="col-md-1"></div>
  </div>
  <div class="row">
    <div class="col-sm-4 textColour"><b>Course Name</b></div>
    <div class="col-sm-4 input-type-label percentage-format textColour">
      <b>Percentage</b>
    </div>
    <div
      class="col-sm-4 input-type-label letter-grade-format d-none textColour"
    >
      <b>Letter Grade</b>
    </div>
    <div class="col-sm-3 textColour"><b>Credits</b></div>
    <div class="col-sm-1"></div>
  </div>
  <div class="course row my-1" data-id="kmdki98yh9">
    <div class="col-sm-4">
      <input
        class="form-control"
        type="text"
        name="course-name-1-kmdki98yh9"
        id="course-name-1-kmdki98yh9"
      />
    </div>
    <div class="col-sm-4 input-type percentage-format">
      <input
        class="form-control"
        type="number"
        name="percentage-1-kmdki98yh9"
        id="percentage-1-kmdki98yh9"
        min="0"
        max="100"
        required
      />
    </div>
    <div class="col-sm-3">
      <input
        class="form-control"
        type="number"
        name="credits-1-kmdki98yh9"
        id="credits-1-kmdki98yh9"
        required
      />
    </div>
    <div class="col-sm-1"></div>
  </div>

  <div class="col-md-4 my-2">
    <button
      type="button"
      class="btn btn-primary"
      onclick="addCourse(1, this)"
    >
      Add Course
    </button>
  </div>
</div>`;
};
//get input value from an array of inputs based off of id
const getInputValue = (inputs, id) => {
  let input = inputs.find((input) => input.id === id);
  return input && input.value;
};
//calculates gpa by multiplying grade with credits and convert letter as needed and adding to total score
const calculateGPA = (semesters) => {
  Object.keys(semesters).forEach((key) => {
    semesters[key].totalScore = 0;
    semesters[key].totalCredits = 0;
    semesters[key].courses.forEach((course) => {
      //check to see of letter grade or percentage
      if (isNaN(course.percentage)) {
        semesters[key].totalScore +=
          covertLetterToGPA(course.letter) * course.credits;
      } else {
        semesters[key].totalScore +=
          covertPercentageToGPA(course.percentage) * course.credits;
      }
      semesters[key].totalCredits += course.credits;
    });
    //gpa calculation
    semesters[key].gpa =
      semesters[key].totalScore / semesters[key].totalCredits;
  });

  let totalGPA = 0;
  let totalCGPA = 0;
  let totalSemester = Object.keys(semesters).length;
  let totalSemestersCredits = 0;

  Object.keys(semesters).forEach((key) => {
    totalGPA += semesters[key].gpa;
    totalCGPA += semesters[key].gpa * semesters[key].totalCredits;
    totalSemestersCredits += semesters[key].totalCredits;
  });

  //show the point
  if (GPAScale === "4.0_12" || GPAScale === "4.0_10") {
    document.querySelector("#point").innerText =
      GPA_SCALES[GPAScale].length -
      1 -
      Array.from(GPA_SCALES[GPAScale]).findIndex((grade, index, array) => {
        if (totalGPA / totalSemester >= grade.gpa) return grade;
      });
  }

  return {
    gpa: totalGPA / totalSemester,
    cgpa: totalCGPA / totalSemestersCredits,
    currentSemester: semesters["1"].gpa,
  };
};

const covertPercentageToGPA = (percentage) => {
  //grab gpa value based off of grade
  let grade = GPA_SCALES[GPAScale].find((item) => {
    if (
      item.percentage.min <= percentage &&
      percentage <= item.percentage.max
    ) {
      return item;
    }
  });
  return grade && grade.gpa;
};

const covertLetterToGPA = (letter) => {
  let grade = GPA_SCALES[GPAScale].find((item) => {
    if (item.letter === letter) {
      return item;
    }
  });
  return grade && grade.gpa;
};

//initialize the form
resetForm();
