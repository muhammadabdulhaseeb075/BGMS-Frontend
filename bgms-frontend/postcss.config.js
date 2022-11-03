const path = require("path");
const postcssResolve = require("postcss-import-alias-resolver");

module.exports = {
    plugins: [
        require("postcss-import")({
            // resolve: postcssResolve({
            //     alias: {
            //         "src": path.resolve(__dirname, "./src"),
            //     },
            // }),
            root: path.resolve(__dirname, "./src"),
            path: path.resolve(__dirname, "./src"),
        }),
        require('postcss-custom-properties')({
            preserve: false, // completely reduce all css vars
            importFrom: [
              'src/router/Booking/containers/ag-calendar/fullcalendar-vars.css' // look here for the new values
            ]
          }),
        require("postcss-nested"),
        require("postcss-advanced-variables"),
        require("tailwindcss"),
        require("postcss-discard-comments"),
        require("autoprefixer"),
        require('postcss-calc')
    ],
}


