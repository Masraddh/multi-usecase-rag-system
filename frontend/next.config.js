/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: process.env.BACKEND_URL || 'http://localhost:8000/api/v1/:path*',
      },
      {
        source: '/docs',
        destination: 'http://localhost:8000/docs',
      },
      {
        source: '/redoc',
        destination: 'http://localhost:8000/redoc',
      },
    ];
  },
};

module.exports = nextConfig;
