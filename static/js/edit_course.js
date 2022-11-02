let newAssignmentID = 1;
let newMidtermID = 1;
let newSubtaskItemID = 1;

const assignmentContainer = document.querySelector("#assignments");
const totalAssignments = document.querySelector("#total-assignments");
const assignmentsCount = countChildren(assignmentContainer);

const midtermContainer = document.querySelector("#midterms");
const midtermsCount = countChildren(midtermContainer);
const totalMidterms = document.querySelector("#total-midterms");

const examHeader = document.querySelector("#exam-header");
const examHasChildren = countChildren(examHeader);

const addFinalExamBtn = document.querySelector("#addFinalExamBtn");
const deleteFinalExamBtn = document.querySelector("#deleteFinalExamBtn");
const finalExamStatusSpan = document.querySelector(
  "#finalExamStatusSpan"
);

const subtaskContainer = document.querySelector("#subtaskItems");
const subtasksCount = countChildren(subtaskContainer);

if (examHasChildren) {
  hideAddExamButton();
} else {
  showAddExamButton();
}

function deleteFinalExam(e) {
  e.preventDefault();
  document.querySelector("#exam-header .accordion-body").remove();
  showAddExamButton();
  updateFinalExamStatus();
}

function updateFinalExamStatus() {
  if (countChildren(examHeader)) {
    finalExamStatusSpan.innerText = "Yes";
  } else {
    finalExamStatusSpan.innerText = "No";
  }
}

updateFinalExamStatus();

function addFinalExam(e) {
  e.preventDefault();
  hideAddExamButton();
  let finalExamAccordionBody = `
  <div class="accordion-body">
                  <strong>Grade Weight: <span></span></strong>
                  <strong><br><br>Date:<span></span></strong>
                  <strong><br><br>Grade Weight:<span></span></strong>
                  <strong><br><br>Material Covered:</strong>
                  <ol type="1">
                    <li>Create classes</li>
                    <li>Create database</li>
                    <li>Static Pages</li>
                    <li>Add functionalities</li>
                  </ol>
                  <!--here-->
                </div>
        `;
  examHeader.insertAdjacentHTML("beforeend", finalExamAccordionBody);
  updateFinalExamStatus();
}

function hideAddExamButton() {
  addFinalExamBtn.style.display = "none";
  deleteFinalExamBtn.style.display = "block";
}
function showAddExamButton() {
  addFinalExamBtn.style.display = "block";
  deleteFinalExamBtn.style.display = "none";
}
function countChildren(node) {
  return Array.from(node.children).length;
}

function deleteAssignment(id) {
  let deletionResponse = confirm(
    "Are you sure you want to delete the chosen assignment"
  );

  if (deletionResponse) {
    document.getElementById(`task${id}`).remove();
    const assignmentsCountAfterDeletion =
      countChildren(assignmentContainer);
    let newAssignmentCount = assignmentsCountAfterDeletion;
    totalAssignments.innerText = newAssignmentCount--;
  }
}

