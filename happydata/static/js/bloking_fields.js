document.addEventListener("DOMContentLoaded", function () {
    const selectPlot = document.getElementById("select_plot");
    const inputs = document.querySelectorAll('.select-choices input[type="text"]');

    function updateInputState() {
      const selected = selectPlot.value;

      if (selected === "heatmap") { 
        inputs.forEach(input => input.disabled = true);
      } else if (selected === "hystogram") {  
        inputs[0].disabled = false;
        inputs[1].disabled = true;
      } else {
        inputs.forEach(input => input.disabled = false);
      }
    }

    selectPlot.addEventListener("change", updateInputState);
    updateInputState();
});