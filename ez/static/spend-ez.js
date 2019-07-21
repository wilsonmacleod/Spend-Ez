window.onload = feedback;

function feedback() { //"budget spent" feedback controller
  var img = document.getElementById('howIfeel');
  var bPerc = document.getElementById("bPerc");
  var pVal = Number(bPerc.getAttribute("value"));
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

document.getElementById("revealButton").addEventListener("click", function () { //"Update Budget Button"
  this.classList.toggle("hidden");
  document.getElementById('budgeUpdateForm').classList.toggle("hidden");

  var rangeFinder = document.getElementById("budget-range"); //slider
  var currentBudge = document.getElementById("budget_qty"); //form value

  currentBudge.innerText = rangeFinder.value;

  rangeFinder.oninput = function () {
    currentBudge.innerHTML = this.value;
    rangeFinder.title = this.value;
    var hiddenForm = document.getElementById("budget-form"); //update Python form 
    hiddenForm.value = currentBudge.innerHTML;
  }

  currentBudge.addEventListener("click", function () { //functions triggered by user clicking on form value
    function toggleHidden() { //function to hide/reveal other form attributes 
      document.getElementById('slidecontainer').toggleAttribute("hidden");
      document.getElementById('buSubmit').toggleAttribute("hidden");
    }
    toggleHidden();
    var inputField = document.createElement("input");
    inputField.type = "text";
    inputField.classList.add("inputField");
    inputField.value = currentBudge.innerText;
    currentBudge.innerHTML = '';
    currentBudge.appendChild(inputField);
    inputField.focus();
    inputField.onblur = function () { //when user "submits" form value
      toggleHidden();
      let val = '';
      for (x = 0; x < inputField.value.length; x++) {
        if (!isNaN(inputField.value[x])) { //remove non ints
          val += inputField.value[x];
        } else {
          continue;
        }
      }
      (val.length <= 0 || val <= 150)?val=150:val=val; //remove outliers 
      currentBudge.removeChild(inputField);
      currentBudge.innerHTML = val;
      var hiddenForm = document.getElementById("budget-form");
      hiddenForm.value = val;
    }
  })
  document.getElementById("budgetIncrease").addEventListener("click", function () { //increase budget scale incrementally
    var r = Number(rangeFinder.max);
    r += 100;
    rangeFinder.max = r;
  })
  document.getElementById("buSubmit").addEventListener("click", function () { //flip back to the beginning when we submit
    document.getElementById("revealButton").click();
  })
})

document.getElementById("seeMoreTotals").addEventListener("click", function () { //modal revealer for year totals
  var container = document.getElementById("seeMoreModal");
  container.style.visibility = (container.style.visibility == "visible") ? "hidden" : "visible";
})

var aTitle = document.querySelectorAll('.acc'); //accordian for modal
var c = document.querySelectorAll('.con');
for (var x = 0; x < aTitle.length; x++) {
  aTitle[x].onclick = function () {
    cCon(this.nextElementSibling);
    this.nextElementSibling.classList.toggle('ac-active');
  }
}

function cCon(t) {
  for (var x = 0; x < c.length; x++) {
    if (t != c[x]) {
      c[x].classList.remove('ac-active');
    }
  }
}
