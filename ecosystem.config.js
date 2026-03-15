module.exports = {
  apps: [
    {
      name: 'quantum-frontend',
      script: 'node_modules/next/dist/bin/next',
      args: 'start -p 3001',
      cwd: '/root/var/www/Quantum-Uz',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 3001,
        PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.nvm/versions/node/v24.14.0/bin',
        NEXT_PUBLIC_API_URL: 'http://62.72.32.37/api'
      }
    }
  ]
};
