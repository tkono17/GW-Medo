import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path' // これを追加

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // 全ての 'react' 参照をプロジェクト直下のものに固定する
      'react': path.resolve(__dirname, 'node_modules/react'),
      'react-dom': path.resolve(__dirname, 'node_modules/react-dom'),
    },
  },
})
