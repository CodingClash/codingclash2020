const size = 40;
const board_size = 550;
const block_size = parseInt(board_size / size);

function createEmptyBoard(){
    for(let r = 0; r < size; r++){
        let row = $("<div></div>", {id: "row-" + r, style: "display: block; font-size: 0"})
        $("#gameboard").append(row);
        for(let c = 0; c < size; c++){
            let id = "row-" + r + "_col-" + c;
            let img = $("<img></img>", {id: id, src: "images/grass.png", width: block_size});
            $("#row-" + r).append(img);
        }
    }
}

function getFilename(char){
    switch(char){
        case "t":
            return "tank_b.png";
        case "g":
            return "gunner_b.png";
        case "h":
            return "hq_b.png";
        case "T":
            return "tank_r.png";
        case "G":
            return "gunner_r.png";
        case "H":
            return "hq_r.png";
        default:
            return "grass.png";
    }
}

function drawBoard(board_string){
    let idx = 0;
    console.log(board_string.length);
    for(let r = 0; r < size; r++){
        for(let c = 0; c < size; c++){
            let filename = "images/" + getFilename(board_string[idx]);
            $("#row-" + r + "_col-" + c).attr("src", filename);
            idx += 1;
        }
    }

}

window.onload = function(){
    createEmptyBoard();
}

/*
drawBoard("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnGGnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnHnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnggnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnngnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnngnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnhnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn");
*/