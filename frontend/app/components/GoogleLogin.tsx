"use client";
import { CredentialResponse, GoogleLogin as GLogin } from "@react-oauth/google";
import { useState, useEffect } from "react";
import { testGetMethod, verifyGoogleToken } from "../api/apiServices";
import TextInputComponent from "./TextInputComponent";
import { Box } from "@mui/material";

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
            console.log(credentialResponse.credential);
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
            {(email && name) && (
                <Box>
                    <p>User is succesfully logged in {name}: {email}</p>
                    <TextInputComponent />
                </Box>
            )
            }
        </div>
    );
}
