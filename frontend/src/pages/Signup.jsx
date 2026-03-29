import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

export default function Signup() {
  const [form, setForm] = useState({ full_name: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirm) return setError("Passwords do not match");
    setLoading(true);
    try {
      await api.post("/auth/signup", { full_name: form.full_name, email: form.email, password: form.password });
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed");
    }
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Create account</h2>
        {error && <p style={styles.error}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input style={styles.input} placeholder="Full name" value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})} required />
          <input style={styles.input} type="email" placeholder="Email address" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
          <input style={styles.input} type="password" placeholder="Password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required />
          <input style={styles.input} type="password" placeholder="Confirm password" value={form.confirm} onChange={e => setForm({...form, confirm: e.target.value})} required />
          <button style={styles.btn} disabled={loading}>{loading ? "Creating..." : "Sign up"}</button>
        </form>
        <p style={styles.link}>Already have an account? <Link to="/login">Log in</Link></p>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f5f5f5" },
  card: { background: "#fff", padding: "2rem", borderRadius: 12, width: 360, boxShadow: "0 2px 16px rgba(0,0,0,0.08)" },
  title: { marginBottom: "1.5rem", fontWeight: 500, fontSize: 22 },
  input: { display: "block", width: "100%", padding: "10px 12px", marginBottom: 12, border: "1px solid #ddd", borderRadius: 8, fontSize: 15, boxSizing: "border-box" },
  btn: { width: "100%", padding: "11px", background: "#4F46E5", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, cursor: "pointer", marginTop: 4 },
  error: { color: "#dc2626", fontSize: 14, marginBottom: 12 },
  link: { textAlign: "center", marginTop: "1rem", fontSize: 14, color: "#666" }
};