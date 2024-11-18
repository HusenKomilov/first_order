document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const full_name = document.getElementById('full_name').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8001/api/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name, password })
        });

        if (!response.ok) {
            throw new Error('Invalid login credentials');
        }

        const data = await response.json();
        console.log(data)
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        window.location.href = '/api/cars';
    } catch (error) {
        document.getElementById('error-message').textContent = error.message;
    }
});
