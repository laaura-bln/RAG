const API_BASE = 'http://localhost:8000/api';

// Elementos - URL
const urlInput = document.getElementById('urlInput');
const ingestUrlBtn = document.getElementById('ingestUrlBtn');
const urlStatus = document.getElementById('urlStatus');

// Elementos - PDF
const pdfInput = document.getElementById('pdfInput');
const ingestPdfBtn = document.getElementById('ingestPdfBtn');
const pdfStatus = document.getElementById('pdfStatus');

// Elementos - Excel
const excelInput = document.getElementById('excelInput');
const ingestExcelBtn = document.getElementById('ingestExcelBtn');
const excelStatus = document.getElementById('excelStatus');

// Elementos - Preguntas
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const loading = document.getElementById('loading');
const resultBox = document.getElementById('resultBox');
const answerText = document.getElementById('answerText');

// 1. Ingerir Web
ingestUrlBtn.addEventListener('click', async () => {
  const url = urlInput.value.trim();
  if (!url) return alert('Introduce una URL.');

  urlStatus.textContent = 'Procesando e ingiriendo página web...';
  urlStatus.classList.remove('hidden');

  try {
    const res = await fetch(`${API_BASE}/ingest-url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    urlStatus.textContent = data.message;
    if (data.status === 'success') urlInput.value = '';
  } catch (err) {
    urlStatus.textContent = 'Error de conexión con el servidor.';
  }
});

// 2. Ingerir PDF
ingestPdfBtn.addEventListener('click', async () => {
  const file = pdfInput.files[0];
  if (!file) return alert('Selecciona un archivo PDF.');

  pdfStatus.textContent = 'Procesando e ingiriendo PDF...';
  pdfStatus.classList.remove('hidden');

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_BASE}/ingest-pdf`, {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    pdfStatus.textContent = data.message;
    if (data.status === 'success') pdfInput.value = '';
  } catch (err) {
    pdfStatus.textContent = 'Error de conexión con el servidor.';
  }
});

// 3. Ingerir Excel
ingestExcelBtn.addEventListener('click', async () => {
  const file = excelInput.files[0];
  if (!file) return alert('Selecciona un archivo Excel.');

  excelStatus.textContent = 'Procesando e ingiriendo Excel...';
  excelStatus.classList.remove('hidden');

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_BASE}/ingest-excel`, {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    excelStatus.textContent = data.message;
    if (data.status === 'success') excelInput.value = '';
  } catch (err) {
    excelStatus.textContent = 'Error de conexión con el servidor.';
  }
});

// 4. Consultar RAG
async function handleAsk() {
  const question = questionInput.value.trim();
  if (!question) return;

  loading.classList.remove('hidden');
  resultBox.classList.add('hidden');

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    answerText.textContent = data.answer || data.detail || 'Sin respuesta';
    resultBox.classList.remove('hidden');
  } catch (err) {
    answerText.textContent = 'Error al conectar con el servidor.';
    resultBox.classList.remove('hidden');
  } finally {
    loading.classList.add('hidden');
  }
}

askBtn.addEventListener('click', handleAsk);
questionInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleAsk();
});