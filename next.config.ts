import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: '/abp-interactive-learning',
  assetPrefix: '/abp-interactive-learning',
};

export default nextConfig;
