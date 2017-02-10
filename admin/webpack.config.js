const path = require('path')
const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: {
    app: './src/index.js',
    vendor: ['vue', 'vue-router', 'vuex', 'axios', 'moment', 'es6-promise']
  },
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/',
    filename: 'build-[hash].js'
  },
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({
          fallbackLoader: 'style-loader',
          loader: 'css-loader'
        })
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          postcss: [require('postcss-cssnext')()],
          loaders: {
              css: ExtractTextPlugin.extract({
                fallbackLoader: 'vue-style-loader',
                loader: 'css-loader'
              })
          }
        }
      },
      {
        test: /\.otf|ttf|woff2?|eot(\?\S*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: '[name].[ext]?[hash]'
        }
      },
      {
        test: /\.svg(\?\S*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: '[name].[ext]?[hash]'
        }
      },
      {
        test: /\.(png|jpg|gif|ico)$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  // devServer: {
  //   host: '127.0.0.1',
  //   port: 8010,
  //   proxy: {
  //     '/api/': {
  //       target: 'http://127.0.0.1:8080',
  //       changeOrigin: true,
  //       pathRewrite: {
  //         '^/api': ''
  //       }
  //     }
  //   },
  //   historyApiFallback: {
  //     index: url.parse(options.dev ? '/assets/' : publicPath).pathname
  //   }
  // },
  plugins: [
    new ExtractTextPlugin('styles-[hash].css'),
    new HtmlWebpackPlugin({
      template: 'src/index.html',
      output: {
        path: path.resolve(__dirname, '../planet/static/admin'),
        filename: 'index.html'
      }
    }),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
    }),
    // extract vendor chunks for better caching
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      filename: 'vendor-[hash].js'
    })
  ],
  devtool: process.env.NODE_ENV ? '#eval-source-map' : '#source-map'
}

if (process.env.NODE_ENV === 'production') {
  module.exports.output={
    path: path.resolve(__dirname, '../planet/static/admin/dist'),
    publicPath: '/admin/dist/',
    filename: 'build-[hash].js'
  }
  // http://vuejs.github.io/vue-loader/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.LoaderOptionsPlugin({
      minimize: true
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    })
  ])
}
