var mousePressed = false;
var lastX, lastY;
var ctx;
var term;
var top_terms;
var top_index = 0;
var path;

function InitThis() {
    ctx = document.getElementById('symbol').getContext("2d");

    $('#symbol').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#symbol').on("touchstart", function(e){
        e.preventDefault();
        touchPressed = true;
        Draw(e.touches[0].pageX - $(this).offset().left, e.touches[0].pageY - $(this).offset().top, false);
    });

    $('#symbol').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#symbol').on('touchmove', function(e){
        e.preventDefault();
        if (touchPressed) {
            Draw(e.touches[0].pageX - $(this).offset().left, e.touches[0].pageY - $(this).offset().top, true);
        }
    })

    $('#symbol').mouseup(function (e) {
        mousePressed = false;
    });
	$('#symbol').mouseleave(function (e) {
        mousePressed = false;
    });

    $('#symbol').on("touchend", function (e) {
        console.log('end');
        e.preventDefault();
        touchPressed = false;
    });
	$('#symbol').on("touchcancel", function (e) {
        console.log('end');
        e.preventDefault();
        touchPressed = false;
    });
}

function Draw(x, y, isDown) {
    if (isDown) {
        //console.log('drawing: '+x+" "+y);
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.lineWidth = "7";
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}

function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function initPage(){
    clearArea();
    $("#content").text("");
    $('#question').css("display", "none");
    $('#init-buttons').css("display", "block");
    $('#select-term').css("display", "none");
}

function getImage() {
    $('#loading').css("display", "block");
    var canvas = document.getElementById("symbol");
    // change non-opaque pixels to white
    var imgData=ctx.getImageData(0,0,canvas.width,canvas.height);
    var data=imgData.data;

    for(var i = 0; i < data.length; i+=4){
        if(data[i+3]<255){
            data[i] = 255;
            data[i+1] = 255;
            data[i+2] = 255;
            data[i+3] = 255;
        }
    }

    ctx.putImageData(imgData,0,0);

    var imgToSend = canvas.toDataURL('image/jpeg');
    console.log(imgToSend)

    $.ajax({
        type: "POST",
        url: "..\\python\\process_image.py",
        data: {
            imgBase64: imgToSend
        },
        success: function(data){
            console.log(data);

            terms_raw = data.term;
            top_terms = terms_raw.split(',');
            term = top_terms[top_index]

            $('#sel-term').empty();
            data.termList.map(function(term){
                var option = $('<option></option>').attr("value", term).text(term);
                $('#sel-term').append(option)
            });

            path = data.path;
            $('#loading').css("display", "none");
            $("#content").text(term);
            $('#question').css("display", "block");
            $('#init-buttons').css("display", "none");
        }
    })
}

function correct(sel_term){
    if(sel_term){
        term = sel_term;
    }
    term = term.split('/')[0];
    console.log(term);
    to_send = [path, term];
    top_index = 0;
    $.ajax({
        type: "POST",
        url: "change_name.php",
        data: {
            data: to_send
        },
        success: function(data){
            console.log(data);
            initPage();
        }
    })
}

function fail(){
    if(top_index == 2){
        $('#question').css("display", "none");
        $('#select-term').css("display", "block");
        top_index = 0;
    }else {
        top_index++;
        term = top_terms[top_index]
        $("#content").text(term);
    }
    
}