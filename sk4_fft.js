// A mesma nota em quatro formas de onda.
// Em cima o desenho da onda, embaixo os harmônicos.

let osc, fft;
let iniciado = false;
let ligado = false;
let tipos = ['sine', 'triangle', 'sawtooth', 'square'];
let atual = 0;
const BARRA = 44;
const FMAX = 4000;

function setup() {
  createCanvas(windowWidth, 340);
  textFont('monospace');
  osc = new p5.Oscillator(220, tipos[atual]);
  osc.amp(0);
  fft = new p5.FFT(512);
  osc.connect(fft);
}

function windowResized() {
  resizeCanvas(windowWidth, 340);
}

function draw() {
  background(17, 17, 19);

  let f = map(mouseX, 0, width, 110, 660, true);
  if (ligado) osc.freq(f, 0.05);

  desenhaOnda();
  desenhaEspectro();
  desenhaBarra();

  noStroke();
  textSize(11);
  fill(140);
  textAlign(LEFT, CENTER);
  text('freq  ' + nf(f, 3, 1) + ' Hz', 14, height - 16);
  fill(ligado ? color(200, 77, 10) : color(90));
  textAlign(RIGHT, CENTER);
  text(ligado ? 'clique para parar' : 'clique para tocar', width - 14, height - 16);
}

function desenhaOnda() {
  let onda = fft.waveform();
  let topo = BARRA + 10;
  let base = 178;
  let meio = (topo + base) / 2;

  stroke(38);
  strokeWeight(1);
  line(0, meio, width, meio);

  stroke(200, 77, 10);
  strokeWeight(2);
  noFill();
  beginShape();
  for (let i = 0; i < onda.length; i++) {
    vertex(map(i, 0, onda.length, 0, width), meio + onda[i] * ((base - topo) / 2));
  }
  endShape();

  noStroke();
  fill(90);
  textSize(10);
  textAlign(LEFT, TOP);
  text('forma de onda', 14, topo);
}

function desenhaEspectro() {
  let espectro = fft.analyze();
  let nyq = getAudioContext().sampleRate / 2;
  let hz = nyq / espectro.length;
  let bins = min(espectro.length, ceil(FMAX / hz));
  let base = height - 30;
  let topo = 196;

  noStroke();
  fill(200, 77, 10);
  for (let i = 0; i < bins; i++) {
    let x = map(i, 0, bins, 0, width);
    let h = map(espectro[i], 0, 0.3, 0, base - topo, true);
    rect(x, base - h, max(1, width / bins - 1), h);
  }

  fill(90);
  textSize(10);
  textAlign(LEFT, TOP);
  text('espectro  0 - ' + FMAX + ' Hz', 14, topo);
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
  ligado = !ligado;
  osc.amp(ligado ? 0.5 : 0, 0.05);
}
