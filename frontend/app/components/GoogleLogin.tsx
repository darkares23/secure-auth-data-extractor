"use client";
import decodeJwt from "../utils/decodeJwt";
import { CredentialResponse, GoogleLogin as GLogin } from "@react-oauth/google";
import { useState, useEffect } from "react";


export default function GoogleLogin() {
  const [email, setEmail] = useState<string | null>(null);
  const [name, setName] = useState<string | null>(null);
  async function testGetMethod() {
      const response = await fetch("/api/authenticate/", {
          method: "GET",
      });
      const json = await response.json();
      console.log("GET response", json);
  }

  useEffect(() => {
      testGetMethod();
  }, []);

  async function handleSuccess(credentialResponse: CredentialResponse) {
    console.log("credentialResponse", credentialResponse);
    if (credentialResponse.credential) {
      const { payload } = decodeJwt(credentialResponse.credential);
      console.log("payload credential", payload);
      const response = await fetch("/api/authenticate/google/", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          token: credentialResponse.credential,
        }),
      });
      const json = await response.json();
      console.log("verify", json);
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
