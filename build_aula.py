#!/usr/bin/env python3
# Monta a pagina de aula sobre sintese sonora no p5.js.
#
# Uso:
#   python3 build_aula.py                      -> usa o CSS de reserva deste arquivo
#   python3 build_aula.py aula07.html          -> le o bloco <style> de aula07.html
#                                                 verbatim, evitando deriva visual
import html
import os
import re
import sys

SAIDA = "/mnt/user-data/outputs/aula08.html"
DIR_SKETCHES = "/mnt/user-data/outputs/sketches"

P5 = "https://cdn.jsdelivr.net/npm/p5@2.3.1/lib/p5.min.js"
P5SOUND = "https://cdn.jsdelivr.net/npm/p5.sound@0.4.1/dist/p5.sound.min.js"

SKETCHES = [
    ("sk1", "01 · oscilador", "sk1_oscilador.js",
     "Frequencia no eixo horizontal, amplitude no vertical. A barra de cima troca a forma de onda sem interromper o som."),
    ("sk2", "02 · envelope", "sk2_envelope.js",
     "O oscilador nunca para: quem abre e fecha a passagem e o envelope. Arrastar os quatro controles muda o formato da nota."),
    ("sk3", "03 · ruido e filtro", "sk3_ruido_filtro.js",
     "Ruido branco, rosa ou marrom passando por um filtro passa-baixa e por um envelope curto. Segurar o mouse repete o disparo."),
    ("sk4", "04 · espectro", "sk4_fft.js",
     "A mesma nota nas quatro formas de onda, com a onda em cima e os harmonicos embaixo."),
]

CSS_RESERVA = """
:root{
  --tinta:#191714;
  --papel:#faf8f5;
  --papel-2:#f2ede6;
  --linha:#ddd5c9;
  --suave:#6f6759;
  --acento:#c84d0a;
  --acento-fraco:#f6e6d8;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  background:var(--papel);
  color:var(--tinta);
  font-family:"DM Sans",system-ui,sans-serif;
  font-size:17px;
  line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
.env{max-width:760px;margin:0 auto;padding:0 22px 120px}
a{color:var(--acento);text-decoration:none;border-bottom:1px solid var(--acento-fraco)}
a:hover{border-bottom-color:var(--acento)}
a:focus-visible,button:focus-visible{outline:2px solid var(--acento);outline-offset:2px}

.volta{font-family:"DM Mono",ui-monospace,monospace;font-size:13px;display:inline-block;margin:30px 0 0;border:0}
header.capa{padding:36px 0 8px;border-bottom:1px solid var(--linha)}
.curso{font-family:"DM Mono",ui-monospace,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--suave);margin:0 0 14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.n-aula{color:var(--acento);border-left:1px solid var(--linha);padding-left:10px}
h1{font-size:clamp(30px,6vw,46px);line-height:1.08;letter-spacing:-.02em;margin:0 0 12px;font-weight:500}
.sub{font-size:19px;color:var(--suave);margin:0 0 26px;max-width:52ch}
.ficha{display:flex;flex-wrap:wrap;gap:8px 26px;font-family:"DM Mono",ui-monospace,monospace;font-size:12.5px;color:var(--suave);margin:0 0 30px;padding:0;list-style:none}
.ficha b{font-weight:500;color:var(--tinta)}

.bloco{position:relative;padding:44px 0 6px;border-bottom:1px solid var(--linha)}
.marca{font-family:"DM Mono",ui-monospace,monospace;font-size:12px;letter-spacing:.1em;color:var(--acento);display:block;margin-bottom:8px}
h2{font-size:clamp(22px,4vw,29px);line-height:1.15;letter-spacing:-.01em;margin:0 0 18px;font-weight:500}
h3{font-size:18px;margin:30px 0 10px;font-weight:500}
p{margin:0 0 16px}
ul,ol{margin:0 0 18px;padding-left:20px}
li{margin-bottom:7px}
code{font-family:"DM Mono",ui-monospace,monospace;font-size:.88em;background:var(--papel-2);padding:1px 5px;border-radius:3px}
pre{background:#141416;color:#e8e4dd;padding:18px 20px;border-radius:6px;overflow-x:auto;font-size:13.5px;line-height:1.55;margin:0 0 20px}
pre code{background:none;color:inherit;padding:0;font-size:13.5px}

.caixa{border-left:3px solid var(--acento);background:var(--papel-2);padding:18px 22px;margin:24px 0;border-radius:0 5px 5px 0}
.caixa .rot{font-family:"DM Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--acento);display:block;margin-bottom:8px}
.caixa p:last-child,.caixa ul:last-child{margin-bottom:0}
.caixa.alerta{border-left-color:#8a7a55;background:#f5f0e2}
.caixa.alerta .rot{color:#7d6c45}

.sk{margin:26px 0 30px;border:1px solid var(--linha);border-radius:6px;overflow:hidden;background:#141416}
.sk-topo{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 12px;background:#1d1d20;border-bottom:1px solid #2a2a2e}
.sk-nome{font-family:"DM Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.09em;color:#a49b8c}
.sk-acoes{display:flex;gap:7px}
.sk-btn{font-family:"DM Mono",ui-monospace,monospace;font-size:11px;color:#cfc7ba;background:#2a2a2e;border:1px solid #38383d;border-radius:3px;padding:4px 10px;cursor:pointer}
.sk-btn:hover{background:var(--acento);border-color:var(--acento);color:#fff}
.sk-frame{display:block;width:100%;height:340px;border:0;background:#111113}
.sk-legenda{margin:0;padding:11px 14px;font-size:13.5px;color:#a49b8c;background:#1d1d20;border-top:1px solid #2a2a2e}
.sk-codigo{margin:0;border-top:1px solid #2a2a2e;border-radius:0;max-height:460px}
.sk-codigo[hidden]{display:none}

table{width:100%;border-collapse:collapse;font-size:14.5px;margin:0 0 22px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--linha);vertical-align:top}
th{font-family:"DM Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--suave);font-weight:400}
td code{white-space:nowrap}

footer.fim{padding:34px 0 0;font-size:14px;color:var(--suave)}
@media (max-width:560px){
  body{font-size:16px}
  .env{padding:0 16px 80px}
  pre{font-size:12.5px}
}
@media (prefers-reduced-motion:no-preference){
  .js .bloco{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
  .js .bloco.visivel{opacity:1;transform:none}
}
"""


