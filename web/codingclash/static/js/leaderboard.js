const NUM_PER_BLOCK = 10;

// Assumes data is sorted
// Split data into blocks (a block is what is displayed per page)

function search(){
    let searchTerm = $("#searchBox").val();
    let matches = [];
    for(let i = 0; i < leaderboard_data.length; i++){
        if(leaderboard_data[i]['name'].indexOf(searchTerm) != -1){
            matches.push(leaderboard_data[i]);
        }
    }
    set_table(matches, 0);
    return false;
}

function set_buttons(data, block_num){
    let num_blocks = Math.ceil(data.length / NUM_PER_BLOCK);
    let button_div = $("#buttons");
    button_div.empty();
    for(let i = 0; i < num_blocks; i++){
        let button = $("<button>").text(i + "").addClass("btn").addClass("btn-primary").css("width", "40px");
        button.click(() => {set_leaderboard(i)});
        button_div.append(button);
    }
}

function get_row(rank, username, score){
    let rank_div = $("<th>").text(rank + "").css("width", "5%");
    let username_div = $("<th>").text(username).css("width", "75%");
    let score_div = $("<th>").text(score + "").css("width", "20%");
    let row = $("<tr>").addClass("table-row");
    row.append(rank_div).append(username_div).append(score_div);
    return row;
}

function set_table(blocks){
    console.log(blocks);
    let table = $("#table");
    table.empty();
    table.append(get_row("Rank", "Team name", "ELO rating"));
    for(let i = 0; i < blocks.length; i++){
        table.append(get_row(blocks[i]['rank'], blocks[i]['name'], blocks[i]['elo']));
    }
}

function display(data, block_num){
    let block = [];
    let min = block_num * NUM_PER_BLOCK;
    let max = (block_num + 1) * NUM_PER_BLOCK;
    for(let i = min; i < Math.min(data.length, max); i++){
        block.push(data[i]);
    }
    set_table(block);
}

function set_search_options(data){
    $("#searchOptions").empty();
    for(let i = 0; i < data.length; i++){
        let option = $("<option>").val(data[i]['name']);
        $("#searchOptions").append(option);
    }
}

function set_leaderboard(block_num){
    display(leaderboard_data, block_num);
    set_buttons(leaderboard_data, block_num);
    set_search_options(leaderboard_data);
}

window.onload = function(){
    set_leaderboard(0);
};