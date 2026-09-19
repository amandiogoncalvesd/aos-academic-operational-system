export function Logo({ size = 28 }: { size?: number }) {
  return (
    <span className="inline-flex items-center gap-2.5">
      <svg width={size} height={size} viewBox="0 0 32 32" aria-hidden>
        <rect width="32" height="32" rx="7" fill="#0F172A" />
        <path d="M9 22 16 9l7 13" stroke="#fff" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        <circle cx="16" cy="22" r="2" fill="#F59E0B" />
      </svg>
      <span className="font-display text-lg font-semibold tracking-tight">AOS</span>
    </span>
  );
}
