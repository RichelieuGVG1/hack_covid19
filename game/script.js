"use strict";

var audio = new Audio('music/fon.mp3');
var audio_shot = new Audio('music/shot.mp3');
var audio_reload = new Audio('music/reload.mp3');
var audio_warning = new Audio('music/warning.mp3');
var audio_win = new Audio('music/win.mp3');

let W, H;
let c, ctx;

let helico, btns;
let posX, posY;
let speed, speedX;

let virusImg, intervalVirus;
let virus = [];
let shoots = [];

let lost, kill, life;

let cptTime, intervalTime;



const init = () => {

	
	W = window.innerWidth;
	H = window.innerHeight;
	
	c = document.getElementById("canvas");
	c.width = W;
	c.height = H;
	ctx = c.getContext("2d");
	
	helico = document.getElementById('ufo');
	posY = W/2;
	speed = 0;
	speedX = 5;
	helico.style.top = posY + "px";
	
	virusImg = new Image();
	virusImg.src = "https://s8.hostingkartinok.com/uploads/images/2020/05/6bb0a74d8876c254b5d3e6d390d994f2.png";
	
	lost = 0;
	kill = 0;
	life = 100;
	
	cptTime = 180;
	intervalTime = setInterval(geTime, 1000);
	
	// phone
	btns = document.getElementsByClassName('btn');
	btns[0].addEventListener("touchstart", () => up() );
	btns[0].addEventListener("touchend", () => stop() );
	btns[1].addEventListener("touchstart", () => shoot() );
	btns[2].addEventListener("touchstart", () => down() );
	btns[2].addEventListener("touchend", () => stop() );
	

	
	//keyboard
	var mapKeyPress = {};
	let stateShoot = false;

	document.onkeydown = (e) => {

		e = e || window.event;
		mapKeyPress[e.keyCode] = true;
		if (e.keyCode == '83') down();/*83*/
		else if (e.keyCode == '87')  up();/*87*/
		else if(!stateShoot){
			shoot();
			stateShoot = true;
			audio_shot.autoplay = false;
			audio_shot.volume=0.35;
			audio_shot.play();
		}
	};
	document.onkeyup =(e) => {
		var i=0;
		e = e || window.event;
		mapKeyPress[e.keyCode] = false;
		if (mapKeyPress[83] == true) down();
		else if (mapKeyPress[87] == true)  up();
		else stop();
		stateShoot = false;
	};
	
	animate();

};
var audio = new Audio('music/fon.mp3');
audio.play();
audio.volume=0.2;
const random = (max=1, min=0) => Math.random() * (max - min) + min;
const clear = () => ctx.clearRect(0, 0, W, H);
const updateLost = () => document.getElementsByClassName('lost')[0].innerText = lost;
const updateKill = () => document.getElementsByClassName('kill')[0].innerText = kill;
const updateLife = () => document.getElementsByClassName('life')[0].innerText = life + "%";

const geTime = () => {
	cptTime--;

	if(cptTime==173){
		audio_reload.volume=0.6;
		audio_reload.play();

	}

	if(cptTime==175){
		audio.volume=0.2;
		audio.play();

	}
	
	document.getElementsByClassName('time')[0].innerText = cptTime;
};

const down = () => {
	speed = 2;
	helico.style.transform = "rotate(3deg)";
};

const up = () => {
	speed =-4;
	helico.style.transform = "rotate(-3deg)";
};

const stop = () => {
	speed = 0;
	helico.style.transform = "rotate(0)";
};

const shoot = () => shoots.push(new Shoot(100, posY+25));

const checkHelico = () => {
	if(posY>0){
		posY>H-105 && speed>=0 ? speed = 0:  posY += 1;
		posY += speed;
	}
	else posY += 1;
	if(posY>H-105) helico.style.transform = "rotate(0)";
	
	helico.style.top = posY + "px";
	helico.style.left = speedX + "px";
};

