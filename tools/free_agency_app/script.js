fetch('https://raw.githubusercontent.com/ibfmultiplayer/bbgm/master/league_files/ibfExport.json')
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
		
		var teams = data['teams'].sort((a, b) => (a.region > b.region) ? 1 : -1);
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
		
		var players = data['players'].sort((a, b) => (a.lastName > b.lastName) ? 1 : (a.lastName === b.lastName) ? ((a.firstName > b.firstName) ? 1 : -1) : -1);
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
    
    document.querySelector("#faForm").addEventListener("submit", 
    function(e)
    {
    e.preventDefault();    //stop form from submitting
    
    var salIn = document.getElementById('salaryIn').value;
    var yrsIn = document.getElementById('yearsIn').value;
    var optIn = document.getElementById('optIn').value;
    var optYrs = (optIn === 'None') ? 0 : ((optIn === 'TO' || optIn === 'PO') ? 1 : 2);
    
    if (isNaN(salIn)){
       window.alert('Salary must be a number!');
    } else if (salIn < 1){
       window.alert('Minimum salary is $ 1M!');
    } else if (optYrs + yrsIn*1 > 5){
       window.alert('Maximum contract length is 5 years (guaranteed + option)');
    } else{
       google.script.run.addNewOffer(this);
       
       window.alert('Thank you. Your offer has been recorded');
    
       document.getElementById('salaryIn').value = '';
       document.getElementById('yearsIn').value = '1';
       document.getElementById('optIn').value = 'None';
    }
    }
    );