const { merge } = require("webpack-merge");
const path = require("path");

const common = require("./webpack.common.js");

const BundleAnalyzerPlugin =
  require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

module.exports = merge(common, {
  mode: "production",

  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: "static",
      reportFilename: path.join(
        "..",
        "..",
        "..",
        "..",
        "..",
        "frontend",
        "bundle-report.html"
      ),
      openAnalyzer: false
    })
  ]
});
