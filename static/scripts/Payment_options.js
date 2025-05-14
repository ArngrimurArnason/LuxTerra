
const tabs = document.querySelectorAll('.tab-header');
const forms = document.querySelectorAll('.form-tab');

tabs.forEach(tab => {
tab.addEventListener('click', () => {
  // Switch active tab
  tabs.forEach(t => t.classList.remove('active-tab'));
  tab.classList.add('active-tab');

  // Show the right form
  const target = tab.getAttribute('data-target');
  forms.forEach(form => {
    form.classList.toggle('d-none', form.id !== target);
  });
});
});
