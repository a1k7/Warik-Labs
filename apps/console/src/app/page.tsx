"use client";

import Link from "next/link";
import {
  ArrowDown,
  ArrowUpRight,
  AudioLines,
  Check,
  Clock3,
  Command,
  Compass,
  FileSearch,
  Gift,
  MessageSquare,
  Plus,
  Send,
  ShieldCheck,
  Sparkles,
  WandSparkles,
  Zap,
} from "lucide-react";
import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";

const API_BASE = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1").replace(/\/$/, "");

type MissionStep = {
  id: string;
  title: string;
  description: string;
  state: "ready" | "needs_input" | "blocked";
  action_class: "read_only" | "reversible" | "irreversible" | "none";
};

type Mission = {
  id: string;
  title: string;
  objective: string;
  intent: string;
  state: "draft" | "needs_input" | "waiting_approval" | "not_executable";
  steps: MissionStep[];
  missing_information: string[];
  capabilities_used: string[];
  execution_note: string;
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  mission?: Mission | null;
  provider?: "groq" | "local";
  provider_status?: "connected" | "fallback" | "not_configured";
  timestamp: number;
};

const starters = [
  { icon: Compass, title: "Plan a trip", prompt: "Plan a 3-day trip from Bhopal to Goa next weekend within ₹12,000." },
  { icon: Gift, title: "Sort my groceries", prompt: "I need 2 litres of milk, eggs and vegetables from Blinkit. Help me prepare the order." },
  { icon: Clock3, title: "Stay on top of things", prompt: "Remind me to follow up on my pending refund tomorrow." },
  { icon: FileSearch, title: "Think something through", prompt: "Help me compare the best options for a student-friendly laptop under ₹60,000." },
];

const initialMessage: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content: "Hey, I'm Warik. Think of me as the companion who helps you move things forward — not just answer questions. Tell me what you're trying to do, even in Hinglish. I'll understand the goal, work out the next steps, and keep you in control before anything consequential happens.",
  timestamp: Date.now(),
};