const checkVirus = () => {
	for(var i = virus.length - 1; i >= 0; i--){
		virus[i].update();
		if(virus[i].x<0){
			virus.splice(i, 1);
			lost++;
			updateLost();
		}
		else if(virus[i].x<100&&virus[i].y+30>posY&&virus[i].y<posY+50){
			virus.splice(i, 1);
			life -= 50;
			lost++;
			updateLife();
			updateLost();
			signalDead();
		}
	}
};

const checkShoot = () => {
	for(var i = shoots.length - 1; i >= 0; i--){
		shoots[i].update();
		if(shoots[i].x>W) shoots.splice(i, 1);
	}
};

const newVirus = () => virus.push(new Virus());

const end = () => {
	clearInterval(intervalTime);
	shoots = [];
	virus = [];
	speedX += 5;
	if(life>0&&speedX<=10){
		setTimeout(function() {
			audio.pause();

			audio_win.autoplay = false;
			audio_win.volume=0.5;
			audio_win.play();

			document.getElementById('finish').style.display = 'flex';
			document.getElementById('state').innerText = 'CONGRATULATIONS! YOU WIN!';
			document.getElementById('cptkill').innerText = kill + " KILLED";
			document.getElementById('cptlost').innerText = lost + " LOST";

			document.getElementById('ufo').style.display = 'none';
			}, 2000);
		
	}
	else if(life<=0){
		audio.pause();
		document.getElementById('finish').style.display = 'flex';
		document.getElementById('state').innerText = 'YOU LOOOOO0OSE IN ' + (180-cptTime) + " SECONDS. \nSTUPID BAG OF BONES!!";
		document.getElementById('cptkill').innerText = kill + " KILLED";
		document.getElementById('cptlost').innerText = lost + " LOST";

		document.getElementById('ufo').style.display = 'none';
	}
};

const checkLife = () =>  {
	if(life<=0) end();
};

const checkTimer = () =>  {
	if(cptTime<=0) end();
};

const start = () => {
	document.getElementById('beginning').style.display = 'none';
	document.getElementById('ufo').style.display = 'block';
	intervalVirus = setInterval(newVirus, 500);
};

const lose = () => {
	clearInterval(intervalTime);
	shoots = [];
	virus = [];
	document.getElementById('finish').style.display = 'flex';
};


const retry = () =>{
	lost = 0;
	kill = 0;
	life = 100;
	cptTime = 180;
	posY = W/2;
	speed = 0;
	speedX = 5;
	geTime();
	intervalTime = setInterval(geTime, 1000);
	updateLost();
	updateKill();
	updateLife();
	
	document.getElementById('finish').style.display = 'none';
	document.getElementById('ufo').style.display = 'block';
};

const signalDead = () => {
	audio_warning.autoplay = false;
	audio_warning.volume=0.5;
	audio_warning.play();

	for(var i=0; i<3; i++){
		canvas.style.backgroundColor = 'red';
		setTimeout(function() { 
			canvas.style.backgroundColor = "transparent";
		}, 100);
	}
	
};

const animate = () => {
	clear();
	checkVirus();
	checkShoot();
	checkHelico();
	checkLife();
	checkTimer();
	window.requestAnimationFrame(animate);
};

class Virus {
	constructor() {
		this.x = W + ~~random(30);
		this.y = ~~random(H-90, 70);
		this.speed = ~~random(3, 1);
	}
	draw() {
		ctx.beginPath();
		ctx.drawImage(virusImg, this.x, this.y, 30, 30);
	}
	update() {
		this.x -= this.speed;
		this.draw();
	}
}

class Shoot {
	constructor(x, y) {
		this.x = x;
		this.y = y;
		this.speed = 4;
	}
	draw() {


		ctx.beginPath();
		ctx.fillStyle = 'red';
		ctx.arc(this.x, this.y,  3, 0, Math.PI * 2, true);
		ctx.fill();

		
	}
	update() {
		for(let i = virus.length - 1; i >= 0; i--){
			if(this.x>virus[i].x&&this.x<virus[i].x+30&&this.y>virus[i].y&&this.y<virus[i].y+30){
				virus.splice(i, 1);
				kill++;
				updateKill();
				this.x = W + 100;
			}
		}
		this.x += this.speed;
		this.draw();
	}
}

window.onload = init;

