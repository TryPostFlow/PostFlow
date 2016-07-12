var vue = require('vue-loader')
var webpack = require('webpack')
var ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    path: './build',
    publicPath: '/build/',
    filename: 'build.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel'},
      { test: /\.css$/, loader: ExtractTextPlugin.extract('style', 'css', 'postcss')},
      { test: /\.vue$/, loader: 'vue' },
      {
        test: /\.(png|jpg|gif)$/,
        loader: 'url',
        query: {
          limit: 10000,
          name: '[name].[ext]?[hash]'
        }
      },
      {
        test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url?limit=10000&mimetype=application/font-woff'
      },
      {
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url?limit=10000&mimetype=application/font-woff'
      },
      {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url?limit=10000&mimetype=application/octet-stream'
      },
      {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'file'
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url?limit=10000&mimetype=image/svg+xml'
      }]
  },
  babel: {
    presets: ['es2015'],
    plugins: ['transform-runtime']
  },
  vue: {
    postcss: [
      require('postcss-import')({
        addDependencyTo: webpack
      }),
      require('postcss-url')({
        url: 'rebase'
      }),
      require('postcss-mixins'),
      require('postcss-simple-vars'),
      require('postcss-cssnext')],
    autoprefixer: false,
    loaders: {
      css: ExtractTextPlugin.extract('css')
    }
  },
  postcss: function () {
    return [
      require('postcss-import')({
        addDependencyTo: webpack,
        onImport: function (files) {
          files.forEach(this.addDependency)
        }.bind(obj) // obj = the argument you should pass to `addDependencyTo()`
      }),
      require('postcss-url')({
        url: 'rebase'
      }),
      require('postcss-mixins'),
      require('postcss-simple-vars'),
      require('postcss-cssnext')]
  },
  plugins: [
    new ExtractTextPlugin('style.css')
  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.plugins = [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    }),
    new webpack.optimize.OccurenceOrderPlugin()
  ]
} else {
  module.exports.devtool = '#source-map'
}
