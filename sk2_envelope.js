// Envelope ADSR: o oscilador toca o tempo todo,
// quem abre e fecha o som é o envelope.

let osc, env;
let iniciado = false;
let segurando = false;
let arrastando = -1;

let params = [
  { nome: 'attack', v: 0.02, min: 0.001, max: 1.0 },
  { nome: 'decay', v: 0.12, min: 0.001, max: 1.0 },
  { nome: 'sustain', v: 0.35, min: 0.0, max: 1.0 },
  { nome: 'release', v: 0.6, min: 0.01, max: 2.0 }
];

const SY0 = 168;
const SDY = 28;
const ZONA = 46;

function setup() {
  createCanvas(windowWidth, 340);
  textFont('monospace');

  osc = new p5.Oscillator(220, 'sawtooth');
  env = new p5.Envelope();

  osc.disconnect();
  osc.connect(env);

  aplica();
}

function windowResized() {
  resizeCanvas(windowWidth, 340);
}

function aplica() {
  env.setADSR(params[0].v, params[1].v, params[2].v, params[3].v);
}

function sx() { return 84; }
function sw() { return max(80, width - 84 - 96); }

function draw() {
  background(17, 17, 19);
  desenhaCurva();
  desenhaSliders();
  desenhaZona();
}

function desenhaCurva() {
  let x0 = 24;
  let x1 = width - 24;
  let yBase = 132;
  let yTopo = 26;

  let a = params[0].v;
  let d = params[1].v;
  let s = params[2].v;
  let r = params[3].v;
  let sus = 0.4;
  let total = a + d + sus + r;

  let pts = [[0, 0], [a, 1], [a + d, s], [a + d + sus, s], [total, 0]];

  stroke(38);
  strokeWeight(1);
  line(x0, yBase, x1, yBase);

  stroke(200, 77, 10);
  strokeWeight(2);
  noFill();
  beginShape();
  for (let i = 0; i < pts.length; i++) {
    vertex(x0 + (pts[i][0] / total) * (x1 - x0), yBase - pts[i][1] * (yBase - yTopo));
  }
  endShape();

  noStroke();
  fill(110);
  textSize(10);
  textAlign(CENTER, TOP);
  let nomes = ['A', 'D', 'S', 'R'];
  let marcos = [a / 2, a + d / 2, a + d + sus / 2, a + d + sus + r / 2];
  for (let j = 0; j < 4; j++) {
    text(nomes[j], x0 + (marcos[j] / total) * (x1 - x0), yBase + 6);
  }
}

function desenhaSliders() {
  textSize(11);
  for (let i = 0; i < params.length; i++) {
    let y = SY0 + i * SDY;
    let t = (params[i].v - params[i].min) / (params[i].max - params[i].min);

    noStroke();
    fill(150);
    textAlign(RIGHT, CENTER);
    text(params[i].nome, sx() - 12, y);

    stroke(40);
    strokeWeight(3);
    line(sx(), y, sx() + sw(), y);
    stroke(200, 77, 10);
    line(sx(), y, sx() + t * sw(), y);

    noStroke();
    fill(200, 77, 10);
    circle(sx() + t * sw(), y, 11);

    fill(120);
    textAlign(LEFT, CENTER);
    text(nf(params[i].v, 1, 3), sx() + sw() + 14, y);
  }
}

function desenhaZona() {
  let y = height - ZONA;
  noStroke();
  fill(segurando ? color(200, 77, 10) : color(30));
  rect(0, y, width, ZONA);
  fill(segurando ? 20 : 165);
  textAlign(CENTER, CENTER);
  textSize(11);
  text(segurando ? 'soltar dispara o release' : 'segure aqui para disparar o envelope', width / 2, y + ZONA / 2);
}

function mousePressed() {
  for (let i = 0; i < params.length; i++) {
    let y = SY0 + i * SDY;
    if (mouseY > y - 13 && mouseY < y + 13 && mouseX > sx() - 24 && mouseX < sx() + sw() + 24) {
      arrastando = i;
      atualiza(i);
      return;
    }
  }
  if (mouseY > height - ZONA) {
    if (!iniciado) {
      userStartAudio();
      osc.start();
      iniciado = true;
    }
    env.triggerAttack();
    segurando = true;
  }
}

function mouseDragged() {
  if (arrastando >= 0) atualiza(arrastando);
}

function mouseReleased() {
  if (arrastando >= 0) {
    arrastando = -1;
    return;
  }
  if (segurando) {
    env.triggerRelease();
    segurando = false;
  }
}

function atualiza(i) {
  let t = constrain((mouseX - sx()) / sw(), 0, 1);
  params[i].v = params[i].min + t * (params[i].max - params[i].min);
  aplica();
}
