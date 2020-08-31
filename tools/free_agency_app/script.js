fetch('https://dl.dropbox.com/s/tx5n31u0c7jmqg7/BBGM_League_136_2028_re_sign_players.json?dl=0')
  .then(function (response) {
        return response.json();
  })
  .then(function (data) {
        outputInfo(data);
  })
  .catch(function (err) {
        console.log(err);
  });
  
function outputInfo(data){
        var teamDiv = document.getElementById('teamDiv');
        var playerDiv = document.getElementById('playerDiv');
        
        var teams = data['teams'];
        var teamSel = document.createElement('select');
        teamSel.id = 'teamIn';
        teamSel.name = 'team';
        teamDiv.appendChild(teamSel);
        
        for (var i = 0; i < teams.length; i++){
                var sel = document.createElement('option');
                sel.innerHTML = teams[i]['region'] + ' ' + teams[i]['name'];
                sel.value = teams[i]['region'] + '_' + teams[i]['name'];
                teamSel.appendChild(sel);
        }
        
        var players = data['players'];
        var playerSel = document.createElement('select');
        playerSel.id = 'playerIn';
        playerSel.name = 'player';
        playerDiv.appendChild(playerSel);
        
        for (var i = 0; i < players.length; i++){
                var sel = document.createElement('option');
                if (players[i]['tid'] === -1){
                        sel.innerHTML = players[i]['firstName'] + ' ' + players[i]['lastName'];
                        sel.value = players[i]['firstName'] + '_' + players[i]['lastName'];
                        playerSel.appendChild(sel);
                }
        }
}

//document.getElementById('optIn').

document.querySelector("#faForm").addEventListener("submit", 
function(e)
{
e.preventDefault();    //stop form from submitting

var salIn = document.getElementById('salaryIn').value;
var yrsIn = document.getElementById('yearsIn').value;
var optIn = document.getElementById('optIn').value;
var optyrsIn = document.getElementById('optYearsIn').value;

if (isNaN(salIn)){
window.alert('Salary must be a number!');
} else if (salIn < 1){
window.alert('Minimum salary is $ 1M!');
} else if (optIn === 'None' && optyrsIn != 0){
window.alert('If option type is None, option years must be 0!');
} else if ((optIn === 'Team' || optIn === 'Player') && optyrsIn === '0'){
window.alert('Option years must be > 0!');
} else if (optyrsIn*1 + yrsIn*1 > 5){
window.alert('Maximum contract length is 5 years (guaranteed + option)');
} else{
google.script.run.addNewOffer(this);

window.alert('Thank you. Your offer has been recorded');

document.getElementById('salaryIn').value = '';
document.getElementById('yearsIn').value = '1';
document.getElementById('optYearsIn').value = '0';
document.getElementById('optIn').value = 'None';
}
}
);
