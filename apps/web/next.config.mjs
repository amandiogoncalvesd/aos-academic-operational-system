/** @type {import('next').NextConfig} */
const API_INTERNAL = process.env.API_INTERNAL_URL ?? 'http://localhost:8000';
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@aos/config'],
  async rewrites() {
    // O browser fala sempre com o próprio host (/api, /health); o dev server encaminha para o core.
    return [
      { source: '/api/:path*', destination: `${API_INTERNAL}/api/:path*` },
      { source: '/health/:path*', destination: `${API_INTERNAL}/health/:path*` },
      { source: '/health', destination: `${API_INTERNAL}/health` },
    ];
  },
};
export default nextConfig;
