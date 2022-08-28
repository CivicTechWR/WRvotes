(function countdown() {
  // Used dates
  //let electionDate = new Date('{{ site.election_date }}');
  let electionDate = new Date('2022-10-24T09:00');
  let currentDate = new Date();

  // Check if the current date is after election day
  let e = document.querySelector('.countdown-days');

  if ((electionDate - currentDate) > 0) {
    let DAY_LENGTH = 24 * 60 * 60 * 1000;

    let numDays = Math.round((electionDate - currentDate) / DAY_LENGTH);

    e.innerText = numDays + ' days until election day';
  } else if ((electionDate - currentDate) == 0) {
    e.innerText = 'Today is election day!';
  } else { 
    e.innerText = 'Election day has passed!' + electionDate;
    // Uhh
  }
})();