function addAssignment(e) {
  e.preventDefault();
  newAssignmentID += assignmentsCount;
  let assignment = `
  <div class="accordion-item task" id="task${newAssignmentID}" data-id="${newAssignmentID}">
                    <h2 class="accordion-header" id="heading2">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse${newAssignmentID}" aria-expanded="false" aria-controls="flush-collapseThree">
                        <p class="h4">
                            Assignment <!--<span id="total-assignments">0</span> -->
                        </p>
                          <div
                        class="btn btn-light align-right"
                        onclick="deleteAssignment(${newAssignmentID})"
                        data-target='assignment${newAssignmentID}'
                        "
                      >
                        ❌
                      </div>
                      </button>

                    </h2>
                    <div id="flush-collapse${newAssignmentID}" class="accordion-collapse collapse" aria-labelledby="flush-heading${newAssignmentID}" data-bs-parent="#accordionFlushExample">
                      <div class="accordion-body">
                          <strong>Course Name: <span></span></strong>
                          <strong><br><br>Grade Weight:<span></span></strong>
                          <strong><br><br>Due Date:<span></span></strong>
                          <strong><br><br>Sub-Tasks:</strong>
                          <ol type="1">
                            <li>Create classes</li>
                            <li>Create database</li>
                            <li>Static Pages</li>
                            <li>Add functionalities</li>
                          </ol>
                        <!--here-->
                      </div>
                    </div>
                    <!-- Modal -->
                    <div class="modal fade" id="assignment${newAssignmentID}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                      <div class="modal-dialog" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Confirm deletion !!</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                              <span aria-hidden="true">&times;</span>
                            </button>
                          </div>
                          <div class="modal-body">
                            Are sure you want to delete Assignment ${newAssignmentID} !!?
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Delete</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  `;

  assignmentContainer.insertAdjacentHTML("beforeend", assignment);
  const updatedAssignmentsCount = countChildren(assignmentContainer);

  totalAssignments.innerText = updatedAssignmentsCount;
}

function addMidterm(e) {
  e.preventDefault();
  newMidtermID += midtermsCount;
  let midterm = ` <div class="accordion-item midterm" id="midterm${newMidtermID}" data-id="${newMidtermID}">
                      <h2 class="accordion-header" id="heading2">
                        <button
                          class="accordion-button collapsed"
                          type="button"
                          data-bs-toggle="collapse"
                          data-bs-target="#mid-${newMidtermID}"
                          aria-expanded="false"
                          aria-controls="mid-${newMidtermID}"
                        >
                          <p class="h4">
                            Midterm
                          </p>
                            <div
                            class="btn btn-light align-right"
                            onclick="deleteMidterm(${newMidtermID})"
                          >
                            ❌
                          </div>
                        </button>
                      </h2>
                      <div
                        id="mid-${newMidtermID}"
                        class="accordion-collapse collapse"
                        aria-labelledby="mid-${newMidtermID}"
                        data-bs-parent="#accordionFlushExample"
                      >
                        <div class="accordion-body">
                          <strong>Grade Weight:<span></span></strong>
                          <strong><br /><br />Date:<span></span></strong>
                          <strong><br /><br />Material Covered:</strong>
                          <ol type="1">
                            <li>Create classes</li>
                            <li>Create database</li>
                            <li>Static Pages</li>
                            <li>Add functionalities</li>
                          </ol>
                          <!--here-->
                        </div>
                      </div>
                    </div>`;

  midtermContainer.insertAdjacentHTML("beforeend", midterm);
  const updatedMidtermsCount = countChildren(midtermContainer);
  totalMidterms.innerText = updatedMidtermsCount;
}

function deleteMidterm(id) {
  let deletionResponse = confirm(
    "Are you sure you want to delete the chosen Midterm"
  );

  if (deletionResponse) {
    document.getElementById(`midterm${id}`).remove();
    const midtermsCountAfterDeletion = countChildren(midtermContainer);
    let newMidtermCount = midtermsCountAfterDeletion;
    totalMidterms.innerText = newMidtermCount--;
  }
}

function addSubtaskItem(e) {
  e.preventDefault();
  newSubtaskItemID += subtasksCount;
  const subtaskItemContent = `
      <li id="subtaskItem${newSubtaskItemID}">
          <div>
            <input
              class="form-control"
              value="new subtask"
              id="subtaskItemInput${newSubtaskItemID}"
            />
            <div
              class="btn btn-light align-right"
              onclick="deleteSubtaskItem(${newSubtaskItemID})"
            >
              ❌
            </div>
          </div>
      </li>`;

  subtaskContainer.insertAdjacentHTML("beforeend", subtaskItemContent);
}

function deleteSubtaskItem(subTaskItemID) {

  document.getElementById(`subtaskItem${subTaskItemID}`).remove();

}