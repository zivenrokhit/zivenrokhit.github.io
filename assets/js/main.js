var hamburger = $('#hamburger-icon');
var nav = $('nav');
var isOn = true;

hamburger.click(function () {
  nav.toggle();
  hamburger.toggleClass('active');
  return false;
});

function closer() {
  nav.toggle();
  hamburger.toggleClass('active');
  openNav();
}

/* Open when someone clicks on the span element */
function openNav() {
  if (isOn) {
    document.getElementById("myNav").style.height = "100%";
    $(".line").css("background", "white");
    isOn = false;
  } else {
    document.getElementById("myNav").style.height = "0%";
    $(".line").css("background", "black");
    isOn = true;
  }
}