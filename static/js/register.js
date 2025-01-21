const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector('.input_feedback');
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.emailFeedback');
const usernameoutput = document.querySelector('.usernameoutput');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');
const submitbtn = document.querySelector('.submit-btn');

//show password

const handletoggle = (e) => {
    if (showPasswordToggle.textContent === 'SHOW') {
        showPasswordToggle.textContent = 'HIDE';
        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute('type', 'password');
    }
};


showPasswordToggle.addEventListener('click' ,handletoggle)

// Email Validation
emailField.addEventListener('input', (e) => {
    const emailVal = e.target.value.trim(); // Trim unnecessary spaces
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch('/authenciation/validate-email', {
            method: 'POST',
            body: JSON.stringify({ email: emailVal }),
            headers: {
                'Content-Type': 'application/json' // Ensure proper headers for JSON
            }
        })
        .then(res => res.json())
        .then((data) => {
            console.log(data);
            if (data.email_error) { // Ensure we use the correct key for error message
                submitbtn.disabled = true;
                usernameoutput.style.display = "none";
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
            else {
                submitbtn.removeAttribute("disabled");
            }
        })
        .catch((err) => {
            console.error('Error validating email:', err);
        });
    }
});

// Username Validation
usernameField.addEventListener('input', (e) => {
    const usernameVal = e.target.value.trim();
    // Trim unnecessary spaces
    usernameoutput.style.display = "block";
    usernameoutput.textContent= `checking ${usernameVal}`;
    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = "none";

    if (usernameVal.length > 0) {
        fetch('/authenciation/validate-username', {
            method: 'POST',
            body: JSON.stringify({ username: usernameVal }),
            headers: {
                'Content-Type': 'application/json' // Ensure proper headers for JSON
            }
        })
        .then(res => res.json())
        .then((data) => {
            console.log(data);
            usernameoutput.style.display = "none";
            if (data.error) { // Ensure we use the correct key for error message
                usernameField.classList.add('is-invalid');
                feedbackField.style.display = "block";
                feedbackField.innerHTML = `<p>${data.error}</p>`;
                submitbtn.disabled = true;
            }
            else{
                submitbtn.removeAttribute("disabled");
            }
        })
        .catch((err) => {
            console.error('Error validating username:', err);
        });
    }
});
