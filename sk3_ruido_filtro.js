// Ruído -> filtro -> envelope -> saída.
// mouseX move a frequência de corte, segurar dispara repetições.

let ruido, filtro, env, fft;
let iniciado = false;
let ultimo = 0;
let corte = 1200;
let tipos = ['white', 'pink', 'brown'];
let atual = 0;
const BARRA = 44;
const FMAX = 6000;

function setup() {
  createCanvas(windowWidth, 340);
  textFont('monospace');

  ruido = new p5.Noise(tipos[atual]);
  filtro = new p5.Biquad(corte, 'lowpass');
  env = new p5.Envelope();
  env.setADSR(0.001, 0.09, 0.0, 0.14);
  fft = new p5.FFT(256);

  ruido.disconnect();
  ruido.connect(filtro);
  filtro.disconnect();
  filtro.connect(env);
  env.connect(fft);
}

function windowResized() {
  resizeCanvas(windowWidth, 340);
}

function draw() {
  background(17, 17, 19);

  corte = 100 * pow(FMAX / 100, constrain(mouseX / width, 0, 1));
  filtro.freq(corte);

  if (mouseIsPressed && mouseY > BARRA && millis() - ultimo > 230) {
    env.play();
    ultimo = millis();
  }

  desenhaEspectro();
  desenhaCorte();
  desenhaBarra();

  noStroke();
  fill(140);
  textSize(11);
  textAlign(LEFT, CENTER);
  text('corte  ' + nf(corte, 4, 0) + ' Hz', 14, height - 18);
  fill(90);
  textAlign(RIGHT, CENTER);
  text('segure para repetir', width - 14, height - 18);
}

function desenhaEspectro() {
  let espectro = fft.analyze();
  let nyq = getAudioContext().sampleRate / 2;
  let hz = nyq / espectro.length;
  let bins = min(espectro.length, ceil(FMAX / hz));
  let base = height - 36;
  let topo = BARRA + 16;

  noStroke();
  fill(200, 77, 10);
  for (let i = 0; i < bins; i++) {
    let x = map(i, 0, bins, 0, width);
    let h = map(espectro[i], 0, 0.25, 0, base - topo, true);
    rect(x, base - h, width / bins - 1, h);
  }
}

function desenhaCorte() {
  let x = map(corte, 0, FMAX, 0, width);
  stroke(90);
  strokeWeight(1);
  line(x, BARRA, x, height - 36);
  noStroke();
  fill(120);
  textSize(10);
  textAlign(LEFT, TOP);
  text('corte', x + 5, BARRA + 5);
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
    ruido.start();
    iniciado = true;
  }
  if (mouseY < BARRA) {
    atual = constrain(floor(mouseX / (width / tipos.length)), 0, tipos.length - 1);
    ruido.type(tipos[atual]);
  }
}
