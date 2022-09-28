const form = document.querySelector("#course-form");

let course = {
  courseName: "",
  courseCode: "",
  credits: "",
  assignments: [],
  midterms: [],
  finalExam: {
    present: false,
  },
};

async function expand() {
  //expand all accordion
  document
    .querySelectorAll(".accordion-collapse")
    .forEach((accordion) =>
      new bootstrap.Collapse(accordion, { toggle: false }).show()
    );
  form.reportValidity() && submit();
}

function submit() {
  //get all input fields visible and having value
  // let inputs = Array.from(document.querySelectorAll("input")).filter(
  //   (input) => input.value
  // );
  // let assignmentIDs = [];
  // let midtermIDs = [];
  // let isFinalExam = false;
  // //save input id and value in object
  // let inputValues = {};
  // //get the fields value and save to course object
  // inputs.forEach((input) => {
  //   if (input.type === "submit" || input.type === "reset") {
  //     return;
  //   }
  //   //save input id and value in object
  //   inputValues[input.id] = input.value;
  //   switch (input.id) {
  //     case "course-name":
  //       course.courseName = input.value;
  //       break;
  //     case "course-code":
  //       course.courseCode = input.value;
  //       break;
  //     case "credits":
  //       course.credits = input.value;
  //       break;

  //     default:
  //       break;
  //   }
  //   //get assignment IDs
  //   if (input.id.includes("assignment") && input.id.includes("due-date")) {
  //     assignmentIDs.push(input.id.split("assignment")[1][0]); //save the ID (1,2,3...)
  //   }
  //   //get midterm IDs
  //   if (input.id.includes("midterm") && input.id.includes("date")) {
  //     midtermIDs.push(input.id.split("midterm")[1][0]); //save the ID (1,2,3...)
  //   }
  //   //check if final exam is present
  //   isFinalExam = input.id.includes("final-exam");
  // });

  // //save assignments
  // assignmentIDs.forEach((id) => {
  //   let assignment = {
  //     dueDate: inputValues[`assignment${id}-due-date`],
  //     gradeWeight: inputValues[`assignment${id}-grade-weight`],
  //     subtasks: [],
  //   };
  //   //save subtasks
  //   inputs.forEach(
  //     (input) =>
  //       input.id.includes(`assignment${id}-subtask`) &&
  //       assignment.subtasks.push(input.value)
  //   );
  //   //store on course object
  //   course.assignments.push(assignment);
  // });
  // //save midterms
  // midtermIDs.forEach((id) => {
  //   let midterm = {
  //     date: inputValues[`midterm${id}-date`],
  //     startTime: inputValues[`midterm${id}-start-time`],
  //     endTime: inputValues[`midterm${id}-end-time`],
  //     gradeWeight: inputValues[`midterm${id}-grade-weight`],
  //     materialsCovered: [],
  //   };
  //   //save materials
  //   inputs.forEach(
  //     (input) =>
  //       input.id.includes(`midterm${id}-material`) &&
  //       midterm.materialsCovered.push(input.value)
  //   );
  //   //store on course object
  //   course.midterms.push(midterm);
  // });
  // //save final exam
  // if (isFinalExam) {
  //   let finalExam = {
  //     present: true,
  //     date: inputValues["final-exam-date"],
  //     startTime: inputValues["final-exam-start-time"],
  //     endTime: inputValues["final-exam-end-time"],
  //     gradeWeight: inputValues["final-exam-grade-weight"],
  //     materialsCovered: [],
  //   };
  //   inputs.forEach(
  //     (input) =>
  //       input.id.includes("final-exam-material") &&
  //       finalExam.materialsCovered.push(input.value)
  //   );
  //   course.finalExam = finalExam;
  // }
  validateCourse();
}

function validateCourse() {
  //must have one assignment
  if (course.assignments.length === 0) {
    return alert("Must add one assignment.");
  }
  //must have final exam
  // if (!course.finalExam.present) {
  //   return alert("Must add final exam.");
  // }
  //check for empty field
  course.assignments.forEach((assignment) => {
    if (!assignment.dueDate || !assignment.gradeWeight) {
      return alert("An assignment's required field is empty!");
    }
  });
  course.midterms.forEach((midterm) => {
    if (
      !midterm.date ||
      !midterm.startTime ||
      !midterm.endTime ||
      !midterm.gradeWeight
    ) {
      return alert("A midterm's required field is empty!");
    }
  });
  //code if final exam is mandatory

  // if (
  //   !course.finalExam.date ||
  //   !course.finalExam.startTime ||
  //   !course.finalExam.endTime ||
  //   !course.finalExam.gradeWeight
  // ) {
  //   return alert("Final Exam's required field is empty!");
  // }

  //show created course object
  // console.log(JSON.stringify(course, null, 2));
  // let tab = window.open("about:blank", "_blank");
  // tab.document.write(`<pre>${JSON.stringify(course, null, 2)}</pre>`);
  // tab.document.close();
  // //reset course object
  // course = {
  //   courseName: "",
  //   courseCode: "",
  //   credits: "",
  //   assignments: [],
  //   midterms: [],
  //   finalExam: {
  //     present: false,
  //   },
  // };
}

