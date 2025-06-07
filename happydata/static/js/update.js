function updateFileName() {
  const input = document.getElementById('fileInput');
  const fileName = document.getElementById('fileName');
  fileName.textContent = input.files.length ? input.files[0].name : 'No file selected';
  }
    