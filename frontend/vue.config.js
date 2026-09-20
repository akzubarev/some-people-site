module.exports = {
  productionSourceMap: false,
  publicPath: '/',
  devServer: {
    proxy: {
      '^/(api|media|staticfiles)': { target: process.env.API_URL, changeOrigin: true },
    },
    port: 8080,
    host: '0.0.0.0',
  },
}
