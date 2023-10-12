"use client";
import React from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import  GoogleLogin from './components/GoogleLogin'


export default function Home() {
  return (
    <GoogleOAuthProvider clientId="452689039897-h894hqefqkcbae2oe2h9354phms4an7n.apps.googleusercontent.com">
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
            <GoogleLogin />
        </Box>
      </main>
    </GoogleOAuthProvider>
  )
}
