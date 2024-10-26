const NodePolyfillPlugin = require("node-polyfill-webpack-plugin");


module.exports = {
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === "production" ? "/" : "/",
  configureWebpack: {
    plugins: [
      new NodePolyfillPlugin()
    ],
  },
  devServer: {
    proxy: {
      "/(media|api|auth)": {
        // target: "https://residual.community",
        target: process.env.API_URL,
        // target: 'http://127.0.0.1:8000',
        // target: 'https://dividendo.link',
        // target: 'https://instagame.pro',
        // target: 'https://cryptoqueue.pro/',
        changeOrigin: true
      }
    },
    port: 8080,
    host: '0.0.0.0',
    https: false,
  }
}
