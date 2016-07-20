var path = require('path')
var webpack = require('webpack')
var ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/admin/',
    filename: 'build.js'
  },
  resolveLoader: {
    root: path.join(__dirname, 'node_modules'),
  },
  module: {
    loaders: [
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel'},
      { test: /\.css$/, loader: ExtractTextPlugin.extract('style', 'css')},
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
    loaders: {
      css: ExtractTextPlugin.extract('css')
    }
  },
  plugins: [
    new ExtractTextPlugin('style.css')
  ],
  devServer: {
    historyApiFallback: {
      index: '/dist/'
    },
    noInfo: true
  },
  devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
  module.exports.output={
    path: path.resolve(__dirname, '../planet/static/admin/dist'),
    publicPath: '/admin/',
    filename: 'build.js'
  }
  module.exports.devtool = 'source-map'
  // http://vuejs.github.io/vue-loader/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
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
  ])
}
