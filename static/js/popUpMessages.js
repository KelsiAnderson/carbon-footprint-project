const toastifyAlert = document.querySelector('#suggestion-pop-up');
console.log("THIS IS THE TOASTY ALERT", toastifyAlert)
toastifyAlert.addEventListener('click', (evt) => {
    console.log("HIIIII")
  Toastify({
    text: randomMessages(),
    duration: 5000,
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
    className: "info",
  }).showToast();
});

function randomMessages(){
  var phrases = ["Consider riding your bike today!","Check the weather and see if it's worth biking!",
    "Do you have enough time to take public transit?" ];
  var random=  Math.floor((Math.random() * phrases.length));
  var randomPhrase= phrases[random];
  console.log(randomPhrase);
  return randomPhrase;
}


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
