module.exports = {
  transpileDependencies: ["vuetify"],

  publicPath: process.env.VUE_APP_STATIC_URL,
  configureWebpack: {
    devtool: "source-map"
  }
};
