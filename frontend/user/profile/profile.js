const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/auth/login/login.html";
        return;
    }

    // Configurar el botón de publicar
    document.getElementById("btnPublish").addEventListener("click", () => crearPost(token));

    // Cargar datos iniciales
    await Promise.all([
        cargarDatosPerfil(token),
        cargarPosts(token)
    ]);
});

// --- FUNCIONES DEL PERFIL ---
async function cargarDatosPerfil(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const usuario = await response.json();

        document.getElementById("userFullName").textContent = usuario.full_name || "Usuario";
        document.getElementById("userUsername").textContent = `@${usuario.username}`;
        document.getElementById("userEmail").textContent = usuario.email;
        document.getElementById("userBio").textContent = usuario.bio || "Sin biografía.";
        
        if (usuario.created_at) {
            const fecha = new Date(usuario.created_at).toLocaleDateString("es-ES", {
                year: 'numeric', month: 'long', day: 'numeric'
            });
            document.getElementById("userDate").textContent = fecha;
        }
        if (usuario.profile_picture) document.getElementById("userAvatar").src = usuario.profile_picture;

    } catch (error) {
        console.error("Error al cargar perfil:", error);
    }
}

// --- CRUD DE POSTS ---

// 1. OBTENER POSTS
async function cargarPosts(token) {
    const container = document.getElementById("postsContainer");
    try {
        const response = await fetch(`${API_BASE_URL}/posts/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const posts = await response.json();
        container.innerHTML = "";

        if (posts.length === 0) {
            container.innerHTML = `<p class="text-gray-400 text-center text-sm">No hay publicaciones.</p>`;
            return;
        }

        posts.forEach(post => {
            const card = document.createElement("div");
            card.className = "p-4 bg-gray-50 rounded-lg border border-gray-100 relative group";
            card.innerHTML = `
                <div id="content-${post.id}" class="text-gray-800 text-sm whitespace-pre-wrap">${post.content}</div>
                <div class="flex justify-between items-center mt-3">
                    <span class="text-[10px] text-gray-400 italic">${new Date(post.created_at).toLocaleString()}</span>
                    <div class="space-x-2">
                        <button onclick="prepararEdicion('${post.id}', '${token}')" class="text-blue-500 hover:underline text-xs">Editar</button>
                        <button onclick="eliminarPost('${post.id}', '${token}')" class="text-red-500 hover:underline text-xs">Eliminar</button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        container.innerHTML = `<p class="text-red-500">Error al conectar con el servidor.</p>`;
    }
}

// 2. CREAR POST
async function crearPost(token) {
    const contentArea = document.getElementById("postContent");
    const content = contentArea.value.trim();

    if (!content) return alert("¡Escribe algo primero!");

    try {
        const response = await fetch(`${API_BASE_URL}/posts/`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: content })
        });

        if (response.ok) {
            contentArea.value = "";
            cargarPosts(token); // Recargar la lista
        }
    } catch (error) {
        alert("Error al publicar");
    }
}

// 3. ELIMINAR POST
async function eliminarPost(postId, token) {
    if (!confirm("¿Seguro que quieres borrar esto?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.ok) cargarPosts(token);
    } catch (error) {
        alert("No se pudo eliminar");
    }
}

// 4. EDITAR POST (Interfaz simple)
function prepararEdicion(postId, token) {
    const div = document.getElementById(`content-${postId}`);
    const originalText = div.innerText;

    div.innerHTML = `
        <textarea id="edit-${postId}" class="w-full p-2 border rounded text-sm">${originalText}</textarea>
        <div class="flex gap-2 mt-1">
            <button onclick="guardarEdicion('${postId}', '${token}')" class="bg-green-500 text-white px-2 py-1 rounded text-[10px]">Guardar</button>
            <button onclick="cargarPosts('${token}')" class="bg-gray-400 text-white px-2 py-1 rounded text-[10px]">Cancelar</button>
        </div>
    `;
}

async function guardarEdicion(postId, token) {
    const newContent = document.getElementById(`edit-${postId}`).value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: newContent })
        });

        if (response.ok) cargarPosts(token);
    } catch (error) {
        alert("Error al actualizar");
    }
}

function cerrarSesion() {
    // 1. Borramos el token y cualquier dato del usuario
    localStorage.removeItem("token");
    
    // 2. Redirigimos al login
    window.location.href = "/auth/login/login.html";
}