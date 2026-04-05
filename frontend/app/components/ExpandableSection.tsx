"use client";
import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

export function ExpandableSection({ title, children }: { title: string, children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div style={{ marginBottom: "1rem", border: "1px solid var(--border)", borderRadius: "12px", background: "var(--panel)", overflow: "hidden" }}>
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        style={{ width: "100%", padding: "1.5rem", display: "flex", justifyContent: "space-between", alignItems: "center", background: "transparent", border: "none", cursor: "pointer", color: "var(--text)" }}
      >
        <h2 style={{ margin: 0, fontSize: "1.25rem", color: "#fe70d7", fontWeight: 600 }}>{title}</h2>
        {isOpen ? <ChevronUp size={24} color="#fe70d7" /> : <ChevronDown size={24} color="#fe70d7" />}
      </button>
      {isOpen && (
        <div style={{ padding: "0 1.5rem 1.5rem 1.5rem", color: "var(--text)" }}>
          {children}
        </div>
      )}
    </div>
  );
}