def le_css_de_referencia(caminho):
    """Le o bloco <style> de uma aula existente, para nao ter deriva visual."""
    with open(caminho, "r", encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"<style>(.*?)</style>", src, re.S)
    if not m:
        raise SystemExit("nao achei um bloco <style> em " + caminho)
    return m.group(1)


def le_sketch(nome):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), nome),
              "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")


PAGINA_SKETCH = """<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="__P5__"></script>
<script src="__P5SOUND__"></script>
<style>html,body{margin:0;padding:0;background:#111113;overflow:hidden}canvas{display:block}</style>
</head><body><script>
__SKETCH__
</script></body></html>"""


def embed(ident, titulo, arquivo, legenda):
    codigo = le_sketch(arquivo)
    inner = (PAGINA_SKETCH
             .replace("__P5__", P5)
             .replace("__P5SOUND__", P5SOUND)
             .replace("__SKETCH__", codigo))
    srcdoc = html.escape(inner, quote=True)
    return """<figure class="sk">
  <div class="sk-topo">
    <span class="sk-nome">{titulo}</span>
    <div class="sk-acoes">
      <button class="sk-btn" type="button" data-codigo="{ident}">codigo</button>
      <button class="sk-btn" type="button" data-tela="{ident}">tela cheia</button>
    </div>
  </div>
  <iframe id="{ident}" class="sk-frame" title="{titulo}" allow="autoplay; fullscreen" allowfullscreen srcdoc="{srcdoc}"></iframe>
  <figcaption class="sk-legenda">{legenda}</figcaption>
  <pre class="sk-codigo" id="{ident}-codigo" hidden><code>{codigo}</code></pre>
</figure>""".format(ident=ident, titulo=html.escape(titulo), srcdoc=srcdoc,
                    legenda=html.escape(legenda), codigo=html.escape(codigo))


