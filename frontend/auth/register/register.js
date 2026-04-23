const registerForm = document.getElementById('registerForm');
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

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/users/register', { // Ajusta según tu ruta
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.className = "mt-4 text-center text-sm font-semibold text-blue-600"; // Cambiado a azul
            messageDiv.innerText = "Usuario creado con éxito. Redirigiendo al login...";
            setTimeout(() => { window.location.href = "../login/login.html"; }, 2000);
        } else {
            messageDiv.className = "mt-4 text-center text-sm font-semibold text-red-600";
            messageDiv.innerText = data.detail || "Error al crear cuenta";
        }
    } catch (error) {
        messageDiv.className = "mt-4 text-center text-sm font-semibold text-red-600";
        messageDiv.innerText = "Error de conexión.";
    }
});