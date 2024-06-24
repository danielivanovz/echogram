/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: process.env.NODE_ENV === "development" ? `${NEXT_PUBLIC_BACKEND_URL}/api/:path*` : "/api/",
      },
      {
        source: "/docs",
        destination: process.env.NODE_ENV === "development" ? `${NEXT_PUBLIC_BACKEND_URL}/docs` : "/api/docs",
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development" ? `${NEXT_PUBLIC_BACKEND_URL}/openapi.json` : "/api/openapi.json",
      },
    ]
  },
}

export default nextConfig
