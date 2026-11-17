import Link from "next/link";

export default function NotFound() {
  return (
    <main className="not-found">
      <span className="eyebrow">404 · NOT FOUND</span>
      <h1>This mission does not exist.</h1>
      <p>The requested workspace route is not part of this Phase 1 scaffold.</p>
      <Link href="/">Return to Mission Control</Link>
    </main>
  );
}
