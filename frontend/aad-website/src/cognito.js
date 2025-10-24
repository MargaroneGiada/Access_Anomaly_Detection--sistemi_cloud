import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails
} from "amazon-cognito-identity-js";

const poolData = {
  UserPoolId: "us-east-1_8YWjvIQWa", 
  ClientId: "2h42ge8aitpkuc2c2grlqmt32e"
};

const userPool = new CognitoUserPool(poolData);

// Signup
export function signUp(username, password, email) {
  return new Promise((resolve, reject) => {
    userPool.signUp(
      username,
      password,
      [{ Name: "email", Value: email }],
      null,
      (err, result) => {
        if (err) reject(err);
        else resolve(result);
      }
    );
  });
}

// Conferma signup (codice email/SMS inviato da Cognito)
export function confirmSignUp(username, code) {
  const user = new CognitoUser({ Username: username, Pool: userPool });
  return new Promise((resolve, reject) => {
    user.confirmRegistration(code, true, (err, result) => {
      if (err) reject(err);
      else resolve(result);
    });
  });
}

// Login
export function signIn(username, password) {
  const authDetails = new AuthenticationDetails({
    Username: username,
    Password: password,
  });
  const user = new CognitoUser({ Username: username, Pool: userPool });

  return new Promise((resolve, reject) => {
    user.authenticateUser(authDetails, {
      onSuccess: (result) => {
        const accessToken = result.getAccessToken().getJwtToken();
        const idToken = result.getIdToken().getJwtToken();
        const refreshToken = result.getRefreshToken().getToken();

        resolve({ accessToken, idToken, refreshToken });
      },
      onFailure: (err) => reject(err),
    });
  });
}
