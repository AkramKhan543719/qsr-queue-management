
import { useCallback, useEffect, useState } from "react";
import {
  Activity, AlertTriangle, Camera, CheckCircle2, Clock3,
  LogOut, Plus, RefreshCw, ShieldCheck, Users, X,
  LayoutDashboard, TrendingUp, MapPin, Video,
} from "lucide-react";
import { apiRequest, clearToken, getToken, login } from "./api";

const initialSummary = {
  total_cameras: 0,
  active_cameras: 0,
  latest_customer_count: 0,
  latest_queue_length: 0,
  latest_wait_seconds: 0,
  unacknowledged_alerts: 0,
};

function formatWait(seconds = 0) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return mins ? `${mins}m ${secs}s` : `${secs}s`;
}

function LoginScreen({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(username, password);
      onLogin();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="login-page">
      <form className="login-card" onSubmit={submit}>
        <div className="brand-icon"><Activity size={28} /></div>
        <p className="eyebrow">QSR INTELLIGENCE PLATFORM</p>
        <h1>Welcome back</h1>
        <p className="muted">Your restaurant operations, at a glance.</p>
        <label>Username</label>
        <input value={username} onChange={e => setUsername(e.target.value)}
          placeholder="Enter username" autoComplete="username" required />
        <label>Password</label>
        <input type="password" value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Enter password" autoComplete="current-password" required />
        {error && <p className="error-message">{error}</p>}
        <button className="primary-button full-width" disabled={busy}>
          {busy ? "Signing in..." : "Sign in"}
        </button>
        <p className="login-footnote">Sign in with your registered QSR account.</p>
      </form>
    </main>
  );
}

function Metric({ icon, label, value, note, tone = "purple" }) {
  return (
    <article className="metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <div className={`metric-icon tone-${tone}`}>{icon}</div>
      </div>
      <strong className="metric-value">{value}</strong>
      <span className="metric-note">{note}</span>
    </article>
  );
}

function EmptyState({ icon, title, text }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <strong>{title}</strong>
      <p>{text}</p>
    </div>
  );
}

