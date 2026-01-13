async function submitData() {
  const files = document.getElementById("resumes").files;
  const jobDesc = document.getElementById("jobDesc").value;

  const formData = new FormData();
  for (let file of files) {
    formData.append("resumes", file);
  }
  formData.append("job_description", jobDesc);

  const res = await fetch("/analyze", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("results").innerHTML =
    JSON.stringify(data, null, 2);
}
