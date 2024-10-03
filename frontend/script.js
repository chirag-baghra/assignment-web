document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const value1 = document.getElementById('value1').value;
    const value2 = document.getElementById('value2').value;

    // Basic validation
    if (value1 === "" || value2 === "") {
        document.getElementById('message').innerText = "Please fill in all fields.";
        return;
    }

    // If valid, display a success message
    document.getElementById('message').innerText = `Values submitted: ${value1}, ${value2}`;
});