//remove the fields
form.addEventListener("reset", (e) => {
  document.querySelector("#assignments").innerHTML = "";
  document.querySelector("#midterms").innerHTML = "";
  document.querySelector("#final-exam").innerHTML = "";
  document.querySelector("#total-assignments").innerText = Array.from(
    document.querySelector("#assignments").children
  ).length;
  document.querySelector("#total-midterms").innerText = Array.from(
    document.querySelector("#midterms").children
  ).length;
  document.querySelector("#final-exam-add-btn").style.display = "inline-block";
  document.querySelector("#is-final-exam").innerText = "No";
  // course = {
  //   courseName: "",
  //   courseCode: "",
  //   credits: "",
  //   assignments: [],
  //   midterms: [],
  //   finalExam: {
  //     present: false,
  //   },
  // };
});

function showAccordion(accordionID) {
  let target = document.querySelector(accordionID);
  new bootstrap.Collapse(target, {
    toggle: false,
  }).show();
}

const getRandomString = () => Math.random().toString(36).slice(2);

function addAssignment() {
  let newAssignmentID = 1;
  Array.from(document.querySelector("#assignments").children).forEach(
    (assignment) =>
      parseInt(assignment.dataset.id) >= newAssignmentID &&
      (newAssignmentID = parseInt(assignment.dataset.id) + 1)
  );
  let content = `<div
  class="accordion accordion-flush"
  id="assignment${newAssignmentID}-accordion" data-id="${newAssignmentID}"
>
  <div class="accordion-item">
    <h3 class="accordion-header" id="assignment${newAssignmentID}">
      <button
        class="accordion-button bg-transparent text-dark p-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#assignment${newAssignmentID}-collapse"
        aria-expanded="true"
        aria-controls="assignment${newAssignmentID}-collapse"
      >
        <p class="h5 assignment-name">Assignment </p>
        <div
          class="btn btn-light align-right"
          onclick="removeAssignment(${newAssignmentID})"
        >
          ❌
        </div>
      </button>
    </h3>
    <div class="accordion-body">
      <input hidden name="assignment-counter" value="${newAssignmentID}"/>
      <div
        class="accordion-collapse collapse show"
        id="assignment${newAssignmentID}-collapse"
        aria-labelledby="assignment${newAssignmentID}"
        data-bs-parent="#assignment${newAssignmentID}-accordion"
      >
        <div class="mb-3 row">
          <label for="assignment${newAssignmentID}-due-date" class="col-sm-2 col-form-label"
            >Due Date:</label
          >
          <div class="col-sm-5">
            <input
              type="date"
              class="form-control-plaintext border rounded px-1"
              id="assignment${newAssignmentID}-due-date"
              placeholder="Due Date"
              required
              name="assignment-${newAssignmentID}-date"
            />
          </div>
        </div>
        <div class="mb-3 row">
          <label
            for="assignment${newAssignmentID}-grade-weight"
            class="col-sm-2 col-form-label"
            >Grade Weight:</label
          >
          <div class="col-sm-5">
            <input
              type="number"
              class="form-control-plaintext border rounded px-1"
              id="assignment${newAssignmentID}-grade-weight"
              placeholder="Grade Weight"
              required
              name="assignment-${newAssignmentID}-gradeWeight"
            />
          </div>
        </div>
        <div
          class="accordion accordion-flush"
          id="assignment${newAssignmentID}-subtasks-accordion"
        >
          <div class="accordion-item">
            <h3
              class="accordion-header"
              id="assignment${newAssignmentID}-subtasks"
            >
              <button
                class="accordion-button bg-transparent text-dark p-2"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#assignment${newAssignmentID}-subtasks-collapse"
                aria-expanded="true"
                aria-controls="assignment${newAssignmentID}-subtasks-collapse"
              >
                <p class="h6">Subtasks</p>
                <div
                  class="btn btn-primary align-right"
                  onclick="showAccordion('#assignment${newAssignmentID}-subtasks-collapse');addSubtask(${newAssignmentID})"
                >
                  Add
                </div>
              </button>
            </h3>
            <div class="accordion-body">
              <div
                class="accordion-collapse collapse show"
                id="assignment${newAssignmentID}-subtasks-collapse"
                aria-labelledby="assignment${newAssignmentID}-subtasks"
                data-bs-parent="#assignment${newAssignmentID}-subtasks-accordion"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>`;
  document
    .querySelector("#assignments")
    .insertAdjacentHTML("beforeend", content);
  document.querySelector("#total-assignments").innerText = Array.from(
    document.querySelector("#assignments").children
  ).length;
}

