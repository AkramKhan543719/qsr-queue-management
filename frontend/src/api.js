
const API_URL = "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("qsr_token");
}

export function saveToken(token) {
  localStorage.setItem("qsr_token", token);
}

export function clearToken() {
  localStorage.removeItem("qsr_token");
}

export async function apiRequest(path, options = {}) {
  const token = getToken();

  let response;

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
      },
    });
  } catch (error) {
    throw new Error(
      `Backend connection failed. Check that FastAPI is running at ${API_URL}.`
    );
  }

  const contentType = response.headers.get("content-type") || "";
  let result = null;

  if (response.status !== 204) {
    if (contentType.includes("application/json")) {
      result = await response.json().catch(() => null);
    } else {
      result = await response.text().catch(() => null);
    }
  }

  if (!response.ok) {
    const detail =
      result && typeof result === "object"
        ? result.detail
        : null;

    throw new Error(
      detail || `Request failed (${response.status})`
    );
  }

  return result;
}

export async function login(username, password) {
  const result = await apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

  if (result?.access_token) {
    saveToken(result.access_token);
  } else {
    throw new Error("Login response did not contain an access token.");
  }

  return result;
}

export async function register(username, email, password) {
  return apiRequest("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
}
