const loginForm = document.getElementById('loginForm');
const messageDiv = document.getElementById('message');
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eyeIcon');

togglePassword.addEventListener('click', () => {
    // Cambiar el tipo de input
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    
    // Cambiar el icono (ojo abierto / ojo cerrado)
    const iconName = type === 'password' ? 'eye' : 'eye-off';
    eyeIcon.setAttribute('data-lucide', iconName);
    
    // Re-renderizar el icono de Lucide
    lucide.createIcons();
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Limpiar mensajes previos
    messageDiv.innerText = "";
    messageDiv.className = "mt-4 text-center text-sm font-semibold";

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.classList.add('text-blue-600');
            messageDiv.innerText = "¡Login exitoso!";
            console.log("Access Token:", data.access_token);
            // El token ya está en tus manos para el siguiente módulo
        } else {
            messageDiv.classList.add('text-red-600');
            messageDiv.innerText = data.detail || "Error en el login";
        }
    } catch (error) {
        messageDiv.classList.add('text-red-600');
        messageDiv.innerText = "No se pudo conectar con el servidor.";
    }
});