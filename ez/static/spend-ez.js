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
      if (val.length <= 0 || val <= 150) { //remove outliers 
        val = 150;
      }
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

//TODO
// All imgs local, change titles
/*
window.onload = feedback

function feedback () {
  var img = document.getElementById('howIfeel');
  var bPerc = document.getElementById("bPerc");
  var pVal = Number(bPerc.getAttribute("value"));
  if(pVal >= 120.00){
    img.src = "https://img.icons8.com/ios/50/000000/headstone.png";
  }else if(pVal >= 90.00){
    img.src = "https://img.icons8.com/ios/50/000000/sad.png";
  }else if(pVal >= 75.00){
    img.src = "https://icons8.com/icon/25542/embarrassed";
  }else{
    img.src = "https://img.icons8.com/ios/50/000000/happy.png";
  }
}
*/