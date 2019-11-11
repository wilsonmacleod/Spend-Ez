window.onload = budgetFeedback;

//budget spent feedback controller

function budgetFeedback() {
  let img = document.getElementById("howIfeel");
  const bPerc = document.getElementById("bPerc");
  const pVal = Number(bPerc.getAttribute("value"));
  if (pVal >= 130.00) {
    img.src = "/static/icons/rip.jpg";
    img.title = "Better luck next month....";
  } else if (pVal >= 100.00) {
    img.src = "/static/icons/sad.jpg";
    img.title = "You've maxed your budget.";
  } else if (pVal >= 75.00) {
    img.src = "/static/icons/emb.jpg";
    img.title = "You're almost to your max spend.";
  } else {
    img.src = "/static/icons/happy.jpg";
    img.title = "You're doing great this month!";
  }
}

//update budget button controls 

document.getElementById("revealButton").addEventListener("click", function () { //controls the update budget button
  this.classList.toggle("hidden");
  document.getElementById("budgeUpdateForm").classList.toggle("hidden");

  let rangeFinder = document.getElementById("budget-range"); //slider
  let currentBudge = document.getElementById("budget_qty"); //form value

  currentBudge.innerText = rangeFinder.value;

  rangeFinder.oninput = function () {
    currentBudge.innerHTML = this.value;
    rangeFinder.title = this.value;
    const hiddenForm = document.getElementById("budget-form"); //update Python form 
    hiddenForm.value = currentBudge.innerHTML;
  }

  currentBudge.addEventListener("click", function () { //functions triggered by user clicking on form value
    toggleHidden = function () { //function to hide/reveal other form attributes 
      document.getElementById("slidecontainer").toggleAttribute("hidden");
      document.getElementById("buSubmit").toggleAttribute("hidden");
    }
    toggleHidden();
    var inputField = document.createElement("input");
    inputField.type = "text";
    inputField.classList.add("inputField");
    inputField.value = currentBudge.innerText;
    currentBudge.innerHTML = "";
    currentBudge.appendChild(inputField);
    inputField.focus();
    inputField.onblur = function () { //when user "submits" form value
      toggleHidden();
      let val = "";
      for (x = 0; x < inputField.value.length; x++) {
        if (!isNaN(inputField.value[x])) { //remove non ints
          val += inputField.value[x];
        } else {
          continue;
        }
      }
      (val.length <= 0 || val <= 150) ? val = 150: val = val; //remove outliers 
      currentBudge.removeChild(inputField);
      currentBudge.innerHTML = val;
      const hiddenForm = document.getElementById("budget-form");
      hiddenForm.value = val;
    }
  })

  document.getElementById("budgetIncrease").addEventListener("click", function () { //increase budget scale incrementally
    let r = Number(rangeFinder.max);
    r += 100;
    rangeFinder.max = r;
  })
  document.getElementById("buSubmit").addEventListener("click", function () { //flip back to the beginning when we submit
    document.getElementById("revealButton").click();
  })
})

//"SEE MORE HERE" button and modal reveal

document.getElementById("seeMoreTotals").addEventListener("click", function () {
  const container = document.getElementById("seeMoreModal");
  container.style.visibility = (container.style.visibility == "visible") ? "hidden" : "visible";
})

//accordian controls for modal

const aTitle = document.querySelectorAll(".acc");
const c = document.querySelectorAll(".con");
for (let x = 0; x < aTitle.length; x++) {
  aTitle[x].onclick = function () {
    cCon(this.nextElementSibling);
    this.nextElementSibling.classList.toggle("ac-active");
  }
}

function cCon(t) {
  for (let x = 0; x < c.length; x++) {
    if (t != c[x]) {
      c[x].classList.remove("ac-active");
    }
  }
}

//edit Transaction Controls

let editBtns = document.getElementsByClassName("editTrans");
if(editBtns.length > 0){
  for (let x = 0; x <= editBtns.length - 1; x++){
    editBtns[x].addEventListener("click", function () {
    const container = document.getElementById("TransModal");
    container.style.visibility = (container.style.visibility == "visible") ? "hidden" : "visible";
  })}
}

document.getElementById("etClose").addEventListener("click", function () {
  const container = document.getElementById("TransModal");
  container.style.visibility = (container.style.visibility == "visible") ? "hidden" : "visible";
})