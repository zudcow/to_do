document.addEventListener("DOMContentLoaded", function () {
        const completeButtons = document.querySelectorAll(".complete-button");

        completeButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                const taskForm = this.closest(".complete-task-form");
                const taskId = taskForm.getAttribute("data-task-id");

                // Send an AJAX request to toggle task completion status
                fetch(`/to_do/complete_task/${taskId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": "{{ csrf_token }}",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                })
                .then((response) => {
                    if (response.ok) {
                        // Toggle the button's appearance
                        button.classList.toggle("completed");
                    }
                })
                .catch((error) => {
                    console.error("Error toggling task completion status:", error);
                });
            });
        });
    });