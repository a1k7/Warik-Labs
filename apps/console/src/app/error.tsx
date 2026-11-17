"use client";

import { useEffect } from "react";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Keep the error local to the browser UI; never log secrets or request payloads.
    console.error("Console rendering error", { digest: error.digest });
  }, [error]);

  return (
    <main className="not-found">
      <span className="eyebrow">WORKSPACE ERROR</span>
      <h1>We hit a problem.</h1>
      <p>The page failed to render. No external action was performed.</p>
      <button className="retry-button" onClick={() => reset()}>Try again</button>
    </main>
  );
}
