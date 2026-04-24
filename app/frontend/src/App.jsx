import { useEffect, useMemo, useState } from "react";

const defaultBackendUrl = "http://localhost:3001";

const systemSeed = {
  role: "assistant",
  content: "Salut, je suis ton assistant financier TechCorp. Pose-moi une question business, budget ou investissement.",
};

export default function App() {
  const backendUrl = defaultBackendUrl;
  const temperature = 0.7;
  const topP = 0.9;
  const numPredict = 256;

  const [status, setStatus] = useState({ connected: false, label: "Not checked" });
  const [messages, setMessages] = useState([systemSeed]);
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const visibleMessages = useMemo(() => messages.filter((msg) => msg !== systemSeed), [messages]);

  const checkStatus = async () => {
    try {
      const res = await fetch(`${backendUrl}/api/status`);
      const data = await res.json();
      setStatus({
        connected: Boolean(data.connected),
        label: data.connected ? "Connected" : data.error || "Disconnected",
      });
    } catch (err) {
      setStatus({ connected: false, label: err.message || "Disconnected" });
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const sendMessage = async (event) => {
    event.preventDefault();
    const text = prompt.trim();
    if (!text || isLoading) return;

    const userMsg = { role: "user", content: text };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setPrompt("");
    setIsLoading(true);

    try {
      const res = await fetch(`${backendUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: nextMessages,
          temperature,
          top_p: topP,
          num_predict: numPredict,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Chat request failed");
      }

      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
      setStatus({ connected: true, label: "Connected" });
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Erreur: ${err.message || "network error"}` }]);
      setStatus({ connected: false, label: err.message || "Disconnected" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <div className="title-row">
          <h1>TechCorp Financial Assistant</h1>
          <span className={`status-pill ${status.connected ? "online" : "offline"}`}>{status.connected ? "Connected" : "Disconnected"}</span>
        </div>
      </header>

      <main className="layout">
        <section className="chat-shell">
          <div className="chat-toolbar">
            <button type="button" className="ghost" onClick={checkStatus}>
              Check server status
            </button>
            <button type="button" className="ghost" onClick={() => setMessages([systemSeed])}>
              Clear history
            </button>
          </div>

          <div className="chat-list">
            {visibleMessages.length === 0 && <div className="empty">Start with a financial prompt to test the model in real time.</div>}

            {visibleMessages.map((msg, index) => (
              <article key={`${msg.role}-${index}`} className={`bubble ${msg.role === "user" ? "user" : "assistant"}`}>
                <p>{msg.content}</p>
              </article>
            ))}

            {isLoading && <div className="typing">Assistant is generating an answer...</div>}
          </div>

          <form className="composer" onSubmit={sendMessage}>
            <input placeholder="Ask a financial question" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            <button type="submit" disabled={isLoading || !prompt.trim()}>
              Send
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
