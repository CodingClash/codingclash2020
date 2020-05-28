const size = 40;
const board_size = 600;
const block_size = parseInt(board_size / size);
var boards = [];
var dlogs = [];
var bchain = [];
var info = [];
var selected = "";
var selectedID = "";
var board_num = 0;
var playing = false;
var playInterval;
var speed = 2;
var t = 0;
var g = 0;
var h = 0;
var T = 0;
var G = 0;
var H = 0;
var blue = "";
var red = "";
var winner = "";

function createEmptyBoard(){
    for(let r = 0; r < size; r++){
        let row = $("<div></div>", {id: "row-" + r, style: "display: block; font-size: 0"})
        $("#gameboard").append(row);
        for(let c = 0; c < size; c++){
            let id = "row-" + r + "_col-" + c;
            let img = $("<img></img>", {id: id, src: "/static/img/images/grass.png", width: block_size});
            img.click(handleClick);
            $("#row-" + r).append(img);
        }
    }
}

function handleClick(e){
    selected = e.target.id;
    // console.log("--------------------------")
    // console.log(document.getElementById(selected).src);
    // console.log(selected);
    // console.log(board_num);
    // console.log(info[board_num]);
    updateInfo("loc");
}

function updateInfo(updateType){
    if(updateType == "loc" && info[board_num][selected]){
        let temp = info[board_num][selected].split(" ");
        let info_arr = ["Robot ID: " + temp[1].slice(1, temp[1].length - 1),
                        "X Location: " + temp[3],
                        "Y Location: " + temp[2],
                        "Health: " + temp[4]]
        selectedID = temp[1].slice(1, temp[1].length - 1)
        document.getElementById("robotinfo").innerHTML = info_arr.join("<br>");
    }
    else if(updateType == "ID" && info[board_num][selectedID]){
        let temp = info[board_num][selectedID].split(" ");
        let info_arr = ["Robot ID: " + temp[1].slice(1, temp[1].length - 1),
                        "X Location: " + temp[3],
                        "Y Location: " + temp[2],
                        "Health: " + temp[4]]
        document.getElementById("robotinfo").innerHTML = info_arr.join("<br>");
    }
    else {
        document.getElementById("robotinfo").innerHTML = "";
    }
}


function getFilename(char){
    switch(char){
        case "t":
            t = t + 1;
            return "tank_b.png";
        case "g":
            g = g + 1;
            return "gunner_b.png";
        case "h":
            h = h + 1;
            return "hq_b.png";
        case "T":
            T = T + 1;
            return "tank_r.png";
        case "G":
            G = G + 1;
            return "gunner_r.png";
        case "H":
            H = H + 1;
            return "hq_r.png";
        default:
            return "grass.png";
    }
}
function drawBoard(){
    t = g = h = T = G = H = 0;
    let idx = 1;
    let board_string = boards[board_num];
    for(let r = 0; r < size; r++){
        for(let c = 0; c < size; c++){
            let filename = "/static/img/images/" + getFilename(board_string[idx]);
            let block = $("#row-" + r + "_col-" + c);
            if(block.attr("src") != filename){
                block.attr("src", filename);
            }
            idx += 1;
        }
    }
}

function updateScrollD(){
    var element = document.getElementById("Debug");
    element.scrollTop = element.scrollHeight;
}

function updateScrollB(){
    var element = document.getElementById("Blockchain");
    element.scrollTop = element.scrollHeight;
}

function updateBoardNum(new_num){
    board_num = Math.max(Math.min(new_num, boards.length - 1), 0);
    document.getElementById("roundRange").value = board_num;
    document.getElementById("roundNum").innerHTML = (board_num + 1) + " / " + boards.length;
    drawBoard();
    updateDlog(board_num);
    updateBchain(board_num);
    updateInfo("ID");
    updatePieceNum();
    updateWinner(board_num);
}

