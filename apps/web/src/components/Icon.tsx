const paths: Record<string, string> = {
  home: 'M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z',
  'book-open': 'M12 6c-2-1.5-5-2-9-2v14c4 0 7 .5 9 2 2-1.5 5-2 9-2V4c-4 0-7 .5-9 2zm0 0v14',
  'clipboard-list': 'M9 4h6v3H9zM7 6H5v15h14V6h-2M9 12h6M9 16h6',
  puzzle: 'M10 4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4h-4a2 2 0 1 1-4 0H6v-4a2 2 0 1 1 0-4V4z',
  activity: 'M3 12h4l3-8 4 16 3-8h4',
  bell: 'M6 16V11a6 6 0 0 1 12 0v5l2 2H4zm4 4a2 2 0 0 0 4 0',
  logout: 'M10 4H5v16h5M14 8l4 4-4 4M18 12H9',
  users: 'M16 20v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M21 20v-1a4 4 0 0 0-3-3.9M15 4.1a3.5 3.5 0 0 1 0 6.8',
  plus: 'M12 5v14M5 12h14',
  check: 'M5 12l5 5L20 7',
  alert: 'M12 3 2 21h20zM12 10v5m0 3h.01',
};

export function Icon({ name, className = 'h-4.5 w-4.5', size = 18 }: { name: string; className?: string; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75"
      strokeLinecap="round" strokeLinejoin="round" className={className} aria-hidden>
      <path d={paths[name] ?? paths.puzzle} />
    </svg>
  );
}
