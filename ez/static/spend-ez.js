var rangeFinder = document.getElementById("budget-range");
var hiddenForm = document.getElementById("budget-form");
var currentBudge = document.getElementById("budget_qty");

currentBudge.innerText = rangeFinder.value;

rangeFinder.oninput = function () {
  currentBudge.innerHTML = this.value;
  rangeFinder.title = this.value;
  hiddenForm.value = currentBudge.innerHTML;
}

currentBudge.addEventListener("click", function () {
  var inputField = document.createElement("input");
  inputField.type = "text";
  inputField.value = currentBudge.innerText;
  currentBudge.innerHTML = '';
  currentBudge.appendChild(inputField);
  inputField.focus();
  inputField.onblur = function () {
    let val = '';
    for (x = 0; x < inputField.value.length; x++) {
      if (!isNaN(inputField.value[x])) {
        val += inputField.value[x];
      } else {
        continue;
      }
    }
    currentBudge.removeChild(inputField);
    currentBudge.innerHTML = val;
    hiddenForm.value = val;
  }
})
document.getElementById("budgetIncrease").addEventListener("click", function () {
  var r = Number(rangeFinder.max);
  r += 100;
  rangeFinder.max = r;
})