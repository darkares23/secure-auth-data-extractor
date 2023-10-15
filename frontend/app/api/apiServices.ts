const AUTH_URL = "/api/authenticate";
const DATA_EXTRACTION_URL = "/api/extract_data/";

export const testGetMethod = async () => {
    const response = await fetch(AUTH_URL, {
        method: "GET",
    });
    return response.json();
}

export const verifyGoogleToken = async (token: string) => {
    const response = await fetch(`${AUTH_URL}/google/`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ token }),
    });
    return response.json();
}

export const extractData = async (text: string) => {
    const response = await fetch(DATA_EXTRACTION_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ text }),
    });

    if (!response.ok) {
        throw new Error("Error extracting data");
    }

    return response.json();
}