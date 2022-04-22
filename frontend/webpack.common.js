const pkg = require("./package.json");

const path = require("path");

const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /\/node_modules\//,
                use: "ts-loader"
            },

            {
                test: /\.module\.s?css$/i,
                use: [
                    "style-loader",
                    {
                        loader: "css-loader",
                        options: {
                            modules: true
                        }
                    },
                    "sass-loader"
                ]
            },

            {
                test: /\.s?css$/i,
                exclude: /\.module\.s?css$/,
                use: ["style-loader", "css-loader", "sass-loader"]
            },

            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: "asset/resource"
            }
        ]
    },

    entry: "./src/main.tsx",

    output: {
        path: path.resolve(
            __dirname,
            "..",
            "src",
            "info",
            "gianlucacosta",
            "jardinero",
            "static"
        ),
        filename: `${pkg.name}.[contenthash].js`
    },

    resolve: {
        extensions: [".ts", ".tsx", "..."]
    },

    performance: {
        assetFilter: asset => {
            return asset.match(`\.js$`);
        }
    },

    plugins: [
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            title: pkg.appName,
            filename: "index.html",
            favicon: "favicon.svg"
        })
    ]
};