function removeAssignment(assignmentID) {
  document
    .querySelector("#assignments")
    .removeChild(
      document.querySelector(`#assignment${assignmentID}-accordion`)
    );
  document.querySelector("#total-assignments").innerText = Array.from(
    document.querySelector("#assignments").children
  ).length;
}

function addSubtask(assignmentID) {
  let randomID = getRandomString();
  let content = `<div class="mb-3 row subtask">
  <label
  for="assignment${assignmentID}-subtask-${randomID}"
  class="col-sm-1 col-form-label"
  >.
  </label>
  <div class="col-sm-6">
  <input
  type="text"
  class="form-control-plaintext border rounded px-1"
  id="assignment${assignmentID}-subtask-${randomID}"
  placeholder="Subtask"
  name="assignment-${assignmentID}-subTask"
  />
  </div>
  <div class="col-sm-1 align-right">
  <div
  class="btn btn-light align-right"
  onclick="document
  .querySelector('#assignment${assignmentID}-subtasks-collapse').removeChild(this.parentNode.parentNode)"
        >
        ❌
        </div>
        </div>
  </div>`;
  document
    .querySelector(`#assignment${assignmentID}-subtasks-collapse`)
    .insertAdjacentHTML("beforeend", content);
}

function addMidterm() {
  let newMidtermID = 1;
  Array.from(document.querySelector("#midterms").children).forEach(
    (assignment) =>
      parseInt(assignment.dataset.id) >= newMidtermID &&
      (newMidtermID = parseInt(assignment.dataset.id) + 1)
  );
  let content = `<div
    class="accordion accordion-flush midterm"
    id="midterm${newMidtermID}-accordion"
    data-id="${newMidtermID}"
  >
    <div class="accordion-item">
      <h2 class="accordion-header" id="midterm${newMidtermID}-heading">
        <button
          class="accordion-button bg-transparent text-dark p-2"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#midterm${newMidtermID}"
          aria-expanded="true"
          aria-controls="midterm${newMidtermID}"
        >
          <p class="h5">Midterm </p>
          <div class="btn btn-light align-right" onclick='removeMidterm(${newMidtermID})'>
            ❌
          </div>
        </button>
      </h2>
      <div class="accordion-body">
      <input hidden name="midterm-counter" value="${newMidtermID}"/>
        <div
          id="midterm${newMidtermID}"
          class="accordion-collapse collapse show"
          aria-labelledby="midterm${newMidtermID}-heading"
          data-bs-parent="#midterm${newMidtermID}-accordion"
        >
          <div class="mb-3 row">
            <label
              for="midterm${newMidtermID}-date"
              class="col-sm-2 col-form-label"
              >Date:</label
            >
            <div class="col-sm-4">
              <input
                type="date"
                class="form-control-plaintext border rounded px-1"
                id="midterm${newMidtermID}-date"
                required="required"
                name="midterm-${newMidtermID}-date"
              />
            </div>
          </div>
          
          </div>
          
          <div class="mb-3 row">
            <label
              for="midterm${newMidtermID}-grade-weight"
              class="col-sm-2 col-form-label"
              >Grade Weight:</label
            >
            <div class="col-sm-4">
              <input
                type="text"
                class="form-control-plaintext border rounded px-1"
                id="midterm${newMidtermID}-grade-weight"
                required="required"
                placeholder="Grade Weight"
                name="midterm-${newMidtermID}-gradeWeight"
              />
            </div>
          </div>
          <div
            class="accordion accordion-flush"
            id="midterm${newMidtermID}-materials-accordion"
          >
            <div class="accordion-item">
              <h4
                class="accordion-header"
                id="midterm${newMidtermID}-materials-accordion-header"
              >
                <button
                  class="accordion-button bg-transparent text-dark p-2"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#midterm${newMidtermID}-materials"
                  aria-expanded="true"
                  aria-controls="midterm${newMidtermID}-materials"
                >
                  <p class="h6">Materials Covered:</p>
                  <div
                    class="btn btn-primary align-right"
                    onclick="showAccordion('#midterm${newMidtermID}-materials');addMidtermMaterials(${newMidtermID})"
                  >
                    Add
                  </div>
                </button>
              </h4>
              <div class="accordion-body">
                <div
                  id="midterm${newMidtermID}-materials"
                  class="accordion-collapse collapse show"
                  aria-labelledby="midterm${newMidtermID}-materials-accordion-header"
                  data-bs-parent="#midterm${newMidtermID}-materials-accordion"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`;
  document.querySelector("#midterms").insertAdjacentHTML("beforeend", content);
  document.querySelector("#total-midterms").innerText = Array.from(
    document.querySelector("#midterms").children
  ).length;
}

