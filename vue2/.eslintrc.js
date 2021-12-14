module.exports = {
  root: true,
  extends: [
    "plugin:vue/strongly-recommended",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "@vue/prettier/@typescript-eslint"
  ],

  "parserOptions": {
    "ecmaVersion": 2021
  },
  "plugins": [],
  "rules": {
    "function-call-argument-newline": ["warn", "consistent"],
    "quotes": ["warn", "single", { "avoidEscape": true }],

    "vue/max-attributes-per-line": ["error", {
      "singleline": {
        "max": 2
      },
      "multiline": {
        "max": 1
      }
    }]

    // 'prettier/prettier': ['error', { singleQuote: true }]
  }
  // parserOptions: {
  //   parser: "babel-eslint",
  //   sourceType: "module"
  // },
  //
  // rules: {
  //   // override/add rules settings here, such as:
  //   // 'vue/no-unused-vars': 'error'
  // }
};
