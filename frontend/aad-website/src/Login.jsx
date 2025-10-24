import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
import { signIn } from "./cognito";

function Login() {
    const [isRightPanelActive, setIsRightPanelActive] = useState(false);
    const navigate = useNavigate();

    const [signupEmail, setSignupEmail] = useState('');
    const [signupPassword, setSignupPassword] = useState('');
    const [signupUsername, setSignupUsername] = useState('');

    const [signinEmail, setSigninEmail] = useState('');
    const [signinPassword, setSigninPassword] = useState('');


    const handleSignUp = async (e) => {
        e.preventDefault();
        try {
            const tokens = await signUp(signupUsername, signupPassword, signupEmail);
            console.log("Signup riuscito:", tokens);
            localStorage.setItem("idToken", tokens.idToken);
        } catch (err) {
            console.error("Errore sugnup:", err);
        }
    };


    const handleSignIn = async (e) => {
        e.preventDefault();
        try {
            const tokens = await signIn(signinEmail, signinPassword);
            console.log("Login riuscito:", tokens);
            localStorage.setItem("idToken", tokens.idToken);
        } catch (err) {
            console.error("Errore login:", err);
        }
    };


    return (
        <div className='Login'>
            <div className={`container ${isRightPanelActive ? 'right-panel-active' : ''}`} id="container">

                <div className="form-container sign-up-container">
                    <form onSubmit={handleSignUp}>
                        <h1>Create Account</h1>
                        <input
                            type="text"
                            placeholder="Username"
                            value={signupUsername}
                            onChange={(e) => setSignupUsername(e.target.value)}
                            required
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={signupEmail} s
                            onChange={(e) => setSignupEmail(e.target.value)}
                            required
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={signupPassword}
                            onChange={(e) => setSignupPassword(e.target.value)}
                            required
                        />
                        <button>Sign Up</button>
                    </form>

                </div>

                <div className="form-container sign-in-container">
                    <form onSubmit={handleSignIn}>
                        <h1>Sign in</h1>

                        <input
                            type="email"
                            placeholder="Email"
                            value={signinEmail} s
                            onChange={(e) => setSigninEmail(e.target.value)}
                            required
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={signinPassword}
                            onChange={(e) => setSigninPassword(e.target.value)}
                            required
                        />
                        <a href="#">Forgot your password?</a>
                        <button>Sign In</button>
                    </form>
                </div>

                <div className="overlay-container">
                    <div className="overlay">
                        <div className="overlay-panel overlay-left">
                            <h1>Welcome Back!</h1>
                            <p>To keep connected with us please login with your personal info</p>
                            <button className="ghost" onClick={() => setIsRightPanelActive(false)}>Sign In</button>
                        </div>
                        <div className="overlay-panel overlay-right">
                            <h1>Hello, Friend!</h1>
                            <p>Enter your personal details</p>
                            <button className="ghost" onClick={() => setIsRightPanelActive(true)}>Sign Up</button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

export default Login;
