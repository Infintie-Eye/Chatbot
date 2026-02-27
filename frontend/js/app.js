/**
 * Conrux AI — Elite JavaScript Application
 * Handles: Geometric canvas, particles, chat pipeline, image/doc analysis, toasts
 */

'use strict';

// ══════════════════════════════════════════════════════
//  CONFIGURATION
// ══════════════════════════════════════════════════════
const CONFIG = {
  API_BASE:       'http://localhost:8000/api/v1',
  TYPING_DELAY:   400,     // ms before showing typing indicator
  TOAST_DURATION: 4000,    // ms
};

// ══════════════════════════════════════════════════════
//  STATE
// ══════════════════════════════════════════════════════
const state = {
  sessionId:      null,
  isProcessing:   false,
  imageFile:      null,
  docFile:        null,
};

// ══════════════════════════════════════════════════════
//  GEOMETRIC BACKGROUND CANVAS
//  Art-Deco gold patterns drawn on a canvas
// ══════════════════════════════════════════════════════
(function initCanvas() {
  const canvas = document.getElementById('geo-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', () => { resize(); draw(); });

  const GOLD_A = 'rgba(201,162,39,0.07)';
  const GOLD_B = 'rgba(201,162,39,0.04)';
  const GOLD_C = 'rgba(255,215,0,0.03)';

  function polygon(cx, cy, r, sides, rotation = 0) {
    ctx.beginPath();
    for (let i = 0; i < sides; i++) {
      const angle = (Math.PI * 2 / sides) * i + rotation;
      const x = cx + r * Math.cos(angle);
      const y = cy + r * Math.sin(angle);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
  }

  function drawDiamondCluster(cx, cy, maxR, steps, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 0.5;
    for (let i = steps; i > 0; i--) {
      const r = (maxR / steps) * i;
      polygon(cx, cy, r, 4, Math.PI / 4);
      ctx.stroke();
    }
    // cross lines
    ctx.globalAlpha = 0.4;
    ctx.beginPath();
    ctx.moveTo(cx - maxR, cy); ctx.lineTo(cx + maxR, cy);
    ctx.moveTo(cx, cy - maxR); ctx.lineTo(cx, cy + maxR);
    ctx.stroke();
    ctx.globalAlpha = 1;
  }

  function drawHexGrid(offsetX, offsetY, cellSize, cols, rows, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 0.3;
    const h = cellSize * Math.sqrt(3) / 2;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const x = offsetX + col * cellSize * 1.5;
        const y = offsetY + row * h * 2 + (col % 2 === 0 ? 0 : h);
        polygon(x, y, cellSize * 0.9, 6, Math.PI / 6);
        ctx.stroke();
      }
    }
  }

  function drawArtDecoCorner(x, y, size, flipX, flipY) {
    const sx = flipX ? -1 : 1;
    const sy = flipY ? -1 : 1;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(sx, sy);
    ctx.strokeStyle = 'rgba(201,162,39,0.12)';
    ctx.lineWidth = 0.6;
    // Fan lines
    for (let i = 0; i <= 5; i++) {
      const angle = (Math.PI / 2 / 5) * i;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(size * Math.cos(angle), size * Math.sin(angle));
      ctx.stroke();
    }
    // Concentric arcs
    for (let r = size * 0.3; r <= size; r += size * 0.17) {
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI / 2);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawGrid(color) {
    const W = canvas.width;
    const H = canvas.height;
    const spacing = 80;
    ctx.strokeStyle = color;
    ctx.lineWidth = 0.3;
    for (let x = 0; x <= W; x += spacing) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y <= H; y += spacing) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const W = canvas.width;
    const H = canvas.height;

    // Subtle full grid
    drawGrid('rgba(201,162,39,0.025)');

    // Hex grids
    drawHexGrid(-30, H * 0.35, 45, 4, 5, GOLD_B);
    drawHexGrid(W - 230, -20, 40, 5, 4, GOLD_B);

    // Diamond clusters
    drawDiamondCluster(W * 0.15, H * 0.1, 120, 5, GOLD_A);
    drawDiamondCluster(W * 0.85, H * 0.08, 100, 4, GOLD_A);
    drawDiamondCluster(W * 0.1,  H * 0.7,  80,  3, GOLD_B);
    drawDiamondCluster(W * 0.9,  H * 0.75, 90,  4, GOLD_B);
    drawDiamondCluster(W * 0.5,  H * 0.15, 60,  3, GOLD_C);

    // Art-deco fan corners
    drawArtDecoCorner(0,  0,  200, false, false);
    drawArtDecoCorner(W,  0,  200, true,  false);
    drawArtDecoCorner(0,  H,  200, false, true);
    drawArtDecoCorner(W,  H,  200, true,  true);

    // Large outer diamond frame
    ctx.strokeStyle = 'rgba(201,162,39,0.04)';
    ctx.lineWidth = 1;
    polygon(W / 2, H / 2, Math.min(W, H) * 0.48, 4, Math.PI / 4);
    ctx.stroke();
    polygon(W / 2, H / 2, Math.min(W, H) * 0.42, 4, Math.PI / 4);
    ctx.stroke();
  }

  draw();
})();

