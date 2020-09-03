function paint(json) {
    let Direction = json['Direction'];
    let X         = json['X'];
    let Y         = json['Y'];
    let ContSum   = json['ContSum'];
    let Area      = json['Area'];
    XY.value = 'X: '+X+' Y: '+Y+' сумма цифр: '+ContSum+' пройденая площадь: '+Area;
    ctx.clearRect(0,0,field_width, field_height);
    let selimg = img[Direction];
    let src    = selimg[numImg];
    let sX = Math.round(X/10);
    let sY = Math.round(Y/10);
    ctx.drawImage(src, sX, sY);
    numImg++;
    if (numImg>=selimg.length) numImg = 0;
    }

async function draw() {
    let response = await fetch('/status');
    if (response.ok) {
        let json = await response.json();
        paint(json);
        } else {
            alert("Ошибка HTTP: " + response.status);
            }
    window.requestAnimationFrame(draw);
    }

var img,numImg,XY,field,ctx,field_width,field_height;

function start() {
    XY = document.getElementById('XY');
    field = document.getElementById('field');
    field_width  = field.width;
    field_height = field.height;
    ctx   = field.getContext('2d');
    
    img = new Object();

    img.Up    = new Array();
    img.Up[0] = new Image();
    img.Up[0].src = '/static/img/antMove1Up.png';
    img.Up[1] = new Image();
    img.Up[1].src = '/static/img/antMove2Up.png';
    
    img.Down  = new Array();
    img.Down[0] = new Image();
    img.Down[0].src = '/static/img/antMove1Down.png';
    img.Down[1] = new Image();
    img.Down[1].src = '/static/img/antMove2Down.png';

    img.Left  = new Array();
    img.Left[0] = new Image();
    img.Left[0].src = '/static/img/antMove1Left.png';
    img.Left[1] = new Image();
    img.Left[1].src = '/static/img/antMove2Left.png';
    
    img.Right = new Array();
    img.Right[0] = new Image();
    img.Right[0].src = '/static/img/antMove1Right.png';
    img.Right[1] = new Image();
    img.Right[1].src = '/static/img/antMove2Right.png';

    numImg = 0;
    draw();
    }

window.onload = start;
