document.addEventListener('DOMContentLoaded', function () {
  const methodSelect = document.getElementById('method-select');

  const creditCardFields = document.getElementById('credit_card_fields');
  const bankTransferFields = document.getElementById('bank_transfer_fields');
  const mortgageFields = document.getElementById('mortgage_fields');

  function toggleFields() {
    const method = methodSelect.value;

    // Hide all first
    creditCardFields.style.display = 'none';
    bankTransferFields.style.display = 'none';
    mortgageFields.style.display = 'none';

    // Show only the selected
    if (method === 'credit_card') {
      creditCardFields.style.display = 'block';
    } else if (method === 'bank_transfer') {
      bankTransferFields.style.display = 'block';
    } else if (method === 'mortgage') {
      mortgageFields.style.display = 'block';
    }
  }

  // Initial state
  toggleFields();

  // On change
  methodSelect.addEventListener('change', toggleFields);
});
