"use client";
import { CredentialResponse, GoogleLogin as GLogin } from "@react-oauth/google";
import { useState, useEffect } from "react";
import { testGetMethod, verifyGoogleToken } from "../api/apiServices";

export default function GoogleLogin() {
    const [email, setEmail] = useState<string | null>(null);
    const [name, setName] = useState<string | null>(null);

    useEffect(() => {
        async function fetchAndLog() {
            const json = await testGetMethod();
            console.log("response", json);
        }

        fetchAndLog();
    }, []);

    async function handleSuccess(credentialResponse: CredentialResponse) {
        if (credentialResponse.credential) {
            const json = await verifyGoogleToken(credentialResponse.credential);
            setEmail(json.email);
            setName(json.name);
        }
    }

    function handleError() {
        console.log("Login failed");
    }

    return (
        <div>
            {!email && (
                <GLogin
                    onSuccess={handleSuccess}
                    onError={handleError}
                    useOneTap
                />
            )}
            {(email && name) && <p>User is succesfully logged in : {name}   =  {email}</p>}
        </div>
    );
}
