import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [isRightPanelActive, setIsRightPanelActive] = useState(false);
    const navigate = useNavigate();

    const [signupEmail, setSignupEmail] = useState('');
    const [signupPassword, setSignupPassword] = useState('');


    const handleSignUp = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('https://dztmp5gmbe.execute-api.us-east-1.amazonaws.com/prod/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: signupEmail,
                    password: signupPassword,
                }),
            });

            if (response.ok) {
                const data = await response.json(); // opzionale, dipende dalla tua lambda
                console.log("[Frontend] Signup success:", data);
                navigate('/');
            } else {
                const errorText = await response.text();
                console.error("[Frontend] Signup failed:", errorText);
                alert("Errore durante la registrazione");
            }
        } catch (error) {
            console.error("[Frontend] Network error:", error);
            alert("Errore di rete");
        }
    };


    const handleSignIn = (e) => {
        e.preventDefault(); 
        navigate('/');
    };


    return (
        <div className='Login'>
            <div className={`container ${isRightPanelActive ? 'right-panel-active' : ''}`} id="container">

                <div className="form-container sign-up-container">
                    <form onSubmit={handleSignUp}>
                    <h1>Create Account</h1>
                    <input type="text" placeholder="Name" />
                    <input
                        type="email"
                        placeholder="Email"
                        value={signupEmail}s
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

                        <input type="email" placeholder="Email" />
                        <input type="password" placeholder="Password" />
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
