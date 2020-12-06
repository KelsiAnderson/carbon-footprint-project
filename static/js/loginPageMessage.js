const loginAlert = document.querySelector('#log-in-existing-user');
console.log("LOOK AT MEEEE", loginAlert)
loginAlert.addEventListener('click', (evt) => {
    console.log("HIIIII")
  Toastify({
    text: "Hi there! Thanks for thinking about your emissions!",
    duration: 5000,
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
    className: "info",
  }).showToast();
});
