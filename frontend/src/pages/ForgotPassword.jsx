import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/auth/forgot-password", { email });
      setMessage(res.data.message);
    } catch {
      setMessage("Something went wrong");
    }
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Reset password</h2>
        <p style={styles.sub}>Enter your email and we'll send a reset link.</p>
        {message ? <p style={styles.success}>{message}</p> : (
          <form onSubmit={handleSubmit}>
            <input style={styles.input} type="email" placeholder="Email address" value={email} onChange={e => setEmail(e.target.value)} required />
            <button style={styles.btn} disabled={loading}>{loading ? "Sending..." : "Send reset link"}</button>
          </form>
        )}
        <p style={styles.link}><Link to="/login">Back to login</Link></p>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f5f5f5" },
  card: { background: "#fff", padding: "2rem", borderRadius: 12, width: 360, boxShadow: "0 2px 16px rgba(0,0,0,0.08)" },
  title: { marginBottom: "0.5rem", fontWeight: 500, fontSize: 22 },
  sub: { color: "#666", fontSize: 14, marginBottom: "1.25rem" },
  input: { display: "block", width: "100%", padding: "10px 12px", marginBottom: 12, border: "1px solid #ddd", borderRadius: 8, fontSize: 15, boxSizing: "border-box" },
  btn: { width: "100%", padding: "11px", background: "#4F46E5", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, cursor: "pointer" },
  success: { color: "#16a34a", fontSize: 14, padding: "10px", background: "#f0fdf4", borderRadius: 8 },
  link: { textAlign: "center", marginTop: "1rem", fontSize: 14, color: "#666" }
};