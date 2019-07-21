module.exports = {
    // ...
    devServer: {
        proxy: {
            // proxy all requests starting with /api to jsonplaceholder
            '/api': {
                target: 'http://localhost',
                changeOrigin: true,
                // pathRewrite: {
                //     '^/api': ''
                // },
                // secure: false
            }
        }
    }
}