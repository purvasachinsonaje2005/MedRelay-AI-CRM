import { useState } from "react";

export default function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error(err);
      alert("Backend connection failed");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f172a] via-[#111827] to-[#1e3a8a] text-white flex overflow-hidden">
      
      {/* SIDEBAR */}
      <div className="w-72 bg-white/10 backdrop-blur-xl border-r border-white/10 p-6 flex flex-col justify-between">
        
        <div>
          {/* Logo */}
          <div className="flex items-center gap-4 mb-10">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-cyan-400 to-blue-600 flex items-center justify-center text-2xl font-bold shadow-lg shadow-blue-500/40">
              M
            </div>

            <div>
              <h1 className="text-3xl font-bold tracking-wide">
                MedRelay
              </h1>

              <p className="text-gray-300 text-sm">
                AI Pharma CRM
              </p>
            </div>
          </div>

          {/* Nav */}
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-5 rounded-3xl shadow-xl cursor-pointer hover:scale-105 transition duration-300">
              <h2 className="font-bold text-lg">
                Dashboard
              </h2>

              <p className="text-sm text-blue-100 mt-1">
                AI interaction management
              </p>
            </div>

            <div className="bg-white/5 hover:bg-white/10 transition p-5 rounded-3xl cursor-pointer border border-white/5">
              <h2 className="font-semibold">
                History
              </h2>
            </div>

            <div className="bg-white/5 hover:bg-white/10 transition p-5 rounded-3xl cursor-pointer border border-white/5">
              <h2 className="font-semibold">
                Follow-Ups
              </h2>
            </div>

            <div className="bg-white/5 hover:bg-white/10 transition p-5 rounded-3xl cursor-pointer border border-white/5">
              <h2 className="font-semibold">
                Analytics
              </h2>
            </div>
          </div>
        </div>

        {/* Bottom Card */}
        <div className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 p-5 rounded-3xl border border-cyan-400/20 backdrop-blur-xl">
          <p className="text-sm text-gray-200">
            Powered by FastAPI, LangGraph & Groq AI
          </p>
        </div>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-8 overflow-auto">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-5xl font-bold leading-tight">
              AI Interaction
              <br />
              Dashboard
            </h1>

            <p className="text-gray-300 mt-3 text-lg">
              Smart healthcare professional engagement system
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-xl px-6 py-4 rounded-3xl border border-white/10 shadow-xl">
            <p className="text-sm text-cyan-300 font-semibold">
              ● Live AI Connected
            </p>
          </div>
        </div>

        {/* GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* INPUT CARD */}
          <div className="bg-white/10 backdrop-blur-2xl rounded-[35px] p-8 border border-white/10 shadow-2xl">
            
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold">
                Log Interaction
              </h2>

              <div className="bg-cyan-500/20 text-cyan-300 px-4 py-2 rounded-full text-sm">
                AI Enabled
              </div>
            </div>

            <textarea
              className="w-full h-80 bg-black/20 border border-white/10 rounded-3xl p-6 text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-400 transition"
              placeholder="Describe your doctor interaction..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <button
              onClick={sendMessage}
              disabled={loading}
              className="w-full mt-6 bg-gradient-to-r from-cyan-400 to-blue-600 hover:scale-[1.02] transition duration-300 text-white py-5 rounded-3xl text-lg font-bold shadow-2xl shadow-blue-500/40"
            >
              {loading ? "Processing..." : "Send to AI"}
            </button>

            {/* EXAMPLE */}
            <div className="mt-6 bg-black/20 border border-white/10 rounded-3xl p-5">
              <h3 className="font-semibold text-cyan-300 mb-2">
                Example Prompt
              </h3>

              <p className="text-gray-300 text-sm leading-7">
                Met Dr Sharma at Ruby Hall Clinic. Interested in oncology drug samples. Follow up next Tuesday.
              </p>
            </div>
          </div>

          {/* RESPONSE */}
          <div className="bg-white/10 backdrop-blur-2xl rounded-[35px] p-8 border border-white/10 shadow-2xl">

            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold">
                AI Response
              </h2>

              <div className="bg-green-500/20 text-green-300 px-4 py-2 rounded-full text-sm">
                ● Active
              </div>
            </div>

            {!response ? (
              <div className="h-[700px] flex items-center justify-center border border-dashed border-white/20 rounded-3xl text-gray-400 text-lg">
                AI output appears here
              </div>
            ) : (
              <div className="space-y-6 max-h-[750px] overflow-auto pr-2">

                {/* Reply */}
                <div className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-400/20 rounded-3xl p-6">
                  <h3 className="text-cyan-300 font-bold mb-3 text-xl">
                    AI Reply
                  </h3>

                  <p className="text-gray-200 whitespace-pre-wrap leading-8">
                    {response.reply}
                  </p>
                </div>

                {/* Summary */}
                {response.summary && (
                  <div className="bg-black/20 rounded-3xl p-6 border border-white/10">
                    <h3 className="font-bold text-xl mb-3">
                      Summary
                    </h3>

                    <p className="text-gray-300 leading-7">
                      {response.summary}
                    </p>
                  </div>
                )}

                {/* Recommendations */}
                {response.recommendations?.length > 0 && (
                  <div className="bg-black/20 rounded-3xl p-6 border border-white/10">
                    <h3 className="font-bold text-xl mb-4">
                      Recommendations
                    </h3>

                    <div className="space-y-3">
                      {response.recommendations.map((rec, index) => (
                        <div
                          key={index}
                          className="bg-white/5 hover:bg-white/10 transition p-4 rounded-2xl border border-white/5"
                        >
                          {rec}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tool Calls */}
                {response.tool_calls?.length > 0 && (
                  <div className="bg-black/20 rounded-3xl p-6 border border-white/10">
                    <h3 className="font-bold text-xl mb-4">
                      Tool Calls
                    </h3>

                    <div className="flex flex-wrap gap-3">
                      {response.tool_calls.map((tool, index) => (
                        <div
                          key={index}
                          className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 px-4 py-2 rounded-full border border-cyan-400/20"
                        >
                          {tool}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Draft */}
                {response.draft &&
                  Object.keys(response.draft).length > 0 && (
                    <div className="bg-black/20 rounded-3xl p-6 border border-white/10">
                      <h3 className="font-bold text-xl mb-4">
                        Extracted Information
                      </h3>

                      <div className="space-y-3">
                        {Object.entries(response.draft).map(([key, value]) => (
                          <div
                            key={key}
                            className="flex justify-between bg-white/5 p-4 rounded-2xl border border-white/5"
                          >
                            <span className="capitalize text-gray-300">
                              {key.replaceAll("_", " ")}
                            </span>

                            <span className="font-semibold text-cyan-300">
                              {String(value)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                {/* Saved */}
                {response.interaction_id && (
                  <div className="bg-green-500/10 border border-green-400/20 rounded-3xl p-6">
                    <h3 className="font-bold text-green-300 text-xl">
                      Interaction Saved Successfully
                    </h3>

                    <p className="mt-2 text-gray-300">
                      Interaction ID: {response.interaction_id}
                    </p>
                  </div>
                )}

              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}