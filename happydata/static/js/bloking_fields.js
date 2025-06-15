document.addEventListener("DOMContentLoaded", function () {
    const selectPlot = document.getElementById("select_plot");
    const inputs = document.querySelectorAll('.select-choices input[type="text"]');
    const targetInput = document.getElementById('target_input');

    function updateInputState() {
      const selected = selectPlot.value;

      if (targetInput) {
            targetInput.disabled = false;
            targetInput.readOnly = false;
      }

      if (selected === "heatmap") { 
        inputs.forEach(input => input.disabled = true);
        targetInput.disabled = false;
      } else if (selected === "hystogram") {  
        inputs[0].disabled = false;
        targetInput.disabled = false;
        inputs[1].disabled = true;
      } else {
        inputs.forEach(input => input.disabled = false);
      }
    }

    selectPlot.addEventListener("change", updateInputState);
    updateInputState();
});