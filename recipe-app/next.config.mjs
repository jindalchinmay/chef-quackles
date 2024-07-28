/** @type {import('next').NextConfig} */

const nextConfig = {
    images: {
        domains: ['firebasestorage.googleapis.com'],
        disableStaticImages: true, 
      },
};

export default nextConfig;
