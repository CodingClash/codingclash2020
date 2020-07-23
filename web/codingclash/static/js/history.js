const col_widths = ["25%", "15%", "15%", "15%", "30%"];

function requestScrim(){
    let oppTeam = $("#oppName").text();
    let csrftoken = Cookies.get('csrftoken');
    let xhr = new XMLHttpRequest();
    xhr.open("POST", location.origin + "/game_request/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(JSON.stringify({
        "opponent": oppTeam
    }));
}

function search(){
    let searchTerm = $("#searchBox").val();
    let matches = [];
    let index = team_lowercase.indexOf(searchTerm.toLowerCase());
    if(index == -1){
        alert("Team " + searchTerm + " not found.");
        $("#playBlock").removeClass("d-block").addClass("d-none");
        return false;
    }
    for(let i = 0; i < game_data.length; i++){
        if(game_data[i]['red'] == searchTerm || game_data[i]['blue'] == searchTerm){
            matches.push(game_data[i]);
        }
    }
    set_replay_table(matches, 0);
    $("#oppName").text(team_list[index]);
    $("#playBlock").removeClass("d-none").addClass("d-block");
    return false;
}

function get_row(row_data){
    console.log(row_data);
    let row = $("<tr>").addClass("table-row");
    for(let i = 0; i < row_data.length; i++){
        let div = $("<th>").text( row_data[i] + "").css("width", col_widths[i]);
        row.append(div);
    }
    console.log(row);
    return row;
}

function set_search_options(data){
    $("#searchOptions").empty();
    for(let i = 0; i < data.length; i++){
        let option = $("<option>").val(data[i]);
        $("#searchOptions").append(option);
    }
}

function set_replay_table(data){
    console.log(data);
    let table = $("#table");
    table.empty();
    console.log("HI");
    table.append(get_row(["Time", "Red", "Blue", "Result", "Replay"]));
    console.log(data);
    for(let i = 0; i < data.length; i++){
        let arr = [data[i]['time'], data[i]['red'], data[i]['blue'], data[i]['outcome'], data[i]["replay"]];
        console.log(arr[4]);
        if(arr[4] == null){
            arr[4] = "";
        }
        table.append(get_row(arr));
    }
}

window.onload = function(){
    for (let i = 0; i < team_list.length; i++) {
        team_lowercase.push(team_list[i].toLowerCase());
    }
    set_replay_table(game_data);
    set_search_options(team_list);
};