EMBEDS = {i[0]: embed(*i) for i in SKETCHES}

CORPO = """
<a class="volta" href="index.html">&larr; indice do curso</a>

<header class="capa">
  <p class="curso">IoT &middot; Interface Analogico-Digital <span class="n-aula">Aula 08 &middot; Audio</span></p>
  <h1>Sintese sonora no p5.js</h1>
  <p class="sub">Do primeiro oscilador ate o espectro na tela, sem instalar nada &mdash; tudo dentro do editor do p5.js.</p>
  <ul class="ficha">
    <li><b>formato</b> laboratorio, 3 h</li>
    <li><b>ferramentas</b> editor.p5js.org, p5.sound</li>
    <li><b>instalacao</b> nenhuma</li>
  </ul>
</header>

<section class="bloco">
  <span class="marca">00:00 &mdash; 00:15</span>
  <h2>Por onde o som entra</h2>
  <p>Ate aqui os sinais do curso vinham de sensores: uma tensao que sobe e desce e chega ao computador como numero. Som e a mesma historia contada mais rapido. Um alto-falante e um cone que empurra ar, e o navegador precisa saber, milhares de vezes por segundo, onde esse cone deve estar.</p>
  <p>Existem dois caminhos para chegar la. Um e tocar um arquivo gravado, que ja traz a lista de posicoes pronta. O outro e calcular essa lista na hora, a partir de parametros: uma frequencia, uma forma, uma amplitude. O segundo caminho e o que chamamos de sintese, e e o que interessa aqui, porque cada um desses parametros pode vir de um potenciometro, de um sensor de distancia, de uma mensagem MQTT.</p>
  <p>O som deixa de ser um arquivo que se toca e vira uma saida do sistema &mdash; do mesmo jeito que um LED ou um motor. E os numeros que ja circulam pelo projeto podem, sem nenhuma conversao especial, virar altura e timbre.</p>
  <div class="caixa">
    <span class="rot">Na bancada</span>
    <p>Antes de escrever qualquer linha, vale abrir o editor e deixar aberta tambem a referencia do p5.sound. Os dois links ficam lado a lado o resto da aula: <a href="https://editor.p5js.org" target="_blank" rel="noopener">editor.p5js.org</a> e <a href="https://p5js.org/reference/p5.sound/" target="_blank" rel="noopener">p5js.org/reference/p5.sound</a>.</p>
  </div>
</section>

<section class="bloco">
  <span class="marca">00:15 &mdash; 00:40</span>
  <h2>O editor e a biblioteca</h2>
  <p>O editor do p5.js roda inteiro no navegador. Um sketch novo ja vem com tres arquivos, e a barra lateral esquerda mostra os tres: <code>sketch.js</code>, onde fica o codigo; <code>index.html</code>, a pagina que carrega tudo; e <code>style.css</code>, que quase nao vamos tocar.</p>
  <p>O p5.js sozinho nao faz som. O que faz som e uma biblioteca separada, o p5.sound, e ela precisa ser carregada na pagina. Isso acontece em <code>index.html</code>, com uma linha logo depois da linha que carrega o p5:</p>
<pre><code>&lt;script src="https://cdn.jsdelivr.net/npm/p5@2.3.1/lib/p5.min.js"&gt;&lt;/script&gt;
&lt;script src="https://cdn.jsdelivr.net/npm/p5.sound@0.4.1/dist/p5.sound.min.js"&gt;&lt;/script&gt;</code></pre>
  <p>Se o sketch ja tiver uma linha de p5.sound, nao precisa de outra. A ordem importa: a biblioteca de som pendura as classes dela dentro do p5, entao o p5 tem que chegar primeiro.</p>

  <h3>O primeiro som</h3>
  <p>Com a biblioteca no lugar, cinco linhas em <code>sketch.js</code> ja produzem uma nota:</p>
<pre><code>let osc;

function setup() {
  createCanvas(400, 200);
  osc = new p5.Oscillator(440, 'sine');
}

function draw() {
  background(240);
  text('clique para tocar', 20, 30);
}

function mousePressed() {
  userStartAudio();
  osc.start();
  osc.amp(0.5, 0.1);
}</code></pre>
  <p>O clique nao esta ali por estilo. Todo navegador atual se recusa a produzir som antes de alguma acao da pessoa &mdash; e uma protecao contra paginas que tocam sozinhas. A funcao <code>userStartAudio()</code> destrava o audio, e ela so funciona se for chamada de dentro de um evento como <code>mousePressed()</code>. Um sketch que tenta tocar direto no <code>setup()</code> fica em silencio e nao acusa erro nenhum, o que costuma custar uns bons minutos de procura.</p>
  <div class="caixa">
    <span class="rot">Na bancada</span>
    <p>Cada um roda esse sketch e confirma que sai som. Quem estiver de fone descobre agora, e nao no meio do bloco seguinte, se o volume do sistema estava no zero.</p>
  </div>
  <div class="caixa alerta">
    <span class="rot">Onde costuma travar</span>
    <ul>
      <li>Tutoriais de dois ou tres anos atras usam <code>p5.MonoSynth</code>, <code>p5.PolySynth</code>, <code>p5.Filter</code> e <code>p5.SoundLoop</code>. A biblioteca foi reescrita em 2024 e essas classes viraram avisos no console &mdash; existem, mas nao fazem mais nada.</li>
      <li>No p5.js 2 nao existe mais <code>preload()</code>. Carregar um arquivo de audio agora e <code>async function setup()</code> com <code>await loadSound('som.mp3')</code>.</li>
    </ul>
  </div>
</section>

<section class="bloco">
  <span class="marca">00:40 &mdash; 01:10</span>
  <h2>Oscilador: frequencia, forma, amplitude</h2>
  <p>Um oscilador repete um desenho. A <b>frequencia</b> diz quantas vezes por segundo esse desenho se repete, e e ela que a gente escuta como altura: 440 Hz e o la que a orquestra usa para afinar, 880 Hz e o mesmo la uma oitava acima. A <b>forma de onda</b> e o desenho em si, e e ela que da o carater do som. A <b>amplitude</b> e o quanto o desenho se estica na vertical, ou seja, o volume.</p>
  <p>Os tres tem um metodo cada:</p>
<pre><code>osc.freq(440, 0.05);      // 440 Hz, chegando la em 0,05 s
osc.amp(0.5, 0.05);       // meia amplitude, com a mesma rampa
osc.setType('sawtooth');  // sine, triangle, sawtooth ou square</code></pre>
  <p>O segundo argumento e uma rampa em segundos, e vale a pena nunca omitir em mudancas de amplitude. Cortar o volume de uma vez cria um degrau na forma de onda, e degrau vira estalo. Uma rampa de cinquenta milisegundos ja resolve, e e curta demais para ser percebida como fade.</p>
  <p>No sketch abaixo, a posicao horizontal do mouse vira frequencia e a vertical vira amplitude. A diferenca entre as quatro formas fica clara logo no primeiro segundo: a senoide e oca, a quadrada e nasal, a dente de serra e a mais aspera das quatro.</p>
  __SK1__
  <div class="caixa">
    <span class="rot">Na bancada</span>
    <p>Uma variacao rapida: trocar o intervalo de <code>map()</code> de 80&ndash;1200 Hz para 80&ndash;120 Hz. Abaixo de uns 20 Hz o ouvido para de escutar altura e passa a escutar pulso &mdash; o mesmo oscilador vira um metronomo. E esse mesmo truque que transforma um oscilador em controle de outro parametro, o tal do LFO.</p>
  </div>
</section>

<section class="bloco">
  <span class="marca">01:20 &mdash; 01:50</span>
  <h2>Envelope: o formato de uma nota</h2>
  <p>O oscilador ligado direto soa como uma sirene: comeca e continua igual, sem comeco nem fim. Nenhum instrumento faz isso. Uma corda pincada tem um pico instantaneo e depois some. Um sopro demora um pouco para chegar ao volume e se mantem enquanto houver ar. Essa diferenca de contorno e boa parte do que a gente reconhece como <i>instrumento</i>.</p>
  <p>O envelope descreve esse contorno em quatro tempos, o famoso ADSR: <b>attack</b>, quanto demora do silencio ate o pico; <b>decay</b>, quanto demora do pico ate se acomodar; <b>sustain</b>, o nivel em que fica enquanto a nota e segurada; e <b>release</b>, quanto demora para sumir depois que solta.</p>
  <p>A ligacao muda um pouco em relacao ao que se via em versoes antigas. Todo objeto de som do p5.sound sai direto para a caixa assim que e criado, entao para colocar um envelope no meio do caminho e preciso primeiro tirar o oscilador da saida:</p>
<pre><code>osc = new p5.Oscillator(220, 'sawtooth');
env = new p5.Envelope();

osc.disconnect();   // tira o oscilador da saida
osc.connect(env);   // e faz ele passar por dentro do envelope

env.setADSR(0.02, 0.12, 0.35, 0.6);</code></pre>
  <p>O oscilador comeca e nunca mais para. Quem abre e fecha a passagem e o envelope, com <code>triggerAttack()</code> quando a tecla desce e <code>triggerRelease()</code> quando sobe. Existe tambem <code>play()</code>, que dispara e solta sozinho &mdash; util para percussao, onde nao ha nota segurada.</p>
  __SK2__
  <div class="caixa">
    <span class="rot">Na bancada</span>
    <p>Tres ajustes que valem ser escutados um atras do outro: attack em zero com release curto da percussao; attack longo com sustain alto da algo de orgao ou naipe de cordas; sustain em zero faz a nota morrer sozinha mesmo com o mouse ainda apertado, que e como um piano se comporta.</p>
  </div>
</section>

<section class="bloco">
  <span class="marca">01:50 &mdash; 02:20</span>
  <h2>Ruido e filtro</h2>
  <p>Ha uma segunda maneira de construir som, e ela funciona ao contrario. Em vez de somar coisas ate chegar no timbre desejado, comeca-se com um material que tem tudo dentro e vai-se tirando. E o metodo do escultor, e chama-se sintese subtrativa.</p>
  <p>O material bruto e o ruido, um sinal com todas as frequencias ao mesmo tempo. O p5.sound tem tres sabores: <code>white</code> distribui energia igual por todas as frequencias e soa como chiado de televisao fora do ar; <code>pink</code> tem mais grave e lembra chuva; <code>brown</code> tem ainda mais grave e soa como cachoeira distante.</p>
  <p>A ferramenta de retirar e o filtro. Um passa-baixa deixa passar o que esta abaixo de uma frequencia de corte e atenua o que esta acima. Movendo esse corte, o mesmo ruido percorre uma faixa enorme de timbres.</p>
<pre><code>ruido  = new p5.Noise('white');
filtro = new p5.Biquad(1200, 'lowpass');
env    = new p5.Envelope();
env.setADSR(0.001, 0.09, 0.0, 0.14);

ruido.disconnect();
ruido.connect(filtro);
filtro.disconnect();
filtro.connect(env);</code></pre>
  <p>Repare no padrao: cada objeto e desconectado da saida antes de ser ligado ao proximo, e so o ultimo da fila continua ligado na caixa. Trocar a ordem &mdash; conectar antes de desconectar &mdash; derruba a ligacao recem-criada, porque <code>disconnect()</code> corta tudo o que sai daquele objeto.</p>
  <p>Ruido com envelope curto e a receita de quase toda percussao eletronica. Corte alto da chimbal; corte baixo da bumbo abafado; no meio aparece caixa.</p>
  __SK3__
  <div class="caixa">
    <span class="rot">Na bancada</span>
    <p>Vale tentar chegar em tres sons de bateria so mexendo em duas coisas: a frequencia de corte e o tempo de decay. Depois disso, trocar <code>'lowpass'</code> por <code>'highpass'</code> ou <code>'bandpass'</code> no construtor do filtro muda completamente o resultado.</p>
  </div>
</section>

<section class="bloco">
  <span class="marca">02:20 &mdash; 02:45</span>
  <h2>Ver o que se escuta</h2>
  <p>A analise fecha o circuito. A FFT pega o sinal e devolve quanta energia existe em cada faixa de frequencia &mdash; e o que permite desenhar o som, e tambem o que permite usar o som como entrada de dados, do mesmo jeito que um sensor.</p>
  <p>Sao dois metodos com finalidades diferentes. <code>waveform()</code> devolve as amostras cruas, entre &minus;1 e 1, e desenha a onda no tempo. <code>analyze()</code> devolve as amplitudes por faixa de frequencia, entre 0 e 1, e desenha o espectro.</p>
<pre><code>fft = new p5.FFT(512);   // potencia de dois, entre 16 e 1024
osc.connect(fft);        // conectar a analise nao tira o som da caixa</code></pre>
  <p>Dois detalhes que mudaram na versao nova e costumam confundir quem segue material antigo: <code>analyze()</code> agora devolve valores de 0 a 1, e nao mais de 0 a 255, entao os <code>map()</code> de tutoriais antigos produzem barras invisiveis. E <code>connect()</code> soma uma ligacao em vez de substituir, entao ligar na FFT nao emudece nada.</p>
  <p>Comparar as quatro formas de onda no espectro explica de uma vez o que os ouvidos ja tinham dito. A senoide tem uma barra so. As outras tem uma serie de barras acima da fundamental, os harmonicos, e e a quantidade e o espacamento deles que produz a sensacao de brilho ou aspereza.</p>
  __SK4__
</section>

<section class="bloco">
  <span class="marca">02:45 &mdash; 03:00</span>
  <h2>Numeros que chegam de fora</h2>
  <p>Todo parametro visto hoje &mdash; frequencia, amplitude, corte do filtro, tempos do envelope &mdash; e simplesmente um numero. Nos exemplos ele veio do mouse, mas nada no p5.sound sabe disso nem se importa.</p>
  <p>O mesmo valor pode chegar de um sensor pela serial, ou de um topico MQTT, ou de uma mensagem OSC. A unica coisa que muda e a linha que produz o numero:</p>
<pre><code>// mouse
osc.freq(map(mouseX, 0, width, 100, 800), 0.05);

// sensor lido pela serial
osc.freq(map(leitura, 0, 4095, 100, 800), 0.05);

// valor recebido por MQTT
osc.freq(map(Number(mensagem), 0, 100, 100, 800), 0.05);</code></pre>
  <p>Vale reparar na rampa de <code>0.05</code> nos tres casos. Dados de sensor chegam com ruido e aos saltos; sem a rampa, cada leitura vira um degrau audivel. Com ela, a mesma sequencia de numeros soa como um movimento continuo. E o mesmo cuidado de suavizacao que ja aparecia ao desenhar leituras na tela, so que agora o erro nao e visual &mdash; e um estalo.</p>
  <div class="caixa">
    <span class="rot">Fica para depois da aula</span>
    <p>Um sketch com uma fonte de som, um filtro e um envelope, em que pelo menos um parametro seja controlado por algo que nao seja o mouse. Pode ser o teclado, pode ser o relogio do proprio sketch, pode ser um sensor pela serial &mdash; o que importa e o caminho do numero ate o parametro.</p>
  </div>
</section>

<section class="bloco">
  <span class="marca">referencia</span>
  <h2>O que foi usado hoje</h2>
  <table>
    <thead><tr><th>objeto</th><th>criacao</th><th>principais metodos</th></tr></thead>
    <tbody>
      <tr><td>oscilador</td><td><code>new p5.Oscillator(440, 'sine')</code></td><td><code>start()</code>, <code>stop()</code>, <code>freq(f, rampa)</code>, <code>amp(a, rampa)</code>, <code>setType(t)</code></td></tr>
      <tr><td>ruido</td><td><code>new p5.Noise('white')</code></td><td><code>start()</code>, <code>stop()</code>, <code>type(t)</code>, <code>amp(a, rampa)</code></td></tr>
      <tr><td>envelope</td><td><code>new p5.Envelope()</code></td><td><code>setADSR(a, d, s, r)</code>, <code>triggerAttack()</code>, <code>triggerRelease()</code>, <code>play()</code></td></tr>
      <tr><td>filtro</td><td><code>new p5.Biquad(1200, 'lowpass')</code></td><td><code>freq(f)</code>, <code>res(q)</code>, <code>setType(t)</code></td></tr>
      <tr><td>delay</td><td><code>new p5.Delay(0.25, 0.4)</code></td><td><code>delayTime(s)</code>, <code>feedback(f)</code>, <code>wet(v)</code></td></tr>
      <tr><td>reverb</td><td><code>new p5.Reverb(2)</code></td><td><code>set(decay)</code>, <code>wet(v)</code></td></tr>
      <tr><td>analise</td><td><code>new p5.FFT(512)</code></td><td><code>analyze()</code> 0&ndash;1, <code>waveform()</code> &minus;1&ndash;1</td></tr>
      <tr><td>nivel</td><td><code>new p5.Amplitude()</code></td><td><code>getLevel()</code>, <code>setInput(fonte)</code></td></tr>
      <tr><td>todos</td><td>&mdash;</td><td><code>connect(destino)</code>, <code>disconnect()</code>, <code>amp(v, rampa)</code></td></tr>
    </tbody>
  </table>
  <p>Referencia completa em <a href="https://p5js.org/reference/p5.sound/" target="_blank" rel="noopener">p5js.org/reference/p5.sound</a>. O codigo da biblioteca, com os exemplos oficiais, esta em <a href="https://github.com/processing/p5.sound.js" target="_blank" rel="noopener">github.com/processing/p5.sound.js</a>.</p>
</section>

<footer class="fim">
  <p>Aula 08 &mdash; Audio. IoT &middot; Interface Analogico-Digital.</p>
</footer>
"""

