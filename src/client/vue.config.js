module.exports = {
    lintOnSave: false,
    configureWebpack: {
      devtool: 'source-map'
    },
    chainWebpack: config => {
      config
      .plugin('html')
      .tap((args) => {
        args[0].title = 'CCC';
        return args;
      });
    },
    
    productionSourceMap: false,
    devServer: { 
      disableHostCheck: true,
      host: '127.0.0.1',
      port: 8089,
    },
  }
  