function updateWinner(board_num){
    gameboard = document.getElementById("gameboard");
    if (board_num==boards.length-1){
        if(winner.localeCompare(red)==0){
            gameboard.style.padding = "0px"
            gameboard.style.border = "5px solid red"
        }
        else if(winner.localeCompare(blue)==0){
            gameboard.style.padding = "0px"
            gameboard.style.border = "5px solid blue"
        }
    }
    else{
        gameboard.style.padding = "5px"
        gameboard.style.border = "0px"
    }
}

function openTab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function updatePieceNum(){
    document.getElementById("pieceNumt").innerHTML = t;
    document.getElementById("pieceNumT").innerHTML = T;
    document.getElementById("pieceNumg").innerHTML = g;
    document.getElementById("pieceNumG").innerHTML = G;
}

function updateDlog(board_num){
    var outlist = [];
    for (let i = 0; i < board_num + 1; i++){
        outlist = outlist.concat(dlogs[i]);
    }
    document.getElementById("dlogs").innerHTML = outlist.join("<br>");
    updateScrollD();
}

function updateBchain(board_num){
    var outlist = [];
    for (let i = 0; i < board_num + 1; i++){
        if(bchain[i].length!=0 && !bchain[i][0].startsWith("X")){
            outlist = outlist.concat(bchain[i]);
        }
        
    }
    document.getElementById("bchain").innerHTML = outlist.join("<br>");
    updateScrollB();
}

function speedToSeconds(speed){
    return 1000 / speed;
}

function updateSpeed(new_speed){
    speed = new_speed;
    document.getElementById("speedNum").innerHTML = speed;
    if(playing){
        clearInterval(playInterval);
        playInterval = setInterval(function(){
            updateBoardNum(board_num + 1);
        }, speedToSeconds(speed));
    }
}

function togglePlay(){
    playing = !playing;
    let btn = document.getElementById("play");
    if(playing){
        btn.innerHTML = "Pause";
        playInterval = setInterval(function(){
            updateBoardNum(board_num + 1);
        }, speedToSeconds(speed));
    } else{
        btn.innerHTML = "Play";
        clearInterval(playInterval);
    }
}

function uploadReplay(){
    var fileReader = new FileReader();
    fileReader.onload = function () {
        var data = fileReader.result;
        let content = data.split("\n");
        boards = [];
        dlogs = [];
        info = [];
        bchain = [];
        let roundNum = -1;
        for (index = 0; index < content.length; index++) { 
            if (content[index].startsWith("#")){
                boards.push(content[index]);
                dlogs.push([]);
                bchain.push([]);
                info.push({});
                roundNum += 1;
            }
            else if (content[index].startsWith("[DLOG]")){
                dlogs[roundNum].push(content[index]);
            }
            else if (content[index].startsWith("[BCHAIN]")){
                if (content[index].trim().length=="[BCHAIN]".length){
                    bchain[roundNum].push("X"+roundNum.toString()+" "+content[index]);
                }
                else{
                    bchain[roundNum].push(roundNum.toString()+" "+content[index]);
                }
                
            }
            else if (content[index].startsWith("|")){
                if (content[index].startsWith("|blue: ")){
                    blue = content[index].replace("|blue: ", "").trim();
                }
                else if (content[index].startsWith("|red: ")){
                    red = content[index].replace("|red: ", "").trim();
                }
                else if (content[index].startsWith("|Winner: ")){
                    winner = content[index].replace("|Winner: ", "").trim();
                }
            }
            else if (content[index].startsWith("[INFO]")){
                let temp = content[index].split(" ");
                let id = temp[1].slice(1, temp[1].length - 1);
                let row = temp[2];
                let col = temp[3];
                info[roundNum]["row-" + row + "_col-" + col] = content[index];
                info[roundNum][id] = content[index];
            }
            else{
                console.log("Unknown line: " + content[index]);
            }
        }
        board_num = 0;
        document.getElementById("roundRange").max = boards.length - 1;
        updateBoardNum(0);
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

window.onload = function (){
    document.getElementById("roundNum").innerHTML = "1 / 1";
    document.getElementById("speedNum").innerHTML = "1";
    createEmptyBoard();
};

document.addEventListener('keydown', keydown);
