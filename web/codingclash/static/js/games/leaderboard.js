const leaderboard_data = [
    ["Bot 1", 100],
    ["Bot 2", 90],
    ["Bot 3", 80],
    ["Bot 4", 70],
    ["Bot 5", 60],
    ["Bot 6", 50],
    ["Bot 7", 40],
    ["Bot 8", 30],
    ["Bot 9", 20],
    ["Bot 10", 10],
    ["Bot 11", 0],
    ["Bot 12", -10],
    ["Bot 13", -20],
    ["Bot 14", -30],
    ["Bot 15", -40],
    ["Bot 16", -50],
    ["Bot 17", -60],
    ["Bot 18", -70],
    ["Bot 19", -80],
    ["Bot 20", -90],
];

const NUM_PER_BLOCK = 10;

// Assumes data is sorted
// Split data into blocks (a block is what is displayed per page)

function set_buttons(data, block_num){
    let num_blocks = Math.ceil(data.length / NUM_PER_BLOCK);
    let button_div = $("#buttons");
    button_div.empty();
    for(let i = 0; i < num_blocks; i++){
        let button = $("<button>").text(i + "").addClass("btn").addClass("btn-primary").css("width", "40px");
        button.click(() => {set_leaderboard(i)});
        button_div.append(button);
        console.log("HI");
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

function set_table(block, start_num){
    console.log(block);
    let table = $("#table");
    table.empty();
    table.append(get_row("Rank", "Team name", "ELO rating"));
    for(let i = 0; i < block.length; i++){
        table.append(get_row(start_num + i + 1, block[i][0], block[i][1]));
    }
}

function display(data, block_num){
    let block = [];
    let min = block_num * NUM_PER_BLOCK;
    let max = (block_num + 1) * NUM_PER_BLOCK;
    for(let i = min; i < Math.min(data.length, max); i++){
        block.push(data[i]);
    }
    set_table(block, min);
}

function set_leaderboard(block_num){
    display(leaderboard_data, block_num);
    set_buttons(leaderboard_data, block_num);
}

window.onload = function(){
    set_leaderboard(0);
};