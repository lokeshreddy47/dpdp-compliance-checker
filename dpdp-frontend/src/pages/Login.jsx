import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";

function Login({ setUser }) {
  const navigate = useNavigate();
  const googleBtnRef = useRef(null);

  useEffect(() => {
    // Auto-login if user exists in localStorage
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        setUser(u);
        navigate("/dashboard");
        return;
      } catch (e) {
        console.error("Failed to parse saved user", e);
        localStorage.removeItem("user");
      }
    }

    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId || clientId === "YOUR_GOOGLE_OAUTH_CLIENT_ID_HERE.apps.googleusercontent.com") {
      console.warn("VITE_GOOGLE_CLIENT_ID not set or using placeholder. Google Sign-In disabled.");
      return;
    }

    // Load Google Identity Services script if not already loaded
    const addScriptAndInit = () => {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        initializeGSI();
        return;
      }

      const existing = document.getElementById("google-identity");
      if (existing) {
        existing.addEventListener("load", initializeGSI);
        return;
      }

      const script = document.createElement("script");
      script.src = "https://accounts.google.com/gsi/client";
      script.async = true;
      script.defer = true;
      script.id = "google-identity";
      script.onload = initializeGSI;
      document.head.appendChild(script);
    };

    function initializeGSI() {
      if (!window.google || !window.google.accounts || !window.google.accounts.id) return;

      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: handleCredentialResponse,
      });

      // Render the Google button into our placeholder div
      if (googleBtnRef.current) {
        window.google.accounts.id.renderButton(googleBtnRef.current, {
          theme: "outline",
          size: "large",
          width: "100%",
        });
      }

      // Optionally show One Tap
      // window.google.accounts.id.prompt();
    }

    function handleCredentialResponse(response) {
      if (!response || !response.credential) return;
      const payload = parseJwt(response.credential);
      const userData = {
        uid: payload.sub,
        email: payload.email,
        displayName: payload.name,
        photoURL: payload.picture,
        emailVerified: payload.email_verified,
      };

      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);
      // Optionally: send id_token to backend for verification
      // await fetch("http://localhost:8000/api/auth/google", { method: "POST", body: JSON.stringify({ token: response.credential }) })

      navigate("/dashboard");
    }

    function parseJwt(token) {
      try {
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split("")
            .map(function (c) {
              return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join("")
        );
        return JSON.parse(jsonPayload);
      } catch (e) {
        console.error("Failed to parse JWT", e);
        return {};
      }
    }

    addScriptAndInit();
  }, [navigate, setUser]);

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="backdrop-blur-lg bg-white/10 border border-white/20 p-10 rounded-2xl shadow-2xl w-96"
      >
        <h1 className="text-3xl font-bold text-white text-center mb-6">DPDP Compliance Checker</h1>
        <p className="text-gray-300 text-center mb-6">AI Powered Privacy Compliance</p>

        {/* Show Google button or setup message */}
        {import.meta.env.VITE_GOOGLE_CLIENT_ID && import.meta.env.VITE_GOOGLE_CLIENT_ID !== "YOUR_GOOGLE_OAUTH_CLIENT_ID_HERE.apps.googleusercontent.com" ? (
          <div ref={googleBtnRef} />
        ) : (
          <div className="text-center">
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 mb-4">
              <p className="text-red-300 text-sm mb-2">⚠️ Google OAuth Not Configured</p>
              <p className="text-gray-300 text-xs">
                Please set up your Google Client ID in the .env file to enable login.
              </p>
            </div>
            <button
              onClick={() => window.open('https://console.cloud.google.com/apis/credentials', '_blank')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Setup Google OAuth
            </button>
          </div>
        )}

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">Secure authentication using Google Identity Services</p>
        </div>
      </motion.div>
    </div>
  );
}

export default Login;