document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab-header");
  const forms = document.querySelectorAll(".form-tab");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active-tab"));
      forms.forEach(f => f.classList.add("d-none"));

      tab.classList.add("active-tab");
      const targetId = tab.dataset.target;
      const targetForm = document.getElementById(targetId);
      if (targetForm) {
        targetForm.classList.remove("d-none");
      }
    });
  });
});