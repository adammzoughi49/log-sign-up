import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  const name = localStorage.getItem("name") || "User";

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Welcome, {name}!</h2>
        <p style={{ color: "#666" }}>You are successfully logged in.</p>
        <button style={styles.btn} onClick={logout}>Log out</button>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f5f5f5" },
  card: { background: "#fff", padding: "2rem", borderRadius: 12, width: 360, boxShadow: "0 2px 16px rgba(0,0,0,0.08)", textAlign: "center" },
  title: { fontWeight: 500, fontSize: 22, marginBottom: "0.5rem" },
  btn: { marginTop: "1.5rem", padding: "10px 24px", background: "#dc2626", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, cursor: "pointer" }
};