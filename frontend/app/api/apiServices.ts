const BASE_URL = "/api/authenticate";

export async function testGetMethod() {
    const response = await fetch(BASE_URL, {
        method: "GET",
    });
    return response.json();
}

export async function verifyGoogleToken(token: string) {
    const response = await fetch(`${BASE_URL}/google/`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ token }),
    });
    return response.json();
}
