// Oscilador: frequência no eixo X, amplitude no eixo Y.
// A barra de cima troca a forma de onda.

let osc;
let iniciado = false;
let tocando = false;
let tipos = ['sine', 'triangle', 'sawtooth', 'square'];
let atual = 0;
const BARRA = 44;

function setup() {
  createCanvas(windowWidth, 340);
  textFont('monospace');
  osc = new p5.Oscillator(440, tipos[atual]);
  osc.amp(0);
}

function windowResized() {
  resizeCanvas(windowWidth, 340);
}

function draw() {
  background(17, 17, 19);

  let f = map(mouseX, 0, width, 80, 1200, true);
  let a = map(mouseY, height - 60, BARRA, 0, 0.7, true);

  if (tocando) {
    osc.freq(f, 0.05);
    osc.amp(a, 0.05);
  }

  desenhaOnda(f, tocando ? a : 0.12);
  desenhaBarra();

  noStroke();
  fill(140);
  textSize(11);
  textAlign(LEFT, CENTER);
  text('freq  ' + nf(f, 3, 1) + ' Hz', 14, height - 34);
  text('amp   ' + nf(a, 1, 2), 14, height - 16);

  fill(tocando ? color(200, 77, 10) : color(90));
  textAlign(RIGHT, CENTER);
  text(tocando ? 'tocando' : 'segure o mouse para tocar', width - 14, height - 25);
}

function desenhaOnda(f, a) {
  let ciclos = map(f, 80, 1200, 1.5, 14);
  let amp = map(a, 0, 0.7, 6, 92, true);
  let meio = (BARRA + height - 60) / 2;

  stroke(38);
  strokeWeight(1);
  line(0, meio, width, meio);

  stroke(200, 77, 10);
  strokeWeight(2);
  noFill();
  beginShape();
  for (let x = 0; x <= width; x++) {
    let t = (x / width) * ciclos;
    vertex(x, meio - amp * forma(tipos[atual], t));
  }
  endShape();
}

function forma(tipo, t) {
  let fase = t - floor(t);
  if (tipo === 'sine') return sin(TWO_PI * t);
  if (tipo === 'triangle') return 4 * abs(fase - 0.5) - 1;
  if (tipo === 'sawtooth') return 2 * fase - 1;
  return fase < 0.5 ? 1 : -1;
}

function desenhaBarra() {
  noStroke();
  fill(26);
  rect(0, 0, width, BARRA);
  let w = width / tipos.length;
  textAlign(CENTER, CENTER);
  textSize(11);
  for (let i = 0; i < tipos.length; i++) {
    fill(i === atual ? color(200, 77, 10) : color(38));
    rect(i * w + 5, 7, w - 10, BARRA - 14, 3);
    fill(i === atual ? 20 : 175);
    text(tipos[i], i * w + w / 2, BARRA / 2);
  }
}

function mousePressed() {
  if (!iniciado) {
    userStartAudio();
    osc.start();
    iniciado = true;
  }
  if (mouseY < BARRA) {
    atual = constrain(floor(mouseX / (width / tipos.length)), 0, tipos.length - 1);
    osc.setType(tipos[atual]);
    return;
  }
  tocando = true;
}

function mouseReleased() {
  osc.amp(0, 0.1);
  tocando = false;
}
