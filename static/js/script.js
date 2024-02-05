document.getElementById('submit').addEventListener('click', function () {
    // Show correct answer
    document.getElementById('correct-result').innerText = correct_answer_country;
    document.getElementById('results-additional-info').innerText = correct_answer_additional_info;
    document.getElementById('correct-result-text').style.display = 'block';

    // Mark correct answer on page
    const options = document.querySelectorAll('input[type="radio"]');
    options.forEach(function (option) {
        if (option.value === correctCountryOption) {
            const label_id = option.id.slice(-1); // Extract the last character from option.id
            const label = document.getElementById('label_' + label_id);
            label.classList.add('btn', 'btn-outline-success', 'correct-option');
            label.setAttribute('for', 'success-outlined');
        }
    });
});