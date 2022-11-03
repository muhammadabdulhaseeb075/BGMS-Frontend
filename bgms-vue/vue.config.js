const BundleTracker = require("webpack-bundle-tracker");
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  publicPath: process.env.VUE_APP_PUBLICPATH,
  outputDir: "../BGMS/main/static/main/dist",
  pages: {
    main: './src/main/main.ts',
    mainbooking: './src/main-booking/main.ts',
    mapmanagement: './src/mapmanagement/main.ts',
    datamatching: './src/datamatching/main.ts',
    analytics: './src/analytics/main.ts'
  },
  chainWebpack: config => {
    const pageKeys = Object.keys(module.exports.pages)
    const IS_VENDOR = /[\\/]node_modules[\\/]/
    
    if(config.plugins.has('extract-css')) {
      const extractCSSPlugin = config.plugin('extract-css')
      extractCSSPlugin && extractCSSPlugin.tap(() => [{
        filename: "[name][contenthash].css",
        chunkFilename: "[id].chunk-[chunkhash].css"
      }])
    }
    
    config.optimization.splitChunks({
      cacheGroups: {
        vendors: {
          name: 'chunk-vendors',
          priority: -10,
          chunks: 'initial',
          minChunks: 2,
          test: IS_VENDOR,
          enforce: true,
        },
        ...pageKeys.map(key => ({
          name: `chunk-${key}-vendors`,
          priority: -11,
          chunks: chunk => chunk.name === key,
          test: IS_VENDOR,
          enforce: true,
        })),
        common: {
          name: 'chunk-common',
          priority: -20,
          chunks: 'initial',
          minChunks: 2,
          reuseExistingChunk: true,
          enforce: true,
        },
      },
    })
  },
  configureWebpack: {
    plugins: [
      new BundleTracker({path: '../BGMS/main/static/main/dist/'}),
      new VuetifyLoaderPlugin()
    ],
    devtool: process.env.NODE_ENV === 'production'
      ? ''
      : 'source-map',
    output: {
      filename: '[name].js',
      chunkFilename: '[id].chunk-[chunkhash].js'
    }
  },
  transpileDependencies: ['vuetify', 'ansi-regex', 'strip-ansi', 'vue-search-select'],
  devServer: {
    clientLogLevel: 'warning',
    hot: true,
    host: process.env.HOST,
    port: 8080,
    open: false,
    overlay: { warnings: false, errors: true },
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: {
      ignored: /node_modules/,
    },
    headers: { 'Access-Control-Allow-Origin': '*' },
    disableHostCheck: true
  }
}
