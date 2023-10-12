import React from 'react';
import jwt_decode from "jwt-decode";
import googleLogin from './services/googleLogin';
import { useGoogleLogin, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

function App() {
  
  const clientId="901993024196-44r7mfptmsop6thoop998km07h0l2blk.apps.googleusercontent.com"

  const responseGoogle = async(response) => {
    console.log(response)
    let googleResponse  = await googleLogin(response.credential)
    console.log(googleResponse);
  }

  return (
    <>
      <GoogleLogin
        onSuccess={response => {
          responseGoogle(response);
        }}
        onError={() => {
          console.log('Login Failed');
        }}
      />;
    </>
  )
}


export default App;
