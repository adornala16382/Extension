document.addEventListener("DOMContentLoaded", function () {

    let jsonObj;

    fetch('http://127.0.0.1:5000/get_assignments')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Process the response data here
        console.log(data);
        // Assign the JSON object to a JavaScript variable
        jsonObj = data;
        // Now you can use jsonObj as a JavaScript variable
        runNextCode();
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });

    function runNextCode() {
        let lateAssignments = jsonObj['LATE_ASSIGNMENTS']
        let dueAssignments = jsonObj['DUE_ASSIGNMENTS']
        console.log(dueAssignments.length)
        const numDueAssignments = dueAssignments.length
        const numLateAssignments = lateAssignments.length

        console.log(lateAssignments)
        console.log(dueAssignments)
        var dueAssignmentList = []
        var lateAssignmentList = []

        const healthValue = 0;     // Example health value, you can change this dynamically

        for (var i=0; i < numDueAssignments; i++) {
            var dueAssignment = dueAssignments[i]
            var timeDue = dueAssignment["DUE_DATE"]
            const timestamp = Date.parse(timeDue);
            var timeLeft = timestamp - Date.now();
            const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));

            var className = dueAssignment["CLASS_NAME"]
            var openUntil = dueAssignment["OPEN_UNTIL"]
            var assignmentName = dueAssignment["ASSIGNMENT_NAME"]
            dueAssignmentList.push("Due in [" + days + "] days, [" + hours + "] hours, [" + minutes + "] minutes\t" + assignmentName + "\t" + className + "\t" + openUntil)
        }

        for (var i=0; i < numLateAssignments; i++) {
            var lateAssignment = lateAssignments[i]
            var timeDue = lateAssignment["DUE_DATE"]
            var className = lateAssignment["CLASS_NAME"]
            var openUntil = lateAssignment["OPEN_UNTIL"]
            var assignmentName = lateAssignment["ASSIGNMENT_NAME"]
            lateAssignmentList.push(timeDue + "\t" + assignmentName + "\t" + className + "\t" + openUntil)
        }

        var ul1 = document.getElementById("due-assignment-list");

        dueAssignmentList.forEach(function (assignmentName) {
            var li1 = document.createElement("li");
            li1.textContent = assignmentName;
            ul1.appendChild(li1);
        });

        var ul2 = document.getElementById("late-assignment-list");

        lateAssignmentList.forEach(function (assignmentName) {
            var li2 = document.createElement("li");
            li2.textContent = assignmentName;
            ul2.appendChild(li2);
        });

        // Set the width of the health bar fill
        document.getElementById('health').value = healthValue;

        // Get the toggle switch element
        const toggleSwitch = document.getElementById('toggleSwitch');

        // Get the image element
        const animalImage = document.getElementById('animalImage');

        function updateImage(){
            console.log("1")
            // Check if the toggle switch is checked
            if (this.checked) {
                console.log("2")
                // If checked, set the image src to the cat image
                if (healthValue <= 0) {
                    animalImage.src = 'images/death.gif';
                }
                else if (healthValue < 33) {
                    animalImage.src = 'images/sad_cat.gif';
                }
                else if (healthValue < 66) {
                    animalImage.src = 'images/hungry_cat.gif';
                }
                else {
                    animalImage.src = 'images/happy_cat.gif';
                }
            } else {
                console.log("3")
                // If not checked, set the image src to the dog image
                if (healthValue <= 0) {
                    animalImage.src = 'images/death.gif';   
                }
                else if (healthValue < 33) {
                    animalImage.src = 'images/sad_dog.gif';
                }
                else if (healthValue < 66) {
                    animalImage.src = 'images/okay_dog.gif';
                }
                else {
                    animalImage.src = 'images/happy_dog.gif';
                }
            }
        }
        // Add event listener to toggle switch
        toggleSwitch.addEventListener('change', updateImage); 
        updateImage();
    }

});