// Karma configuration
// Generated on Tue Oct 27 2015 16:03:36 GMT+0000 (GMT Standard Time)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',

//    plugins: ['karma-requirejs'],

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],

    // list of files / patterns to load in the browser
    files: [
            //loading library files
            'BGMS/static/libs/bower_components/jquery/dist-js/jquery.min.js',
            'BGMS/static/libs/bootstrap/js/bootstrap.js',
            'BGMS/static/libs/proj4/**/*.js',
            'BGMS/static/libs/openlayers/v3.13.0/js/ol.js',
            'BGMS/static/libs/pnotify/v2.0.1/js/pnotify.custom.min.js',
            'dataentry/static/dataentry/bower_components/angular/angular.js',
            'dataentry/static/dataentry/bower_components/angular-mocks/angular-mocks.js',
            'dataentry/static/dataentry/bower_components/angular-route/angular-route.js',
            'dataentry/static/dataentry/bower_components/angular-sanitize/angular-sanitize.js',
            'dataentry/static/dataentry/bower_components/bootstrap-table/dist/bootstrap-table.js',
            'dataentry/static/dataentry/bower_components/bootstrap-table/dist/extensions/angular/bootstrap-table-angular.js',
            'dataentry/static/dataentry/bower_components/bootstrap-table/dist/extensions/reorder-columns/bootstrap-table-reorder-columns.js',
            'dataentry/static/dataentry/bower_components/dragtable/jquery.dragtable.js',
            'dataentry/static/dataentry/bower_components/ladda/dist/ladda.min.js',
            'dataentry/static/dataentry/bower_components/TableDnD/dist/jquery.tablednd.js',
            'mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-openlayers-directive.js',

            //Then mapmanagement angular-modules
            "mapmanagement/static/dataentry/angular/components/openlayers-directive/**/*.js",
            
            //Dataentry angular modules
            "dataentry/static/dataentry/angular/components/dataentry.js",
            "dataentry/static/dataentry/angular/app.module.js",
            "dataentry/static/dataentry/angular/app.route.js",
            "dataentry/static/dataentry/angular/**/**.js"
            
    ],


    // list of files to exclude
    exclude: [
              'mapmanagement/static/mapmanagement/bgms_angular/bower_components/goog/**/*.js',
              'mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular/**/*.js',
              'BGMS/static/libs/RequireJS/**/*.js',
              'main/static/main/js/app.js',
              'dataentry/static/dataentry/bower_components/dragtable/**/*.js',
              'mapmanagement/static/mapmanagement/js/mapmanagement.js'
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false,

    // Concurrency level
    // how many browser should be started simultanous
    concurrency: Infinity
  })
}