function renderAssistantText(content: string) {
  return content.split(/(\\*\\*[^*]+\\*\\*)/g).map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

function timeLabel(timestamp: number) {
  return new Date(timestamp).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
}

function MissionCard({ mission }: { mission: Mission }) {
  const status = mission.state === "needs_input"
    ? { label: "Needs your input", className: "needs-input" }
    : mission.state === "not_executable"
      ? { label: "Plan prepared · Execution unavailable", className: "blocked" }
      : mission.state === "waiting_approval"
        ? { label: "Waiting for approval", className: "needs-input" }
        : { label: "Draft plan", className: "draft" };

  return (
    <section className="mission-card">
      <div className="mission-card-top">
        <div className="mission-card-icon"><WandSparkles size={16} /></div>
        <span className={`mission-state ${status.className}`}>{status.label}</span>
      </div>
      <h3>{mission.title}</h3>
      <p className="mission-objective">{mission.objective}</p>
      <div className="mission-steps">
        {mission.steps.map((step, index) => (
          <div className="mission-step" key={step.id}>
            <div className={`step-marker ${step.state}`}>{step.state === "ready" ? <Check size={12} /> : index + 1}</div>
            <div className="step-copy">
              <strong>{step.title}</strong>
              <span>{step.description}</span>
            </div>
            <span className={`step-status ${step.state}`}>
              {step.state === "ready" ? "Ready" : step.state === "needs_input" ? "Input" : "Blocked"}
            </span>
          </div>
        ))}
      </div>
      {mission.missing_information.length > 0 && (
        <div className="missing-box">
          <strong>To move forward</strong>
          <span>{mission.missing_information.join(" · ")}</span>
        </div>
      )}
      <div className="mission-foot"><ShieldCheck size={13} /><span>{mission.execution_note}</span></div>
    </section>
  );
}

export default function HomePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [apiState, setApiState] = useState<"checking" | "online" | "offline">("checking");
  const [showScroll, setShowScroll] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    try {
      const saved = localStorage.getItem("warik-companion-session-v1");
      if (saved) {
        const parsed = JSON.parse(saved) as ChatMessage[];
        if (Array.isArray(parsed) && parsed.length) setMessages(parsed);
      }
    } catch {
      localStorage.removeItem("warik-companion-session-v1");
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("warik-companion-session-v1", JSON.stringify(messages.slice(-60)));
  }, [messages]);

  useEffect(() => {
    fetch(`${API_BASE}/health/live`, { cache: "no-store" })
      .then((response) => setApiState(response.ok ? "online" : "offline"))
      .catch(() => setApiState("offline"));
  }, []);

  useEffect(() => {
    if (!scrollRef.current) return;
    scrollRef.current.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, sending]);

  const submit = async (event?: FormEvent, preset?: string) => {
    event?.preventDefault();
    const message = (preset ?? input).trim();
    if (!message || sending) return;
    const history = messages.slice(-10).map((item) => ({ role: item.role, content: item.content }));
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(), role: "user", content: message, timestamp: Date.now(),
    };
    setMessages((current) => [...current, userMessage]);
    setInput("");
    setSending(true);
    if (inputRef.current) inputRef.current.style.height = "auto";

    try {
      const response = await fetch(`${API_BASE}/companion/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Companion request failed (${response.status})`);
      }
      const data = await response.json();
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.reply,
        mission: data.mission,
        provider: data.provider,
        provider_status: data.provider_status,
        timestamp: Date.now(),
      };
      setMessages((current) => [...current, assistantMessage]);
      setApiState("online");
    } catch (error) {
      setApiState("offline");
      setMessages((current) => [...current, {
        id: crypto.randomUUID(),
        role: "assistant",
        content: error instanceof Error
          ? `I couldn't reach my reasoning service. ${error.message}. Your message is still here; check that the FastAPI server is running and try again.`
          : "I couldn't reach the API. Check the backend and try again.",
        timestamp: Date.now(),
        provider: "local",
        provider_status: "fallback",
      }]);
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void submit();
    }
  };

  const newChat = () => {
    setMessages([{ ...initialMessage, id: crypto.randomUUID(), timestamp: Date.now() }]);
    inputRef.current?.focus();
  };

  return (
    <main className="companion-shell">
      <aside className="companion-sidebar">
        <Link className="brand-lockup" href="/" aria-label="Warik home">
          <div className="brand-symbol">w<span>.</span></div>
          <div><strong>warik<span> labs</span></strong><small>PERSONAL COMPANION</small></div>
        </Link>

        <button className="new-chat-button" onClick={newChat}><Plus size={16} /> New conversation</button>

        <div className="side-section-label">YOUR SPACE</div>
        <nav className="side-nav">
          <a className="side-link active" href="#companion"><MessageSquare size={17} /><span>Companion</span><span className="nav-live-dot" /></a>
          <div className="side-link unavailable"><Command size={17} /><span>Missions</span><small>SOON</small></div>
          <div className="side-link unavailable"><ShieldCheck size={17} /><span>Approvals</span><small>SOON</small></div>
          <div className="side-link unavailable"><DatabaseIcon /><span>Memory</span><small>SOON</small></div>
        </nav>

        <div className="side-section-label integrations-label">CONNECTED WORLD</div>
        <div className="integration-item"><span className="integration-icon whatsapp">◉</span><span>WhatsApp</span><em>Not linked</em></div>
        <div className="integration-item"><span className="integration-icon web">⌘</span><span>Web access</span><em>Not linked</em></div>

        <div className="sidebar-spacer" />
        <div className="privacy-card">
          <ShieldCheck size={16} />
          <strong>Your control comes first.</strong>
          <p>Warik plans before it acts. Consequential actions need your permission.</p>
        </div>
        <div className="profile-row"><div className="profile-avatar">A</div><div><strong>Personal workspace</strong><span>Local development</span></div><span className="profile-menu">···</span></div>
      </aside>

      <section className="companion-main" id="companion">
        <header className="companion-topbar">
          <div className="mobile-brand"><span className="brand-symbol">w<span>.</span></span> warik</div>
          <div className="topbar-context"><span className="context-dot" /> Your personal companion <span className="context-divider">/</span> <span className="context-muted">Private workspace</span></div>
          <div className="topbar-actions">
            <div className={`api-indicator ${apiState}`}><span />{apiState === "online" ? "System online" : apiState === "offline" ? "API offline" : "Connecting"}</div>
            <button className="topbar-icon" title="Start a new conversation" onClick={newChat}><Plus size={17} /></button>
          </div>
        </header>

        <div className="conversation" ref={scrollRef} onScroll={(event) => {
          const element = event.currentTarget;
          setShowScroll(element.scrollHeight - element.scrollTop - element.clientHeight > 180);
        }}>
          <div className="conversation-inner">
            <div className="date-divider"><span /> TODAY <span /></div>

            {messages.length === 1 && (
              <section className="welcome-block">
                <div className="welcome-orb"><div className="orb-ring ring-a" /><div className="orb-ring ring-b" /><div className="orb-letter">w<span>.</span></div><Sparkles className="orb-spark" size={17} /></div>
                <div className="welcome-overline"><span className="welcome-line" /> A LITTLE MORE HUMAN. A LOT MORE HELPFUL.</div>
                <h1>Good things happen<br />when <em>everything clicks.</em></h1>
                <p>Tell me what&apos;s on your mind. I&apos;ll help connect the dots, make a plan, and keep the little things from slipping through.</p>
                <div className="starter-grid">
                  {starters.map((starter) => {
                    const Icon = starter.icon;
                    return <button className="starter-card" key={starter.title} onClick={() => void submit(undefined, starter.prompt)}>
                      <span className="starter-icon"><Icon size={17} /></span><span><strong>{starter.title}</strong><small>{starter.prompt}</small></span><ArrowUpRight className="starter-arrow" size={15} />
                    </button>;
                  })}
                </div>
              </section>
            )}

            {messages.map((message) => (
              <article className={`chat-row ${message.role}`} key={message.id}>
                {message.role === "assistant" ? <div className="assistant-avatar">w<span>.</span></div> : <div className="user-avatar">A</div>}
                <div className="chat-content">
                  <div className="chat-meta">
                    <strong>{message.role === "assistant" ? "Warik" : "You"}</strong>
                    <time>{timeLabel(message.timestamp)}</time>
                    {message.role === "assistant" && message.provider === "groq" && <span className="reasoning-chip"><Sparkles size={10} /> GROQ REASONING</span>}
                    {message.role === "assistant" && message.provider_status === "not_configured" && <span className="reasoning-chip local-chip">LOCAL MODE</span>}
                  </div>
                  <div className="message-text">{message.role === "assistant" ? renderAssistantText(message.content) : message.content}</div>
                  {message.mission && <MissionCard mission={message.mission} />}
                </div>
              </article>
            ))}

            {sending && (
              <article className="chat-row assistant">
                <div className="assistant-avatar">w<span>.</span></div>
                <div className="chat-content">
                  <div className="chat-meta"><strong>Warik</strong><span className="thinking-label">THINKING THROUGH IT</span></div>
                  <div className="thinking-bubble"><span /><span /><span /></div>
                </div>
              </article>
            )}

            {messages.length > 1 && !sending && (
              <div className="followup-prompts">
                <span>KEEP GOING</span>
                <button onClick={() => setInput("Make the plan more specific")}>Make it more specific <ArrowUpRight size={12} /></button>
                <button onClick={() => setInput("What do you need from me next?")}>What&apos;s next? <ArrowUpRight size={12} /></button>
              </div>
            )}
          </div>
        </div>

        {showScroll && <button className="scroll-bottom" onClick={() => scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" })}><ArrowDown size={15} /></button>}

        <div className="composer-wrap">
          <form className="composer" onSubmit={(event) => void submit(event)}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) => {
                setInput(event.target.value);
                event.target.style.height = "auto";
                event.target.style.height = `${Math.min(event.target.scrollHeight, 150)}px`;
              }}
              onKeyDown={handleKeyDown}
              placeholder="Tell Warik what's on your mind..."
              rows={1}
              maxLength={4000}
              disabled={sending}
              aria-label="Message Warik"
            />
            <div className="composer-bottom">
              <div className="composer-tools"><span className="composer-hint"><span className="keycap">↵</span> to send <span className="hint-separator">·</span> shift + enter for new line</span></div>
              <div className="composer-right"><span className="character-count">{input.length > 0 ? `${input.length}/4000` : " "}</span><button className="send-button" type="submit" disabled={!input.trim() || sending} aria-label="Send message">{sending ? <AudioLines size={16} /> : <Send size={16} />}</button></div>
            </div>
          </form>
          <div className="composer-disclaimer"><ShieldCheck size={12} /> Warik can plan and reason. External actions remain disabled until connected and approved.</div>
        </div>

        <footer className="companion-footer"><span>WARIK LABS</span><span><Zap size={11} /> BUILT FOR FOLLOW-THROUGH</span><span>English · Hinglish · India</span></footer>
      </section>
    </main>
  );
}

function DatabaseIcon() {
  return <span className="database-icon">▤</span>;
}
