import { defineConfig } from 'vite'
import dotenv from 'dotenv';
import react from '@vitejs/plugin-react'

dotenv.config();

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    'process.env': {},
  },
  plugins: [react()],
  server: {
    host: true, // Or use your Mac's IP address like '192.168.x.x'
    port: 3000, // Ensure this matches the port you are using
    //strictPort: true,
  },
})