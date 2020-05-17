const col_widths = ["25%", "25%", "25%", "25%"];

function search(){
    let searchTerm = $("#searchBox").val();
    let matches = [];
    for(let i = 0; i < leaderboard_data.length; i++){
        if(leaderboard_data[i][1].indexOf(searchTerm) != -1){
            matches.push(leaderboard_data[i]);
        }
    }
    set_table(matches, 0);
    return false;
}

function get_row(row_data){
    let divs = [];
    console.log(row_data);
    let row = $("<tr>").addClass("table-row");
    for(let i = 0; i < row_data.length; i++){
        let div = $("<th>").text( row_data[i] + "").css("width", col_widths[i]);
        row.append(div);
    }
    return row;
}

function set_search_options(data){
    $("#searchOptions").empty();
    for(let i = 0; i < data.length; i++){
        let option = $("<option>").val(data[i][1]);
        $("#searchOptions").append(option);
    }
}

function set_replay_table(data){
    console.log(data);
    let table = $("#table");
    table.empty();
    table.append(get_row(["Time", "Red", "Blue", "Result"]));
    for(let i = 0; i < data.length; i++){
        let arr = [data[i]['time'], data[i]['red'], data[i]['blue'], data[i]['outcome']];
        table.append(get_row(arr));
    }
}

window.onload = function(){
    set_replay_table(game_data);
};