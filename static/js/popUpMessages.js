const toastifyAlert = document.querySelector('#suggestion-pop-up');
console.log("THIS IS THE TOASTY ALERT", toastifyAlert)
toastifyAlert.addEventListener('click', (evt) => {
    console.log("HIIIII")
  Toastify({
    text: randomMessages(),
    duration: 5000,
    backgroundColor: "#9a9df6",
    className: "info",
  }).showToast();
});


function randomMessages(){
  var phrases = ["Consider riding your bike today!","Check the weather and see if it's worth biking!",
    "Do you have enough time to take public transit?", "call a friend and carpool to work today!", "Have you asked your boss if you can work from home today?" ];
  var random=  Math.floor((Math.random() * phrases.length));
  var randomPhrase= phrases[random];
  console.log(randomPhrase);
  return randomPhrase;
}


