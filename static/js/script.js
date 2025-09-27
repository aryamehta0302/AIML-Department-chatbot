// 🌐 Elements
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');
const languageSelect = document.getElementById('languageSelect');
const micToggle = document.getElementById('micToggle');
const voiceToggle = document.getElementById('voiceToggle');

// 🛑 Optional stop button (if added in HTML)
const stopVoiceBtn = document.getElementById('stopVoice');

let recognizing = false;
let recognition;
let chatHistory = [];
let isSpeaking = false; // track speech status

// ✉️ Handle Message Send
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  const lang = languageSelect.value;
  if (!message) return;

  addMessage(message, 'user');
  userInput.value = '';
  const loadingRef = addMessage('Thinking...', 'bot');

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: message, language: lang })
    });

    const data = await response.json();
    if (data.answer) {
      const cleaned = cleanBotReply(data.answer);
      const formatted = formatAnswer(cleaned);
      updateMessage(loadingRef, formatted, true);

      chatHistory.push({ question: message, answer: formatted });

      // 🔊 Speak only once per reply
      speakResponse(cleaned, lang);
    } else {
      updateMessage(loadingRef, data.error || "❌ Something went wrong.", true);
    }
  } catch (err) {
    updateMessage(loadingRef, "❌ Failed to reach server.", true);
  }
});

// 🎙️ Voice Input
micToggle.addEventListener('click', () => {
  if (recognizing) {
    recognition.stop();
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('🎙️ Your browser does not support speech recognition.');
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang =
    languageSelect.value === 'hi' ? 'hi-IN' :
    languageSelect.value === 'gu' ? 'gu-IN' :
    languageSelect.value === 'ta' ? 'ta-IN' :
    languageSelect.value === 'te' ? 'te-IN' : 'en-IN';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    recognizing = true;
    micToggle.classList.replace('btn-secondary', 'btn-danger');
    micToggle.innerHTML = '<i class="bi bi-stop-circle"></i>';
  };

  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
  };

  recognition.onerror = () => stopMic();
  recognition.onend = () => stopMic();

  recognition.start();
});

function stopMic() {
  recognizing = false;
  micToggle.classList.replace('btn-danger', 'btn-secondary');
  micToggle.innerHTML = '<i class="bi bi-mic"></i>';
}

// 🔊 Speak response (clean, once)
function speakResponse(text, lang) {
  if (!voiceToggle.checked || !text) return; // skip if disabled or empty

  // 🧹 Clean text
  const speakText = text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/[*_#`]/g, '')
    .replace(/<[^>]*>?/gm, '')
    .trim();

  // 🚫 Cancel previous speech if ongoing
  if (isSpeaking) {
    window.speechSynthesis.cancel();
    isSpeaking = false;
  }

  const utterance = new SpeechSynthesisUtterance(speakText);
  utterance.lang =
    lang === 'hi' ? 'hi-IN' :
    lang === 'gu' ? 'gu-IN' :
    lang === 'ta' ? 'ta-IN' :
    lang === 'te' ? 'te-IN' : 'en-IN';

  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  utterance.onstart = () => { isSpeaking = true; };
  utterance.onend = () => { isSpeaking = false; };

  window.speechSynthesis.speak(utterance);
}

// 🛑 Stop voice manually
if (stopVoiceBtn) {
  stopVoiceBtn.addEventListener('click', () => {
    window.speechSynthesis.cancel();
    isSpeaking = false;
  });
}

// 🧹 Clean Gemini replies
function cleanBotReply(text) {
  let cleaned = text;
  const patterns = [
    /^based on (the )?provided text[:,]?\s*/i,
    /^according to (the )?(context|text)[:,]?\s*/i,
    /^from (the )?(given|provided) (text|information)[:,]?\s*/i,
    /^as mentioned (in|by) (the )?text[:,]?\s*/i,
    /^the passage (states|suggests)[:,]?\s*/i,
    /^in (summary|conclusion)[:,]?\s*/i,
    /^to (summarize|conclude)[:,]?\s*/i
  ];
  patterns.forEach(p => cleaned = cleaned.replace(p, ""));
  return cleaned.trim();
}

// ✨ Format Answer (Markdown → HTML)
function formatAnswer(text) {
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
    .replace(/(?<!\n)\*(.*?)\*/g, "<i>$1</i>")
    .replace(/(?:^\*|^-|^•)\s+(.*)/gm, "<li>$1</li>")
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>");
  if (formatted.includes("<li>")) formatted = "<ul>" + formatted + "</ul>";
  return formatted;
}

// 💬 UI Helpers
function addMessage(text, type) {
  const div = document.createElement('div');
  div.className = `message ${type}-message mb-2`;

  const content = document.createElement('div');
  content.className = `message-content ${type}-content`;
  content.innerHTML = type === 'bot'
    ? `<div class="fw-bold mb-1">AIML Assistant</div><div>${text}</div>`
    : `<div>${text}</div>`;

  div.appendChild(content);
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return content;
}

function updateMessage(contentDiv, newHTML, overwrite = false) {
  contentDiv.innerHTML = overwrite ? newHTML : contentDiv.innerHTML + newHTML;
}
