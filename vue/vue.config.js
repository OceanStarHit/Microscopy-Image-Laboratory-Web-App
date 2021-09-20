// const WasmPackPlugin = require("@wasm-tool/wasm-pack-plugin");
// const path = require("path");

module.exports = {
  // chainWebpack: config => {
  //   // rust wasm bindgen https://github.com/rustwasm/wasm-bindgen
  //   config
  //     .plugin("wasm-pack")
  //     .use(require("@wasm-tool/wasm-pack-plugin"))
  //     .init(
  //       Plugin =>
  //         new Plugin({
  //           crateDirectory: path.resolve(__dirname, "../wasm"),
  //           outDir: path.resolve(__dirname, "./src/assets/wasm/pkg"),
  //           forceMode: "development",
  //           // forceMode: "production"
  //         })
  //     )
  //     .end();
  // },

  transpileDependencies: ["vuetify"],

  publicPath: process.env.VUE_APP_STATIC_URL,
  configureWebpack: {
    devtool: "source-map"
  }
};
