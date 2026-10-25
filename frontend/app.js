const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const loading = document.getElementById('loading');
const resultBox = document.getElementById('resultBox');
const answerText = document.getElementById('answerText');

async function handleAsk() {
  const question = questionInput.value.trim();
  if (!question) return;

  // Mostrar cargando y ocultar resultado anterior
  loading.classList.remove('hidden');
  resultBox.classList.add('hidden');
  answerText.textContent = '';

  try {
    const response = await fetch('http://localhost:8000/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question }),
    });

    const data = await response.json();
    answerText.textContent = data.answer || data.detail || 'Sin respuesta';
    resultBox.classList.remove('hidden');
  } catch (error) {
    answerText.textContent = 'Error al conectar con el servidor backend.';
    resultBox.classList.remove('hidden');
  } finally {
    loading.classList.add('hidden');
  }
}

askBtn.addEventListener('click', handleAsk);

// Permitir pulsar Enter para enviar
questionInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleAsk();
});