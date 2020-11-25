const toastifyAlert = document.querySelector('#log-in-existing-user');
console.log("THIS IS THE TOASTY ALERT", toastifyAlert)
toastifyAlert.addEventListener('click', (evt) => {
    console.log("HIIIII")
  Toastify({
    text: "Hi there! Thanks for being cautious of your emissions!",
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
    className: "info",
  }).showToast();
});


