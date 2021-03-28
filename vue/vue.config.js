var path = require("path");

module.exports = {
    configureWebpack: {
        devtool: "source-map"
    },
    publicPath: "./static",
    indexPath: path.join("../templates", "index.html"),
    outputDir: path.join("../Django", "static")
};