SCRIPT = """
document.documentElement.classList.add('js');

document.addEventListener('click', function (ev) {
  var alvoCodigo = ev.target.closest('[data-codigo]');
  if (alvoCodigo) {
    var bloco = document.getElementById(alvoCodigo.dataset.codigo + '-codigo');
    var aberto = !bloco.hidden;
    bloco.hidden = aberto;
    alvoCodigo.textContent = aberto ? 'codigo' : 'fechar';
    return;
  }
  var alvoTela = ev.target.closest('[data-tela]');
  if (alvoTela) {
    var quadro = document.getElementById(alvoTela.dataset.tela);
    if (quadro.requestFullscreen) { quadro.requestFullscreen(); }
    else if (quadro.webkitRequestFullscreen) { quadro.webkitRequestFullscreen(); }
  }
});

if ('IntersectionObserver' in window) {
  var observador = new IntersectionObserver(function (entradas) {
    for (var i = 0; i < entradas.length; i++) {
      if (entradas[i].isIntersecting) {
        entradas[i].target.classList.add('visivel');
        observador.unobserve(entradas[i].target);
      }
    }
  }, { rootMargin: '0px 0px -8% 0px' });
  var blocos = document.querySelectorAll('.bloco');
  for (var b = 0; b < blocos.length; b++) { observador.observe(blocos[b]); }
} else {
  var todos = document.querySelectorAll('.bloco');
  for (var t = 0; t < todos.length; t++) { todos[t].classList.add('visivel'); }
}
"""

MOLDE = """<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aula 08 &middot; Audio: sintese sonora no p5.js &middot; IoT: Interface Analogico-Digital</title>
<meta name="description" content="Introducao a sintese sonora no p5.js usando o editor online: oscilador, envelope, filtro e analise espectral, sem instalar nada.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<main class="env">
{corpo}
</main>
<script>{script}</script>
</body>
</html>
"""


def main():
    css = CSS_RESERVA
    if len(sys.argv) > 1:
        css = le_css_de_referencia(sys.argv[1])
        print("css lido de", sys.argv[1])

    corpo = CORPO
    for ident in EMBEDS:
        corpo = corpo.replace("__" + ident.upper() + "__", EMBEDS[ident])

    pagina = MOLDE.format(css=css, corpo=corpo, script=SCRIPT)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(pagina)

    os.makedirs(DIR_SKETCHES, exist_ok=True)
    for ident, titulo, arquivo, legenda in SKETCHES:
        destino = os.path.join(DIR_SKETCHES, arquivo)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(le_sketch(arquivo) + "\n")

    print("gerado:", SAIDA, os.path.getsize(SAIDA), "bytes")


if __name__ == "__main__":
    main()
