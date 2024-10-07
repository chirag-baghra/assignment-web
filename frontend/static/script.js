document.getElementById("valueForm").onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission

    const value1 = document.getElementById("value1").value;
    const value2 = document.getElementById("value2").value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Set the content type
        },
        body: JSON.stringify({ value1: value1, value2: value2 }) // Send JSON data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Show a success message
        alert(data.message || "Values submitted successfully!");

        // Clear the form fields after submission
        document.getElementById("valueForm").reset();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Show an error message
        alert('Error submitting values: ' + error.message);
    });
};
