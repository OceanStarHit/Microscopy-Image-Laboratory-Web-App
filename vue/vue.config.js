var path = require("path");

// module.exports = {
//     configureWebpack: {
//         devtool: "source-map"
//     },
//     publicPath: "./static",
//     indexPath: path.join("../templates", "index.html"),
//     outputDir: path.join("../Django", "static")
// };

// const path = require("path");

module.exports = {
  transpileDependencies: ["vuetify"],

  publicPath: process.env.VUE_APP_STATIC_URL,
  outputDir: path.resolve(__dirname, "../django/static"),
  indexPath: path.resolve(__dirname, "../django/templates", "index.html"),

  configureWebpack: {
    devtool: "source-map"
  }
};
