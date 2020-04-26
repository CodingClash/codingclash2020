const size = 40;
const board_size = 600;
const block_size = parseInt(board_size / size);
var boards = ["#" + "n" * size * size];
var board_num = 0;

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

function drawBoard(){
    let idx = 1;
    let board_string = boards[board_num];
    for(let r = 0; r < size; r++){
        for(let c = 0; c < size; c++){
            let filename = "images/" + getFilename(board_string[idx]);
            let block = $("#row-" + r + "_col-" + c);
            if(block.attr("src") != filename){
                block.attr("src", filename);
            }
            idx += 1;
        }
    }

}

function updateBoardNum(new_num){
    board_num = Math.max(Math.min(new_num, boards.length - 1), 0);
    drawBoard();
}

function uploadReplay(){
    var fileReader = new FileReader();
    fileReader.onload = function () {
      var data = fileReader.result;  // data <-- in this var you have the file data in Base64 format
      let content = data.split("\n");
      boards = content.slice(2);
      board_num = 0;
      drawBoard();
      console.log(boards.length);
    };
    fileReader.readAsText($('#myFile').prop('files')[0]);
}

function keydown(e){
    console.log(e.code);
    switch(e.code){
        case 'KeyA':
            updateBoardNum(board_num - 1);
            break;
        case 'KeyD':
            updateBoardNum(board_num + 1);
            break;
    }
}

//$("#myFile").on('change', function() {
//    console.log("WASSUP");
//});

window.onload = createEmptyBoard;

document.addEventListener('keydown', keydown);

//document.getElementById("file-input")

/*
drawBoard("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnGGnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnHnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnggnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnngnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnngnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnhnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn");
*/