function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(getToken()));
  const [summary, setSummary] = useState(initialSummary);
  const [cameras, setCameras] = useState([]);
  const [queue, setQueue] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeNav, setActiveNav] = useState("dashboard");
  const [showCameraForm, setShowCameraForm] = useState(false);
  const [cameraName, setCameraName] = useState("");
  const [cameraLocation, setCameraLocation] = useState("");
  const [cameraType, setCameraType] = useState("video");
  const [cameraUri, setCameraUri] = useState("");

  const logout = useCallback(() => {
    clearToken();
    setAuthenticated(false);
    setSummary(initialSummary);
    setCameras([]);
    setQueue([]);
    setAlerts([]);
  }, []);

  const refreshData = useCallback(async () => {
    if (!getToken()) return;
    setLoading(true);
    setError("");
    try {
      const [me, dashboard, cameraData, queueData, alertData] =
        await Promise.all([
          apiRequest("/api/auth/me"),
          apiRequest("/api/dashboard/summary"),
          apiRequest("/api/cameras"),
          apiRequest("/api/queue/latest"),
          apiRequest("/api/alerts"),
        ]);
      if (!me) throw new Error("Authentication required");
      setSummary(dashboard);
      setCameras(cameraData);
      setQueue(queueData);
      setAlerts(alertData);
    } catch (err) {
      setError(err.message);
      if (/token|credentials|unauthorized/i.test(err.message)) logout();
    } finally {
      setLoading(false);
    }
  }, [logout]);

  useEffect(() => {
    if (authenticated) refreshData();
  }, [authenticated, refreshData]);

  async function addCamera(event) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest("/api/cameras", {
        method: "POST",
        body: JSON.stringify({
          name: cameraName,
          location: cameraLocation || null,
          source_type: cameraType,
          source_uri: cameraUri,
          is_active: true,
        }),
      });
      setCameraName("");
      setCameraLocation("");
      setCameraUri("");
      setShowCameraForm(false);
      await refreshData();
    } catch (err) {
      setError(err.message);
    }
  }

  async function acknowledgeAlert(id) {
    try {
      await apiRequest(`/api/alerts/${id}/acknowledge`, { method: "PATCH" });
      await refreshData();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!authenticated) {
    return <LoginScreen onLogin={() => setAuthenticated(true)} />;
  }

  const openAlerts = alerts.filter(a => !a.is_acknowledged);
  const maxQueue = Math.max(1, ...queue.slice(0, 12).map(q => q.queue_length));
  const latestQueue = [...queue].slice(0, 12).reverse();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon small"><Activity size={22} /></div>
          <div>
            <strong>QSR Vision</strong>
            <span>Queue intelligence</span>
          </div>
        </div>

        <p className="nav-heading">WORKSPACE</p>
        <a href="#dashboard"
          className={`nav-item ${activeNav === "dashboard" ? "active" : ""}`}
          onClick={() => setActiveNav("dashboard")}>
          <LayoutDashboard size={18} /> Dashboard
        </a>
        <a href="#cameras"
          className={`nav-item ${activeNav === "cameras" ? "active" : ""}`}
          onClick={() => setActiveNav("cameras")}>
          <Camera size={18} /> Cameras
        </a>
        <a href="#queue"
          className={`nav-item ${activeNav === "queue" ? "active" : ""}`}
          onClick={() => setActiveNav("queue")}>
          <Users size={18} /> Queue monitoring
        </a>
        <a href="#alerts"
          className={`nav-item ${activeNav === "alerts" ? "active" : ""}`}
          onClick={() => setActiveNav("alerts")}>
          <AlertTriangle size={18} /> Alerts
          {openAlerts.length > 0 && <span className="nav-count">{openAlerts.length}</span>}
        </a>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot" />
            <div><strong>Backend connected</strong><span>API session active</span></div>
          </div>
          <button className="nav-item logout-button" onClick={logout}>
            <LogOut size={18} /> Sign out
          </button>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div>
            <p className="eyebrow">RESTAURANT OPERATIONS / OVERVIEW</p>
            <h1>Queue dashboard</h1>
            <p className="muted">Monitor customer flow, cameras and waiting times.</p>
          </div>
          <button className="secondary-button" onClick={refreshData} disabled={loading}>
            <RefreshCw size={16} className={loading ? "spin" : ""} />
            {loading ? "Refreshing..." : "Refresh data"}
          </button>
        </header>

        {error && (
          <div className="error-banner">
            <AlertTriangle size={18} />
            <span>{error}</span>
            <button onClick={() => setError("")} aria-label="Dismiss error"><X size={16} /></button>
          </div>
        )}

        <section className="welcome-strip">
          <div>
            <span className="welcome-label">LIVE OPERATIONS</span>
            <h2>Your queue overview</h2>
            <p>Review current activity across your registered camera sources.</p>
          </div>
          <div className="welcome-graphic"><Activity size={66} /></div>
        </section>

        <section className="metric-grid">
          <Metric icon={<Camera />} label="Total cameras"
            value={summary.total_cameras} note={`${summary.active_cameras} currently active`} tone="purple" />
          <Metric icon={<Users />} label="Customers detected"
            value={summary.latest_customer_count} note="Latest recorded result" tone="blue" />
          <Metric icon={<TrendingUp />} label="Queue length"
            value={summary.latest_queue_length} note="Latest recorded result" tone="orange" />
          <Metric icon={<Clock3 />} label="Estimated wait"
            value={formatWait(summary.latest_wait_seconds)} note="Latest recorded result" tone="green" />
        </section>

        <div className="content-grid">
          <section className="panel" id="queue">
            <div className="panel-header">
              <div><h2>Queue activity</h2><p>Recent recorded queue lengths</p></div>
              <span className="count-badge">{queue.length} records</span>
            </div>
            {latestQueue.length === 0 ? (
              <EmptyState icon={<Activity />} title="Waiting for analytics data"
                text="Queue activity appears here when records are sent to the API." />
            ) : (
              <div className="activity-chart">
                <div className="chart-guide"><span>Queue size</span><span>Recent records</span></div>
                <div className="bar-chart">
                  {latestQueue.map((item, index) => (
                    <div className="bar-column" key={item.id} title={`Queue: ${item.queue_length}`}>
                      <span className="bar-value">{item.queue_length}</span>
                      <div className="bar-track">
                        <div className="bar-fill"
                          style={{ height: `${Math.max(5, item.queue_length / maxQueue * 100)}%` }} />
                      </div>
                      <span className="bar-label">{index + 1}</span>
                    </div>
                  ))}
                </div>
                <div className="chart-legend"><span className="legend-dot" /> Queue length per record</div>
              </div>
            )}
          </section>

          <section className="panel" id="alerts">
            <div className="panel-header">
              <div><h2>Recent alerts</h2><p>Queue and wait-time notifications</p></div>
              <span className="count-badge">{openAlerts.length} open</span>
            </div>
            {alerts.length === 0 ? (
              <EmptyState icon={<ShieldCheck />} title="All quiet for now"
                text="Alerts will appear when queue records cross configured thresholds." />
            ) : (
              <div className="alert-list">
                {alerts.slice(0, 6).map(alert => (
                  <div className="alert-row" key={alert.id}>
                    <div className="alert-icon"><AlertTriangle size={18} /></div>
                    <div className="row-main">
                      <strong>{alert.alert_type.replace(/_/g, " ")}</strong>
                      <span>{alert.message}</span>
                      <small>{new Date(alert.created_at).toLocaleString()}</small>
                    </div>
                    {!alert.is_acknowledged && (
                      <button className="icon-button" title="Acknowledge alert"
                        onClick={() => acknowledgeAlert(alert.id)}>
                        <CheckCircle2 size={18} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        <section className="panel queue-panel" id="cameras">
          <div className="panel-header">
            <div><h2>Camera sources</h2><p>Manage registered video and camera feeds</p></div>
            <button className="primary-button compact"
              onClick={() => setShowCameraForm(!showCameraForm)}>
              <Plus size={16} /> Add camera
            </button>
          </div>

          {showCameraForm && (
            <form className="camera-form" onSubmit={addCamera}>
              <label>Camera name</label>
              <input value={cameraName} onChange={e => setCameraName(e.target.value)}
                required placeholder="Front counter" />
              <label>Location</label>
              <input value={cameraLocation} onChange={e => setCameraLocation(e.target.value)}
                placeholder="Restaurant branch" />
              <label>Source type</label>
              <select value={cameraType} onChange={e => setCameraType(e.target.value)}>
                <option value="video">Video file</option>
                <option value="rtsp">RTSP stream</option>
                <option value="webcam">Webcam</option>
              </select>
              <label>Source URI</label>
              <input value={cameraUri} onChange={e => setCameraUri(e.target.value)}
                required placeholder="C:/videos/sample.mp4 or rtsp://..." />
              <div className="form-actions">
                <button type="button" className="secondary-button"
                  onClick={() => setShowCameraForm(false)}>Cancel</button>
                <button className="primary-button">Save camera</button>
              </div>
            </form>
          )}

          {cameras.length === 0 ? (
            <EmptyState icon={<Video />} title="No cameras registered"
              text="Add a camera source to start managing your restaurant feeds." />
          ) : (
            <div className="camera-list">
              {cameras.map(camera => (
                <div className="camera-row" key={camera.id}>
                  <div className="camera-avatar"><Camera size={20} /></div>
                  <div className="row-main">
                    <strong>{camera.name}</strong>
                    <span><MapPin size={12} /> {camera.location || "Location not specified"} · {camera.source_type}</span>
                    <small>Camera ID: CAM-{String(camera.id).padStart(3, "0")}</small>
                  </div>
                  <span className={`pill ${camera.is_active ? "pill-green" : "pill-gray"}`}>
                    {camera.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel queue-panel">
          <div className="panel-header">
            <div><h2>Latest queue records</h2><p>Recent analytics data received by the backend</p></div>
            <span className="count-badge">{queue.length} records</span>
          </div>
          {queue.length === 0 ? (
            <EmptyState icon={<Users />} title="No queue records yet"
              text="Records will appear after an analytics source sends data to the API." />
          ) : (
            <div className="table-scroll">
              <table>
                <thead><tr><th>Camera</th><th>Customers</th><th>Queue length</th><th>Estimated wait</th><th>FPS</th><th>Recorded at</th></tr></thead>
                <tbody>
                  {queue.map(item => (
                    <tr key={item.id}>
                      <td>CAM-{String(item.camera_id).padStart(3, "0")}</td>
                      <td>{item.customer_count}</td>
                      <td>{item.queue_length}</td>
                      <td>{formatWait(item.estimated_wait_seconds)}</td>
                      <td>{item.fps ?? "—"}</td>
                      <td>{new Date(item.recorded_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className="footer">
          <span>QSR Vision · Queue Management</span>
          <span>Analytics pipeline status depends on your configured source.</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
