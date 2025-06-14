document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("fill-form");

  form.addEventListener("submit", function (e) {
    e.preventDefault();  

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/calculate/calculating/', {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("fileNameInput").value = data.file_name_inp;
      document.getElementById("NumberOfRowsInput").value = data.number_of_rows;
      document.getElementById("NumberOfColumnsInput").value = data.number_of_col;
      document.getElementById("NumberOfNumericalValues").value = data.number_of_num_val;
      document.getElementById("NumberOfCategorialValues").value = data.number_of_cat_val;
      document.getElementById("NumberOfMissingValues").value = data.number_of_miss_val;
      document.getElementById("Message1").value = data.mess1;
    })
    .catch(error => {
      document.getElementById("Message2").value =  error;
    });
  });
});
