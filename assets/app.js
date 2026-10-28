(function () {
  const S = window.SAMPLES;
  const $ = (id) => document.getElementById(id);
  let current = "Impressora offline";
  let ticket = null;
  let seq = 1040;

  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function select(k) {
    current = k;
    document.querySelectorAll(".shot").forEach((b) => b.classList.toggle("active", b.dataset.k === k));
  }
  document.querySelectorAll(".shot").forEach((b) =>
    b.addEventListener("click", () => {
      select(b.dataset.k);
      $("preview").hidden = true; $("dropText").hidden = false; $("note").hidden = true;
    })
  );

  // Palpite simples pelo nome do arquivo; sem IA no navegador.
  function guess(name) {
    const n = name.toLowerCase();
    if (/outlook|senha|mail|password|login/.test(n)) return "Outlook pedindo senha";
    if (/bsod|azul|blue|crash|irql|stop/.test(n)) return "Tela azul (BSOD)";
    return "Impressora offline";
  }
  function useFile(f) {
    if (!f || !f.type.startsWith("image/")) return;
    const img = $("preview");
    img.src = URL.createObjectURL(f); img.hidden = false; $("dropText").hidden = true;
    const k = guess(f.name);
    select(k);
    const note = $("note");
    note.hidden = false;
    note.textContent = "A análise com IA de verdade roda no app em Python, que manda a imagem para um modelo de visão. Aqui no site não há modelo nenhum, então vou mostrar o exemplo mais parecido: " + k + ".";
  }
  const drop = $("drop");
  $("file").addEventListener("change", (e) => useFile(e.target.files[0]));
  ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => useFile(e.dataTransfer.files[0]));

  function toMarkdown(t) {
    const passos = t.passos.map((p, i) => `${i + 1}. ${p}`).join("\n");
    return `## ${t.numero} · ${t.titulo}\n\n**Categoria:** ${t.categoria}  \n**Prioridade:** ${t.prioridade}  \n**Confiança da IA:** ${Math.round(t.confianca * 100)}%\n\n### Diagnóstico\n${t.diagnostico}\n\n### Passos para resolver\n${passos}\n\n### Quando escalar\n${t.quando_escalar}\n`;
  }

  function render(t) {
    const pct = Math.round(t.confianca * 100);
    $("ticket").innerHTML = `
      <div class="t-head"><span class="t-num">Chamado ${t.numero}</span><span class="pill">Aberto</span></div>
      <h3 class="t-title">${esc(t.titulo)}</h3>
      <div class="meta"><span class="pill">${esc(t.categoria)}</span><span class="pill p-${t.prioridade}">Prioridade ${esc(t.prioridade)}</span></div>
      <div class="blk"><h4>Diagnóstico</h4><p>${esc(t.diagnostico)}</p></div>
      <div class="blk"><h4>Passo a passo</h4><ol class="steps">${t.passos.map((p) => `<li>${esc(p)}</li>`).join("")}</ol></div>
      <div class="blk"><h4>Quando escalar</h4><p class="esc">${esc(t.quando_escalar)}</p></div>
      <div class="conf"><span>Confiança</span><div class="bar"><i style="width:0"></i></div><b>${pct}%</b></div>
      <div class="actions"><button class="btn small" id="copy">Copiar como Markdown</button><button class="btn small" id="dl">Baixar .md</button></div>`;
    $("ticket").hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => { $("ticket").querySelector(".bar i").style.width = pct + "%"; }));
    $("copy").onclick = async (e) => {
      try { await navigator.clipboard.writeText(toMarkdown(t)); e.target.textContent = "Copiado"; }
      catch { e.target.textContent = "Não foi possível copiar"; }
      setTimeout(() => (e.target.textContent = "Copiar como Markdown"), 1800);
    };
    $("dl").onclick = () => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([toMarkdown(t)], { type: "text/markdown" }));
      a.download = `chamado-${t.numero.replace("#", "")}.md`;
      a.click();
    };
  }

  function analyze(instant) {
    const go = $("go");
    ticket = Object.assign({ numero: "#" + new Date().getFullYear() + "-" + seq++ }, S[current]);
    $("empty").hidden = true; $("ticket").hidden = true;
    if (instant) return render(ticket);
    $("loading").hidden = false; go.disabled = true;
    const msgs = ["Lendo o print...", "Identificando o erro...", "Montando o chamado..."];
    let i = 0; $("loadMsg").textContent = msgs[0];
    const iv = setInterval(() => { $("loadMsg").textContent = msgs[++i % msgs.length]; }, 450);
    setTimeout(() => { clearInterval(iv); $("loading").hidden = true; go.disabled = false; render(ticket); }, 1400);
  }
  $("go").addEventListener("click", () => analyze(false));
  if (location.hash === "#preview") analyze(true);
})();
