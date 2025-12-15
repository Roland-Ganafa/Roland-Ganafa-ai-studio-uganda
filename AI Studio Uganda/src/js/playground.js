import '../styles/global.css';

document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.querySelector('.btn-primary');
    const inputArea = document.querySelector('.model-input');
    const outputArea = document.querySelector('.model-output');
    const progressSteps = document.querySelectorAll('.progress-step');

    runBtn.addEventListener('click', () => {
        const prompt = inputArea.value.trim();
        if (!prompt) return;

        // Visual loading state
        outputArea.innerHTML = '<span style="color:#666">Generating response... <span class="blink">|</span></span>';
        runBtn.disabled = true;
        runBtn.style.opacity = '0.7';

        // Mock delay for realism
        setTimeout(() => {
            const response = mockModelResponse(prompt);
            typeWriter(response, outputArea);
            runBtn.disabled = false;
            runBtn.style.opacity = '1';

            // Check challenge
            if (prompt.toLowerCase().includes('good morning') && prompt.toLowerCase().includes('guest')) {
                unlockAchievement();
            }
        }, 1500);
    });

    function mockModelResponse(input) {
        if (input.toLowerCase().includes('good morning')) {
            return "Wassuze otya, omugenyi omulungi. (Good morning, honored guest).";
        }
        return `[Crane-v1] Processed input: "${input}". \n\nThis is a simulated response for the playground. In a live environment, this would call the inference API.`;
    }

    function typeWriter(text, element) {
        element.innerHTML = '';
        let i = 0;
        const speed = 20;

        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    function unlockAchievement() {
        // Unlock the next step visually
        // Find first non-completed step
        // In this mock, we just light up the 3rd one
        if (progressSteps[2]) {
            progressSteps[2].classList.add('active');
            // Show toast
            alert("Challenge Complete: 'Linguist' Badge Unlocked!");
        }
    }
});

// Add blink animation style
const style = document.createElement('style');
style.innerHTML = `
@keyframes blink { 50% { opacity: 0; } }
.blink { animation: blink 1s step-end infinite; }
`;
document.head.appendChild(style);
