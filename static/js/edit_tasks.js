let inputSubTasks = document.getElementsByClassName("subtask")
//console.log(inputSubTasks.length)
//$('.delete-subtask').on('click', deleteSubTask);

//deletes the subtask: input box and button (sibling)
function deleteSubTask(){

    console.log("clicked")
    //e.preventDefault();
    this.nextElementSibling.remove();
    this.remove();
}

// for (let i = 0; i<inputSubTasks.length;i++){
//   if(inputSubTasks){
//     //print(inputSubTasks.length)
//     inputSubTasks[i].addEventListener("click", function(){
//     this.nextElementSibling.remove();
//     this.remove();
//   });
//   }
  
// }


$('.add').on('click', addSubtaskInput);
let subTaskList = document.getElementById("subTaskList")
//appends a subtask to the existing subtask list
function addSubtaskInput(e){
    let randomID = getRandomString();
    e.preventDefault();
    let inputHtml =`<div>
                        <button class="delete-subtask" onclick="deleteSubTask(this)" id=${randomID}>❌</button>
                        <input type="text" placeholder="Enter subtasks/material">    
                    </div>`;
    $('#subTaskList').append(inputHtml);
}
