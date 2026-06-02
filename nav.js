const CURSO = {
  titulo: "IoT — Interface Analógico-Digital",
  professor: "André Damião",
  aulas: [
    {
      num: 1,
      titulo: "Introdução ao curso e ao Pure Data",
      arquivo: "aula01.html",
      disponivel: true,
    },
    {
      num: 2,
      titulo: "p5.js e uso consciente de IA",
      arquivo: "aula02.html",
      disponivel: true,
    },
    {
      num: 3,
      titulo: "Hardware e protocolos de comunicação",
      arquivo: "aula03.html",
      disponivel: true,
    },
    {
      num: 4,
      titulo: "Integração, sensores complexos e estética da interface",
      arquivo: "aula04.html",
      disponivel: false,
    },
    {
      num: 5,
      titulo: "App mobile — MobMuPlat e p5.js",
      arquivo: "aula05.html",
      disponivel: false,
    },
    {
      num: 6,
      titulo: "IoT — conceitos e plataformas",
      arquivo: "aula06.html",
      disponivel: false,
    },
    {
      num: 7,
      titulo: "IoT — integração com Pure Data e p5.js",
      arquivo: "aula07.html",
      disponivel: false,
    },
    {
      num: 8,
      titulo: "Seminários — apresentação dos projetos",
      arquivo: "aula08.html",
      disponivel: false,
    },
  ],
};

// ── detecta a aula atual pelo nome do arquivo ──────────────────────────────
function aulaAtual() {
  const arquivo = location.pathname.split("/").pop() || "index.html";
  return CURSO.aulas.find((a) => a.arquivo === arquivo) || null;
}

// ── injeta o header de navegação em todas as páginas de aula ──────────────
function injetarNav() {
  const atual = aulaAtual();
  if (!atual) return; // index.html não recebe o header de aula

  const anterior = CURSO.aulas.find((a) => a.num === atual.num - 1) || null;
  const proxima  = CURSO.aulas.find((a) => a.num === atual.num + 1) || null;

  const css = `
    <style id="nav-js-style">
      #curso-nav {
        position: sticky;
        top: 0;
        z-index: 100;
        background: rgba(248,247,244,.93);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #d8d4cc;
        padding: 0 48px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 52px;
        font-family: 'DM Mono', monospace;
        gap: 24px;
      }
      #curso-nav a {
        text-decoration: none;
        color: inherit;
      }
      .cnav-home {
        display: flex;
        flex-direction: column;
        gap: 1px;
        text-decoration: none !important;
        flex-shrink: 0;
      }
      .cnav-course {
        font-size: 10px;
        letter-spacing: .1em;
        text-transform: uppercase;
        color: #c84d0a;
        line-height: 1;
      }
      .cnav-author {
        font-size: 10px;
        color: #999990;
        line-height: 1;
      }
      .cnav-center {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;
        justify-content: center;
      }
      .cnav-dots {
        display: flex;
        gap: 5px;
        align-items: center;
      }
      .cnav-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #d8d4cc;
        text-decoration: none;
        transition: background .15s;
        flex-shrink: 0;
      }
      .cnav-dot.disponivel {
        background: #b8b4ac;
        cursor: pointer;
      }
      .cnav-dot.disponivel:hover {
        background: #888880;
      }
      .cnav-dot.atual {
        background: #e8651a;
        cursor: default;
      }
      .cnav-label {
        font-size: 10px;
        color: #999990;
        letter-spacing: .06em;
        white-space: nowrap;
      }
      .cnav-arrows {
        display: flex;
        gap: 2px;
        flex-shrink: 0;
      }
      .cnav-btn {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        padding: 6px 12px;
        border: 1px solid #d8d4cc;
        border-radius: 3px;
        background: none;
        color: #666660;
        cursor: pointer;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: border-color .15s, color .15s;
        white-space: nowrap;
      }
      .cnav-btn:hover {
        border-color: #b8b4ac;
        color: #18180f;
      }
      .cnav-btn.disabled {
        opacity: .25;
        cursor: default;
        pointer-events: none;
      }
      @media (max-width: 640px) {
        #curso-nav { padding: 0 16px; }
        .cnav-center { display: none; }
      }
    </style>
  `;

  const dotsHTML = CURSO.aulas.map((a) => {
    let cls = "cnav-dot";
    if (a.num === atual.num) cls += " atual";
    else if (a.disponivel) cls += " disponivel";
    const title = `Aula ${String(a.num).padStart(2,"0")} — ${a.titulo}`;
    if (a.disponivel && a.num !== atual.num) {
      return `<a class="${cls}" href="${a.arquivo}" title="${title}"></a>`;
    }
    return `<span class="${cls}" title="${title}"></span>`;
  }).join("");

  const btnAnterior = anterior
    ? `<a class="cnav-btn" href="${anterior.arquivo}">← Aula ${String(anterior.num).padStart(2,"0")}</a>`
    : `<span class="cnav-btn disabled">←</span>`;

  const btnProxima = proxima
    ? `<a class="cnav-btn" href="${proxima.arquivo}">Aula ${String(proxima.num).padStart(2,"0")} →</a>`
    : `<span class="cnav-btn disabled">→</span>`;

  const html = `
    ${css}
    <nav id="curso-nav">
      <a class="cnav-home" href="index.html">
        <span class="cnav-course">IoT</span>
        <span class="cnav-author">André Damião</span>
      </a>
      <div class="cnav-center">
        <span class="cnav-label">Aula ${String(atual.num).padStart(2,"0")} / ${CURSO.aulas.length}</span>
        <div class="cnav-dots">${dotsHTML}</div>
      </div>
      <div class="cnav-arrows">
        ${btnAnterior}
        ${btnProxima}
      </div>
    </nav>
  `;

  document.body.insertAdjacentHTML("afterbegin", html);
}

// ── atualiza o index.html: marca aulas disponíveis nos cards ───────────────
function sincronizarIndex() {
  const arquivo = location.pathname.split("/").pop() || "index.html";
  if (arquivo !== "index.html" && arquivo !== "") return;

  CURSO.aulas.forEach((aula) => {
    // tenta encontrar cards pelo href
    const link = document.querySelector(`a.aula-card[href="${aula.arquivo}"]`);
    if (link) return; // já está disponível no HTML

    if (aula.disponivel) {
      // procura um card locked com o mesmo texto de número e converte
      document.querySelectorAll(".aula-card.locked").forEach((card) => {
        const num = card.querySelector(".aula-num");
        if (num && num.textContent.trim() === `Aula ${String(aula.num).padStart(2,"0")}`) {
          card.classList.remove("locked");
          card.classList.add("available");
          card.setAttribute("href", aula.arquivo);
          card.outerHTML = card.outerHTML.replace(/^<div/, "<a").replace(/div>$/, "a>");
          const lock = card.querySelector(".aula-lock");
          if (lock) lock.textContent = "→";
        }
      });
    }
  });
}

// ── ponto de entrada ───────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  injetarNav();
  sincronizarIndex();
});
