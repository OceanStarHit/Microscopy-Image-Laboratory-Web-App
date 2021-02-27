module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: ["plugin:vue/essential", "eslint:recommended", "@vue/prettier"],
  parserOptions: {
    parser: "babel-eslint"
  },
  // rules: {
  //   "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
  //   "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
  //   // allow paren-less arrow functions
  //   "arrow-parens": 0,
  //   // allow async-await
  //   "generator-star-spacing": 0,
  //   // allow debugger during development
  //   "no-debugger": process.env.NODE_ENV === "production" ? 2 : 0,
  //   // 4 space indentation
  //   indent: ["error", 4],
  //   // Allow extra semicolons
  //   semi: 0
  // },
  // required to lint *.vue files
  plugins: ["html"],
  parserOptions: {
    sourceType: "module"
  }
};