function removeMidterm(midtermID) {
  document
    .querySelector("#midterms")
    .removeChild(document.querySelector(`#midterm${midtermID}-accordion`));
  document.querySelector("#total-midterms").innerText = Array.from(
    document.querySelector("#midterms").children
  ).length;
}

function addMidtermMaterials(midtermID) {
  let randomID = getRandomString();
  let content = `<div class="mb-3 row material">
    <label
      for="midterm${midtermID}-material-${randomID}"
      class="col-sm-1 col-form-label"
      >.</label
    >
    <div class="col-sm-6">
      <input
        type="text"
        class="form-control-plaintext border rounded px-1"
        id="midterm${midtermID}-material-${randomID}"
        placeholder="Material"
        name="midterm-${midtermID}-subTask"
      />
    </div>
    <div class="col-sm-1 align-right">
      <div
      class="btn btn-light align-right"
      onclick="document
        .querySelector('#midterm${midtermID}-materials').removeChild(this.parentNode.parentNode)"
      >
        ❌
      </div>
    </div>
  </div>`;
  document
    .querySelector(`#midterm${midtermID}-materials`)
    .insertAdjacentHTML("beforeend", content);
}

function addFinalExam() {
  let content = `<div style="display: flex; justify-content: space-between">
    <h5>Final Exam</h5>
    <div class="btn btn-light" onclick='document.querySelector("#final-exam").innerHTML = "";document.querySelector("#final-exam-add-btn").style.display = "inline-block";document.querySelector("#is-final-exam").innerText = "No"'>❌</div>
  </div>
  <div class="p-3 pt-0">
    <div class="mb-3 row">
      <label for="final-exam-date" class="col-sm-2 col-form-label"
        >Date:</label
      >
      <div class="col-sm-4">
        <input
          type="date"
          class="form-control-plaintext border rounded px-1"
          id="final-exam-date"
          required="required"
          name="finalExamDate"
        />
        <input hidden name="has_FinalExam" value="True"/>
      </div>
    </div>
    
    <div class="mb-3 row">
      <label
        for="final-exam-grade-weight"
        class="col-sm-2 col-form-label"
        >Grade Weight:</label
      >
      <div class="col-sm-4">
        <input
          type="text"
          class="form-control-plaintext border rounded px-1"
          id="final-exam-grade-weight"
          required="required"
          placeholder="Grade Weight"
          name="fianlExamGradeWeight"
        />
      </div>
    </div>
    <div
      class="accordion accordion-flush"
      id="final-exam-materials-accordion"
    >
      <div class="accordion-item">
        <h4
          class="accordion-header"
          id="final-exam-materials-accordion-header"
        >
          <button
            class="accordion-button bg-transparent text-dark p-2"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#final-exam-materials"
            aria-expanded="true"
            aria-controls="final-exam-materials"
          >
            <p class="h6">Materials Covered:</p>
            <div
              class="btn btn-primary align-right"
              onclick="showAccordion('#final-exam-materials'); addFinalExamMaterials();"
            >
              Add
            </div>
          </button>
        </h4>
        <div class="accordion-body">
          <div
            id="final-exam-materials"
            class="accordion-collapse collapse show"
            aria-labelledby="final-exam-materials-accordion-header"
            data-bs-parent="#final-exam-materials-accordion"
          ></div>
        </div>
      </div>
    </div>
  </div>`;
  document.querySelector("#final-exam").innerHTML = content;
  document.querySelector("#final-exam-add-btn").style.display = "none";
  document.querySelector("#is-final-exam").innerText = "Yes";
}

function addFinalExamMaterials() {
  let randomID = getRandomString();
  let content = `<div class="mb-3 row material">
        <label
          for="final-exam-material-${randomID}"
          class="col-sm-1 col-form-label"
          >.</label
        >
        <div class="col-sm-6">
          <input
            type="text"
            class="form-control-plaintext border rounded px-1"
            id="final-exam-material-${randomID}"
            placeholder="Material"
            name="finalExamMaterial"
          />
        </div>
        <div class="col-sm-1 align-right">
          <div
          class="btn btn-light align-right"
          onclick="document
            .querySelector('#final-exam-materials').removeChild(this.parentNode.parentNode)"
          >
            ❌
          </div>
        </div>
      </div>`;
  document
    .querySelector("#final-exam-materials")
    .insertAdjacentHTML("beforeend", content);
}
