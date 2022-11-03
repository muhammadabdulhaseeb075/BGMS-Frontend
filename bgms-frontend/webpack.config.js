const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");

const DEV_ENV = "development";
const PROD_ENV = "production";
const ENV = process.env.NODE_ENV || DEV_ENV;
const staticPathConfig = {
    production: "https://bgms36.s3.amazonaws.com/build/bgms-frontend/",
    staging: "https://bgmscompressed.s3.amazonaws.com/build/bgms-frontend/",
    development: "/static/build/bgms-frontend/",
};
const isNotLocal = ENV !== DEV_ENV;


module.exports = {
    mode: isNotLocal ? PROD_ENV : DEV_ENV,
    entry: [
        "./src/main.js",
    ],
    plugins: [
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({ filename: "styles.css"}),
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify(isNotLocal ? PROD_ENV : DEV_ENV),
        })
    ],
    resolve: {
        extensions: [".js", ".vue"],
        // makes the main routes absolute for the whole project
        alias: {
            src: path.resolve(__dirname, "src"),
            vue: "@vue/runtime-dom",
        }
    },
    module: {
        rules: [
            {
                test: /\.vue?$/,
                loader: "vue-loader",
            },
            { 
                test: /\.js?$/,
                use: "babel-loader",
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "postcss-loader",
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader"
                ]
            },
            { test: /\.pug?$/, use: "pug-plain-loader" },
            {
                test: /\.(jpg|png|eot|svg|ttf|woff|woff2)$/,
                use: "file-loader"
            },
            {
                test: /\.(gif|mp3|mp4|webm)/,
                use: "file-loader"
            }
        ],
    },
    devtool: isNotLocal ? "source-map" : "inline-source-map",
    output: {
        path: path.resolve(__dirname, "../BGMS/BGMS/static/build/bgms-frontend"),
        filename: "bundle.js",
        publicPath: staticPathConfig[ENV],
    },
    watchOptions: {
        ignored: "**/node_modules",
    },
    optimization: {
        minimize: isNotLocal,
    },
};
