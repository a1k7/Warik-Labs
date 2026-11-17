import {
  Activity,
  ArrowUpRight,
  Bot,
  CheckCircle2,
  CircleDashed,
  Clock3,
  Database,
  MessageCircle,
  ShieldCheck,
  Workflow,
} from "lucide-react";

const metrics = [
  { label: "Active missions", value: "0", note: "No tasks have been run", icon: Workflow },
  { label: "Awaiting approval", value: "0", note: "Nothing needs your decision", icon: ShieldCheck },
  { label: "Actions today", value: "0", note: "Execution is disabled in Phase 1", icon: Activity },
  { label: "Verified outcomes", value: "0", note: "No outcome receipts yet", icon: CheckCircle2 },
];

const foundations = [
  { label: "API service", detail: "FastAPI scaffold", state: "Ready", icon: Bot },
  { label: "Database", detail: "PostgreSQL schema + migrations", state: "Ready", icon: Database },
  { label: "Queue", detail: "Redis local service", state: "Ready", icon: CircleDashed },
  { label: "WhatsApp channel", detail: "Cloud API not connected", state: "Not connected", icon: MessageCircle },
];

export default function HomePage() {
  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">W</div>
          <div>
            <strong>WARIK<span> LABS</span></strong>
            <small>MISSION CONTROL</small>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>
        <nav className="nav-list" aria-label="Main navigation">
          <a className="nav-item active" href="#overview"><Activity size={17} /> Overview</a>
          <a className="nav-item disabled" href="#missions"><Workflow size={17} /> Missions <span>0</span></a>
          <a className="nav-item disabled" href="#approvals"><ShieldCheck size={17} /> Approvals <span>0</span></a>
          <a className="nav-item disabled" href="#memory"><Database size={17} /> Memory</a>
          <a className="nav-item disabled" href="#integrations"><MessageCircle size={17} /> Integrations</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="environment"><span className="status-dot" /> LOCAL DEVELOPMENT</div>
          <div className="user-chip"><div className="avatar">WL</div><div><strong>Workspace owner</strong><small>Administrator</small></div></div>
        </div>
      </aside>

      <section className="content" id="overview">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> Overview</div>
          <div className="topbar-right"><span className="build-label">PHASE 1 · FOUNDATION</span><div className="avatar small">WL</div></div>
        </header>

        <div className="page">
          <div className="hero">
            <div>
              <div className="eyebrow"><span className="status-dot" /> SYSTEM FOUNDATION</div>
              <h1>Your work, <em>in motion.</em></h1>
              <p>One place to see what Warik is working on, what needs your permission, and what has actually been completed.</p>
            </div>
            <div className="hero-art"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="orb-core">W</div><div className="orbit-caption">PERSONAL EXECUTION SYSTEM</div></div>
          </div>

          <div className="section-heading"><div><span className="eyebrow">LIVE OPERATIONS</span><h2>Workspace pulse</h2></div><span className="muted">No live activity yet</span></div>
          <div className="metric-grid">
            {metrics.map((metric) => {
              const Icon = metric.icon;
              return <article className="metric-card" key={metric.label}><div className="metric-top"><span>{metric.label}</span><Icon size={17} /></div><strong>{metric.value}</strong><small>{metric.note}</small></article>;
            })}
          </div>

          <div className="lower-grid">
            <section className="panel">
              <div className="panel-heading"><div><span className="eyebrow">RUNTIME</span><h2>System foundations</h2></div><span className="tiny-status">LOCAL</span></div>
              <div className="foundation-list">
                {foundations.map((item) => {
                  const Icon = item.icon;
                  const ready = item.state === "Ready";
                  return <div className="foundation-row" key={item.label}><div className="foundation-icon"><Icon size={17} /></div><div className="foundation-copy"><strong>{item.label}</strong><small>{item.detail}</small></div><span className={ready ? "state ready" : "state idle"}>{item.state}</span></div>;
                })}
              </div>
            </section>

            <section className="panel next-panel">
              <span className="eyebrow">NEXT MILESTONE</span>
              <div className="milestone-icon"><Clock3 size={20} /></div>
              <h2>Connect the first channel</h2>
              <p>WhatsApp is the primary user interface. The webhook adapter will be added after the task model and approval gate are in place.</p>
              <a className="text-link" href="https://developers.facebook.com/documentation/business-messaging/whatsapp/" target="_blank" rel="noreferrer">WhatsApp Cloud API docs <ArrowUpRight size={15} /></a>
              <div className="progress-track"><span /></div>
              <small className="muted">Foundation phase · 1 of 7 milestones started</small>
            </section>
          </div>

          <footer className="footer"><span>WARIK LABS · BUILT FOR FOLLOW-THROUGH</span><span>Payments disabled · External actions disabled</span></footer>
        </div>
      </section>
    </main>
  );
}
