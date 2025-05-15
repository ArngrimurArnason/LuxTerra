 document.addEventListener("DOMContentLoaded", function () {
    const methodSelect = document.getElementById('method-select');
    const creditFields = document.getElementById('credit_card_fields');
    const bankFields = document.getElementById('bank_transfer_fields');
    const mortgageFields = document.getElementById('mortgage_fields');

    function toggleFields(method) {
      creditFields.style.display = method === 'credit_card' ? 'block' : 'none';
      bankFields.style.display = method === 'bank_transfer' ? 'block' : 'none';
      mortgageFields.style.display = method === 'mortgage' ? 'block' : 'none';
    }

    // Set initial state
    toggleFields(methodSelect.value);

    // Change on select
    methodSelect.addEventListener('change', () => {
      toggleFields(methodSelect.value);
    });
  });