// ══════════════════════════════════════════════════════
//  FLOATING PARTICLES
// ══════════════════════════════════════════════════════
(function initParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  const COUNT = 40;
  for (let i = 0; i < COUNT; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.left  = Math.random() * 100 + 'vw';
    p.style.top   = (30 + Math.random() * 70) + 'vh';
    p.style.setProperty('--dur',   (6 + Math.random() * 10) + 's');
    p.style.setProperty('--delay', (Math.random() * 8) + 's');
    p.style.width  = (1 + Math.random() * 2.5) + 'px';
    p.style.height = p.style.width;
    p.style.opacity = (0.2 + Math.random() * 0.5).toString();
    container.appendChild(p);
  }
})();

// ══════════════════════════════════════════════════════
//  TOAST NOTIFICATIONS
// ══════════════════════════════════════════════════════
function toast(message, type = 'info', duration = CONFIG.TOAST_DURATION) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  const icons = {
    info:    '✦',
    success: '✔',
    error:   '✖',
    warning: '⚠',
  };
  el.innerHTML = `<span style="color:var(--gold-primary)">${icons[type] || '✦'}</span> ${message}`;
  container.appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toast-out 0.3s ease forwards';
    setTimeout(() => el.remove(), 300);
  }, duration);
}

// ══════════════════════════════════════════════════════
//  API HELPERS
// ══════════════════════════════════════════════════════
async function apiPost(endpoint, body, isFormData = false) {
  const options = {
    method: 'POST',
    body: isFormData ? body : JSON.stringify(body),
  };
  if (!isFormData) {
    options.headers = { 'Content-Type': 'application/json' };
  }
  const res = await fetch(CONFIG.API_BASE + endpoint, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(err.error || err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

async function apiGet(endpoint) {
  const res = await fetch(CONFIG.API_BASE + endpoint);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ══════════════════════════════════════════════════════
//  STATUS / HEALTH CHECK
// ══════════════════════════════════════════════════════
async function checkHealth() {
  const dot  = document.getElementById('status-dot');
  const text = document.getElementById('status-text');
  try {
    const data = await apiGet('/health');
    if (data.success) {
      dot.className  = 'status-dot online';
      text.textContent = 'Online';
      const sessions = data.data?.active_sessions ?? 0;
      const statEl   = document.getElementById('stat-sessions');
      if (statEl) statEl.textContent = sessions;
    }
  } catch {
    dot.className  = 'status-dot offline';
    text.textContent = 'Offline';
  }
}

// ══════════════════════════════════════════════════════
//  SESSION MANAGEMENT
// ══════════════════════════════════════════════════════
async function createSession() {
  try {
    const data = await apiPost('/chat/session', {});
    state.sessionId = data.data?.session_id;
    const el = document.getElementById('session-id-display');
    if (el && state.sessionId) {
      el.textContent = `Session: ${state.sessionId.slice(0, 8)}…`;
    }
  } catch (e) {
    // Use a client-generated ID as fallback
    state.sessionId = crypto.randomUUID?.() || Date.now().toString(36);
    const el = document.getElementById('session-id-display');
    if (el) el.textContent = `Session: ${state.sessionId.slice(0, 8)}… (local)`;
  }
}

// ══════════════════════════════════════════════════════
//  MARKDOWN RENDERER (lightweight)
// ══════════════════════════════════════════════════════
function renderMarkdown(text) {
  return text
    // Code blocks
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
    .replace(/^# (.+)$/gm,   '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Blockquote
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // Unordered lists
    .replace(/^\s*[-•] (.+)$/gm, '<li>$1</li>')
    // Numbered lists
    .replace(/^\s*\d+\. (.+)$/gm, '<li>$1</li>')
    // Line breaks
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');
}

// ══════════════════════════════════════════════════════
//  CHAT
// ══════════════════════════════════════════════════════
const messagesArea  = document.getElementById('messages-area');
const chatInput     = document.getElementById('chat-input');
const sendBtn       = document.getElementById('send-btn');
const charCount     = document.getElementById('char-count');
const welcomeMsg    = document.getElementById('welcome-msg');

function appendMessage(role, content, meta = '') {
  // Hide welcome on first message
  if (welcomeMsg && !welcomeMsg.classList.contains('hidden')) {
    welcomeMsg.classList.add('hidden');
  }

  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  // Avatar SVG
  const avatar = document.createElement('div');
  avatar.className = `msg-avatar ${role === 'assistant' ? 'ai-avatar' : 'user-avatar'}`;
  avatar.innerHTML = role === 'assistant'
    ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polygon points="12,2 22,7 22,17 12,22 2,17 2,7" fill="none" stroke="#C9A227" stroke-width="1.5"/><circle cx="12" cy="12" r="3" fill="#C9A227" opacity="0.5"/></svg>`
    : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="#3D9B6A" stroke-width="1.5" fill="none"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#3D9B6A" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>`;

  const bubble = document.createElement('div');
  bubble.className = `msg-bubble ${role === 'assistant' ? 'ai' : 'user'}`;
  bubble.innerHTML = `<p>${renderMarkdown(content)}</p>`;

  if (meta) {
    const metaEl = document.createElement('div');
    metaEl.className = 'msg-meta';
    metaEl.innerHTML = meta;
    bubble.appendChild(metaEl);
  }

  const main = document.createElement('div');
  main.style.display = 'flex';
  main.style.flexDirection = 'column';
  main.style.maxWidth = '76%';
  main.appendChild(bubble);

  row.appendChild(avatar);
  row.appendChild(main);

  messagesArea.appendChild(row);
  messagesArea.scrollTop = messagesArea.scrollHeight;
  return row;
}

function showTypingIndicator() {
  const row = document.createElement('div');
  row.className = 'typing-indicator';
  row.id = 'typing-indicator';

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar ai-avatar';
  avatar.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polygon points="12,2 22,7 22,17 12,22 2,17 2,7" fill="none" stroke="#C9A227" stroke-width="1.5"/><circle cx="12" cy="12" r="3" fill="#C9A227" opacity="0.5"/></svg>`;

  const dots = document.createElement('div');
  dots.className = 'typing-dots';
  dots.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

  row.appendChild(avatar);
  row.appendChild(dots);
  messagesArea.appendChild(row);
  messagesArea.scrollTop = messagesArea.scrollHeight;
}

function hideTypingIndicator() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

async function sendMessage(text) {
  if (!text || state.isProcessing) return;
  state.isProcessing = true;
  sendBtn.disabled = true;

  appendMessage('user', text);
  chatInput.value = '';
  chatInput.style.height = 'auto';
  charCount.textContent = '0 / 10000';

  const typingTimeout = setTimeout(showTypingIndicator, CONFIG.TYPING_DELAY);

  try {
    const startMs = performance.now();
    const result = await apiPost('/chat', {
      message: text,
      session_id: state.sessionId,
    });
    clearTimeout(typingTimeout);
    hideTypingIndicator();

    const latency = Math.round(performance.now() - startMs);
    const data = result.data || {};
    const response = data.response || 'No response received.';
    const model    = data.model || 'gemini-2.0-flash-exp';
    const msgId    = (data.message_id || '').slice(0, 8);

    const metaHtml = `
      <span>⚡ ${latency}ms</span>
      <span>Model: ${model}</span>
      ${msgId ? `<span>ID: ${msgId}</span>` : ''}
    `;
    appendMessage('assistant', response, metaHtml);

  } catch (err) {
    clearTimeout(typingTimeout);
    hideTypingIndicator();
    appendMessage('assistant', `⚠ Error: ${err.message}`, '');
    toast(err.message, 'error');
  } finally {
    state.isProcessing = false;
    sendBtn.disabled = chatInput.value.trim().length === 0;
  }
}

// Chat input events
if (chatInput) {
  chatInput.addEventListener('input', () => {
    // Auto-resize
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 180) + 'px';
    // Char count
    const len = chatInput.value.length;
    charCount.textContent = `${len} / 10000`;
    // Enable send
    sendBtn.disabled = len === 0 || state.isProcessing;
  });

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (text) sendMessage(text);
    }
  });
}
if (sendBtn) {
  sendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (text) sendMessage(text);
  });
}

// Suggestion chips
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const prompt = chip.dataset.prompt;
    if (chatInput && prompt) {
      chatInput.value = prompt;
      chatInput.dispatchEvent(new Event('input'));
      chatInput.focus();
    }
  });
});

// New session button
const newSessionBtn = document.getElementById('new-session-btn');
if (newSessionBtn) {
  newSessionBtn.addEventListener('click', async () => {
    await createSession();
    toast('New session started', 'success');
  });
}

// Clear history
const clearBtn = document.getElementById('clear-btn');
if (clearBtn) {
  clearBtn.addEventListener('click', async () => {
    if (!state.sessionId) return;
    try {
      await fetch(`${CONFIG.API_BASE}/chat/history/${state.sessionId}`, { method: 'DELETE' });
    } catch {}
    // Clear UI
    messagesArea.innerHTML = '';
    messagesArea.appendChild(welcomeMsg);
    welcomeMsg.classList.remove('hidden');
    toast('Conversation cleared', 'info');
  });
}

// ══════════════════════════════════════════════════════
//  IMAGE ANALYSIS
// ══════════════════════════════════════════════════════
const imgDropZone     = document.getElementById('img-drop-zone');
const imgFileInput    = document.getElementById('img-file-input');
const imgPreviewContainer = document.getElementById('img-preview-container');
const imgPreview      = document.getElementById('img-preview');
const imgRemoveBtn    = document.getElementById('img-remove-btn');
const analyzeImgBtn   = document.getElementById('analyze-img-btn');
const visionResult    = document.getElementById('vision-result');
const visionResultText= document.getElementById('vision-result-text');
const visionResultMeta= document.getElementById('vision-result-meta');
const visionPromptEl  = document.getElementById('vision-prompt');

function setImageFile(file) {
  if (!file) return;
  state.imageFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    imgPreview.src = e.target.result;
    imgDropZone.classList.add('hidden');
    imgPreviewContainer.classList.remove('hidden');
    analyzeImgBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

if (imgDropZone) {
  imgDropZone.addEventListener('click', () => imgFileInput.click());
  imgDropZone.addEventListener('keydown', e => e.key === 'Enter' && imgFileInput.click());
  imgDropZone.addEventListener('dragover',  e => { e.preventDefault(); imgDropZone.classList.add('dragover'); });
  imgDropZone.addEventListener('dragleave', () => imgDropZone.classList.remove('dragover'));
  imgDropZone.addEventListener('drop', e => {
    e.preventDefault();
    imgDropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) setImageFile(file);
  });
}
if (imgFileInput) {
  imgFileInput.addEventListener('change', () => {
    if (imgFileInput.files[0]) setImageFile(imgFileInput.files[0]);
  });
}
if (imgRemoveBtn) {
  imgRemoveBtn.addEventListener('click', () => {
    state.imageFile = null;
    imgPreview.src  = '';
    imgFileInput.value = '';
    imgDropZone.classList.remove('hidden');
    imgPreviewContainer.classList.add('hidden');
    analyzeImgBtn.disabled = true;
    visionResult.classList.add('hidden');
  });
}

if (analyzeImgBtn) {
  analyzeImgBtn.addEventListener('click', async () => {
    if (!state.imageFile) return;
    const prompt = visionPromptEl?.value || 'Describe this image in detail.';

    analyzeImgBtn.disabled = true;
    analyzeImgBtn.innerHTML = '<span class="spinner"></span> Analysing…';

    try {
      const fd = new FormData();
      fd.append('file', state.imageFile, state.imageFile.name);
      fd.append('prompt', prompt);
      if (state.sessionId) fd.append('session_id', state.sessionId);

      const result = await apiPost('/analyze/image', fd, true);
      const data   = result.data || {};

      visionResultText.textContent = data.analysis || '';
      visionResultMeta.innerHTML   = `
        <span>📐 ${data.image_size?.width || '?'} × ${data.image_size?.height || '?'} px</span>
        <span>⚡ ${data.latency_ms?.toFixed(0) || '?'} ms</span>
        <span>🤖 ${data.model || 'gemini'}</span>
      `;
      visionResult.classList.remove('hidden');
      toast('Image analysed successfully', 'success');
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      analyzeImgBtn.disabled = false;
      analyzeImgBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="8" stroke="#0A0A0A" stroke-width="2"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="#0A0A0A" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Analyse Image`;
    }
  });
}

// ══════════════════════════════════════════════════════
//  DOCUMENT ANALYSIS
// ══════════════════════════════════════════════════════
const docDropZone   = document.getElementById('doc-drop-zone');
const docFileInput  = document.getElementById('doc-file-input');
const docFileInfo   = document.getElementById('doc-file-info');
const analyzeDocBtn = document.getElementById('analyze-doc-btn');
const docResult     = document.getElementById('doc-result');
const docResultText = document.getElementById('doc-result-text');
const docResultMeta = document.getElementById('doc-result-meta');
const docQueryEl    = document.getElementById('doc-query');

function setDocFile(file) {
  if (!file) return;
  state.docFile = file;
  docFileInfo.innerHTML = `
    <strong style="color:var(--gold-primary)">✦ ${file.name}</strong><br>
    <span style="opacity:.7">${(file.size / 1024).toFixed(1)} KB</span>
  `;
  docFileInfo.classList.remove('hidden');
  analyzeDocBtn.disabled = false;
}

if (docDropZone) {
  docDropZone.addEventListener('click', () => docFileInput.click());
  docDropZone.addEventListener('keydown', e => e.key === 'Enter' && docFileInput.click());
  docDropZone.addEventListener('dragover',  e => { e.preventDefault(); docDropZone.classList.add('dragover'); });
  docDropZone.addEventListener('dragleave', () => docDropZone.classList.remove('dragover'));
  docDropZone.addEventListener('drop', e => {
    e.preventDefault();
    docDropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) setDocFile(file);
  });
}
if (docFileInput) {
  docFileInput.addEventListener('change', () => {
    if (docFileInput.files[0]) setDocFile(docFileInput.files[0]);
  });
}

if (analyzeDocBtn) {
  analyzeDocBtn.addEventListener('click', async () => {
    if (!state.docFile) return;
    const query = docQueryEl?.value || 'Summarize this document.';

    analyzeDocBtn.disabled = true;
    analyzeDocBtn.innerHTML = '<span class="spinner"></span> Processing…';

    try {
      const fd = new FormData();
      fd.append('file', state.docFile, state.docFile.name);
      fd.append('query', query);
      if (state.sessionId) fd.append('session_id', state.sessionId);

      const result = await apiPost('/analyze/document', fd, true);
      const data   = result.data || {};

      docResultText.textContent = data.analysis || '';
      docResultMeta.innerHTML   = `
        <span>📄 ${data.filename || ''} (${data.file_type || ''})</span>
        <span>💾 ${data.file_size_kb?.toFixed(1) || '?'} KB</span>
        <span>⚡ ${data.latency_ms?.toFixed(0) || '?'} ms</span>
      `;
      docResult.classList.remove('hidden');
      toast('Document analysed successfully', 'success');
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      analyzeDocBtn.disabled = false;
      analyzeDocBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M9 3C6.24 3 4 5.24 4 8c0 1.2.44 2.3 1.17 3.13C4.45 11.67 4 12.79 4 14c0 2.21 1.34 4.1 3.27 4.77" stroke="#0A0A0A" stroke-width="1.6" fill="none"/>
        </svg>
        Analyse Document`;
    }
  });
}

// ══════════════════════════════════════════════════════
//  NAV ACTIVE LINK (scroll spy)
// ══════════════════════════════════════════════════════
(function initScrollSpy() {
  const sections = ['hero', 'chat-section', 'vision-section', 'docs-section'];
  const navLinks  = document.querySelectorAll('.nav-link');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio > 0.4) {
          navLinks.forEach(l => l.classList.remove('active'));
          const link = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
          if (link) link.classList.add('active');
        }
      });
    },
    { threshold: 0.4 }
  );

  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el) observer.observe(el);
  });
})();

// ══════════════════════════════════════════════════════
//  SMOOTH NAVBAR SHADOW ON SCROLL
// ══════════════════════════════════════════════════════
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  if (nav) {
    nav.style.boxShadow = window.scrollY > 20
      ? '0 2px 30px rgba(201,162,39,0.1)'
      : 'none';
  }
}, { passive: true });

// ══════════════════════════════════════════════════════
//  STARTUP
// ══════════════════════════════════════════════════════
(async function init() {
  await createSession();
  await checkHealth();
  // Re-check health every 30s
  setInterval(checkHealth, 30000);
})();
