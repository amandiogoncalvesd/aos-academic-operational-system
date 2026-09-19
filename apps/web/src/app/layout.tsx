import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AOS — G Designer School',
  description: 'Academic Operational System: o sistema operativo da instituição de ensino.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-AO">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
