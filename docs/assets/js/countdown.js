(function countdown() {
  // Used dates
  let electionDate = new Date(2019, 9, 21);
  let currentDate = new Date();

  // Check if the current date is after election day
  if ((electionDate - currentDate) > 0) {
    let DAY_LENGTH = 24 * 60 * 60 * 1000;
    let e = document.querySelector('.countdown-days');

    let numDays = Math.round((electionDate - currentDate) / DAY_LENGTH);

    e.innerText = numDays + ' days until October 21, 2019';
  } else {
    // Uhh
  }
})();
