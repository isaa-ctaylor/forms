const parseHashParams = () => {
    const hash = window.location.hash.substring(1);
    const params = {};
    hash.split('&').forEach(pair => {
        const parts = pair.split('=');
        params[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1]);
    });
    return params;
};

const params = parseHashParams();
const accessToken = params.access_token;
const idToken = params.id_token;

// --- IMPORTANT: Update these values with your actual configuration ---
const BACKEND_API_URL = "http://localhost:8001"; // Your backend API's URL
const AUTH0_DOMAIN = "isaa-ctaylor.uk.auth0.com"; // Your Auth0 domain
const AUTH0_CLIENT_ID = "etB4HM6AVic1sXtWlLFMyGuDUtV7OW1p"; // Your Auth0 SPA Client ID
// --- End of IMPORTANT section ---


if (accessToken) {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('idToken', idToken); // Store ID token for display
    try {
        const decodedIdToken = JSON.parse(atob(idToken.split('.')[1]));
        document.getElementById('userInfo').textContent = `Welcome, ${decodedIdToken.nickname || decodedIdToken.name || decodedIdToken.email || decodedIdToken.sub}!`;
    } catch (e) {
        console.error("Error decoding ID token:", e);
        document.getElementById('userInfo').textContent = "Welcome, User!";
    }
} else {
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedIdToken = localStorage.getItem('idToken');
    if (storedAccessToken && storedIdToken) {
        try {
            const decodedIdToken = JSON.parse(atob(storedIdToken.split('.')[1]));
            document.getElementById('userInfo').textContent = `Welcome back, ${decodedIdToken.nickname || decodedIdToken.name || decodedIdToken.email || decodedIdToken.sub}!`;
        } catch (e) {
            console.error("Error decoding stored ID token:", e);
            document.getElementById('userInfo').textContent = "Welcome back!";
        }
    } else {
        alert("Not authenticated. Please log in.");
        window.location.href = '/';
    }
}

document.getElementById('callApiButton').addEventListener('click', async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        alert("No access token found. Please log in.");
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch(`${BACKEND_API_URL}/api/protected`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('apiResponse').textContent = JSON.stringify(data);
        } else if (response.status === 401 || response.status === 403) {
            alert("Authentication failed or insufficient permissions. Please log in again.");
            localStorage.removeItem('accessToken');
            localStorage.removeItem('idToken');
            window.location.href = '/';
        } else {
            const errorText = await response.text();
            document.getElementById('apiResponse').textContent = `Error: ${response.status} - ${errorText}`;
        }
    } catch (error) {
        console.error("Error calling API:", error);
        document.getElementById('apiResponse').textContent = "Failed to call API.";
    }
});

document.getElementById('logoutButton').addEventListener('click', () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('idToken');
    const returnToUrl = encodeURIComponent(`http://localhost:${window.location.port}`); // Dynamically get frontend port
    window.location.href = `https://${AUTH0_DOMAIN}/v2/logout?client_id=${AUTH0_CLIENT_ID}&returnTo=${returnToUrl}`;
});