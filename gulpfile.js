
var gulp = require('gulp');
var gutil = require('gulp-util');
var del = require('del');
var gulpif = require('gulp-if');
var pump = require('pump');
var exec = require('child_process').exec;
var notify = require('gulp-notify');
var buffer = require('vinyl-buffer');
var concat = require('gulp-concat');
var runSequence = require('run-sequence');
var browserSync = require('browser-sync');
var stripDebug = require('gulp-strip-debug');
var strip = require('gulp-strip-comments');
var reload = browserSync.reload;
var debug = require('gulp-debug');
var shell = require('gulp-shell');
var install = require('gulp-install');
var uglify = require('gulp-uglify-es').default;
var pump = require('pump');


// sass
var sass = require('gulp-sass');
var postcss = require('gulp-postcss');
var sourcemaps = require('gulp-sourcemaps');
var cssnano = require('cssnano');
var rename = require('gulp-rename');
// js
var watchify = require('watchify');
var browserify = require('browserify');
var source = require('vinyl-source-stream');


var postcssPlugins = [cssnano()];

// --------------------------
// Relative paths function
// --------------------------
var pathsConfig = function (appName) {
  this.app = "./" + appName + "/" + appName;
  this.build = this.app + '/static/build/';
  return {
    app: this.app,
    css: this.app + '/static/css',
    sass: this.app + '/static/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
    build: this.build,
    buildCss: this.build + 'css/',
    buildJs: this.build + 'js/',
    serviceWorker: this.app + '/templates/sw.js',
  };
};

var paths = pathsConfig('BGMS');


// --------------------------
// TASK METHODS
// --------------------------
var tasks = {
  // --------------------------
  // Delete build folder
  // --------------------------
  clean: function(cb) {
    del([paths.build, paths.serviceWorker], cb);
  },
  // --------------------------
  // Copy static assets
  // --------------------------
  assets: function() {
    return gulp.src('./BGMS/BGMS/static/js/*')
      .pipe(gulp.dest('build/assets/'));
  },
  // --------------------------
  // SASS (libsass)
  // --------------------------
  defaultsass: function(sassFilename, basename) {
    return gulp.src(paths.sass + sassFilename)
      // .pipe(debug())
      // sourcemaps + sass + error handling
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sass().on('error', sass.logError))
      // autoprefixer
      // .pipe(postcss([autoprefixer({browsers: ['last 2 versions']})]))
      .pipe(postcss(postcssPlugins)) // Minifies the result
      .pipe(rename({ basename:basename, suffix: '.min' }))
      // generate .maps
      .pipe(sourcemaps.write())
      // give it a file and save
      .pipe(gulp.dest(paths.buildCss));
  },

  mainsass: function() {
    return tasks.defaultsass('/main.scss', 'main');
  },

  mainsass_dev: function() {
    return gulp.src(paths.sass + '/main.scss')
      // .pipe(debug())
      // sourcemaps + sass + error handling
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sass().on('error', sass.logError))
      // autoprefixer
      // .pipe(postcss([autoprefixer({browsers: ['last 2 versions']})]))
      .pipe(postcss(postcssPlugins)) // Minifies the result
      .pipe(rename({ suffix: '.min' }))
      // generate .maps
      .pipe(sourcemaps.write())
      // give it a file and save
      .pipe(gulp.dest(paths.buildCss));
      // .pipe(browserSync.reload({stream:true}));
  },

  mapmanagementsass: function() {
    return tasks.defaultsass('/mapmanagement.scss', 'mapmanagement');
  },

  mapmanagementsass_dev: function() {
    return gulp.src(paths.sass + '/mapmanagement.scss')
      // .pipe(debug())
      // sourcemaps + sass + error handling
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sass().on('error', sass.logError))
      // autoprefixer
      // .pipe(postcss([autoprefixer({browsers: ['last 2 versions']})]))
      .pipe(postcss(postcssPlugins)) // Minifies the result
      .pipe(rename({ suffix: '.min' }))
      // generate .maps
      .pipe(sourcemaps.write())
      // give it a file and save
      .pipe(gulp.dest(paths.buildCss));
      // .pipe(browserSync.reload({stream:true}));
  },

  desass: function() {
    return tasks.defaultsass('/dataentry.scss', 'de');
  },

  admsass: function() {
    return tasks.defaultsass('/admin.scss', 'adm');
  },

  dmsass: function() {
    return tasks.defaultsass('/datamatching.scss', 'dm');
  },

  dmsass_dev: function() {
    return gulp.src(paths.sass + '/datamatching.scss')
      // .pipe(debug())
      // sourcemaps + sass + error handling
      .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(sass().on('error', sass.logError))
      // autoprefixer
      // .pipe(postcss([autoprefixer({browsers: ['last 2 versions']})]))
      .pipe(postcss(postcssPlugins)) // Minifies the result
      .pipe(rename({ basename: 'dm', suffix: '.min' }))
      // generate .maps
      .pipe(sourcemaps.write())
      // give it a file and save
      .pipe(gulp.dest(paths.buildCss));
      // .pipe(browserSync.reload({stream:true}));
  },

  lpsass: function() {
    return tasks.defaultsass('/landing-page.scss', 'lp');
  },

//   gulp.task('styles', function() {
//   return gulp.src(paths.sass + '/project.scss')
//     .pipe(sass().on('error', sass.logError))
//     .pipe(plumber()) // Checks for errors
//     .pipe(autoprefixer({browsers: ['last 2 version']})) // Adds vendor prefixes
//     .pipe(pixrem())  // add fallbacks for rem units
//     .pipe(gulp.dest(paths.css))
//     .pipe(rename({ suffix: '.min' }))
//     .pipe(postcss(postcssPlugins)) // Minifies the result
//     .pipe(gulp.dest(paths.css));
// });


  // --------------------------
  // Uglify
  // --------------------------
  mapvanjs: function() {
    // mapmanagement vanilla js
    return gulp.src(['./BGMS/BGMS/static/js/*.js', './BGMS/mapmanagement/static/mapmanagement/js/*.js'])
    .pipe(concat('all.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./BGMS/BGMS/static/build/js/'));
  },

  mapangjs: function() {
    // mapmanagement angular js
    return gulp.src([
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/app.module.ng1.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/map.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/constants.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/mapService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/personService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/layerGroupService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/layerService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/layerToolbar/layerGeneratorService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/notificationHelper.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/featureHelperService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/geometryHelperService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/featureOverlayService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/interactionService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/eventService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/styleService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/markerService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/memorialService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/userActionService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/mapController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/modalHelperService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/map/reportingService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/layerToolbar/layerController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/personController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/personInteractionService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/security/securityService.js' ,
              
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/layerSelection/layerSelectionController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/layerSelection/layerSelectionService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/offline/offlineService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/exportMap/exportMapService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/reservePlot/reservedPersonService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/util/subdomainService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/util/capitalizeFilter.js',
              
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/ManagementToolController.js',
              ])
    .pipe(strip())
    .pipe(stripDebug())
    .pipe(concat('all-a.js'))
    // .pipe(uglify({ mangle: false }))
    .pipe(uglify())
    .pipe(gulp.dest(paths.buildJs));
  },

  mapauthangjs: function() {
    // mapmanagement angular js
    return gulp.src([
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/drawingToolbar/toolbarService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/addGraveController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/addMemorialController.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/addGraveService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/addMemorialService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/floatingPlotToolbarService.js' ,
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/person/floatingMemorialToolbarService.js' ,
              
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/MemorialCaptureSidebarController.js',
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/GraveLinkSidebarController.js',
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/VueOtherToolsController.js',
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/VueDrawingToolsController.js',
              './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/vue-components/VueLayersToolbarController.js'
              ])
    .pipe(strip())
    .pipe(stripDebug())
    .pipe(concat('all-a-auth.js'))
    // .pipe(uglify({ mangle: false }))
    .pipe(uglify())
    .pipe(gulp.dest(paths.buildJs));
  },

  devanjs: function() {
    // dataentry vanilla js
    return gulp.src(['./BGMS/dataentry/static/dataentry/js/*.js'])
    .pipe(concat('all-de.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./BGMS/BGMS/static/build/js/'));
  },

  deangjs: function() {
    //dataentry angular js
    return gulp.src(['./BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olHelperExtended.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexHelper.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexInteractionHelper.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexMapInteractionDirective.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexMapEventDirective.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexFeatureOverlayDirective.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexExtentDirective.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/olexOverlayDirective.js',
                './BGMS/dataentry/static/dataentry/angular/components/openlayers-directive/openlayersDecorator.js',
                './BGMS/dataentry/static/dataentry/angular/app.module.js',
                './BGMS/dataentry/static/dataentry/angular/app.route.js',
                './BGMS/dataentry/static/dataentry/angular/components/dataentry.js',
                './BGMS/dataentry/static/dataentry/angular/components/arrayHelperService.js',
                './BGMS/dataentry/static/dataentry/angular/components/notificationHelper.js',
                './BGMS/dataentry/static/dataentry/angular/components/featureHelperService.js',
                './BGMS/dataentry/static/dataentry/angular/models/templateModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/columnModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/fieldModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/formModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/imageModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/tagModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/burialRecordModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/imageHistoryModel.js',
                './BGMS/dataentry/static/dataentry/angular/models/userActivityModel.js',
                './BGMS/dataentry/static/dataentry/angular/services/burialRecordService.js',
                './BGMS/dataentry/static/dataentry/angular/services/manyToManyFieldService.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsLadda.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsPanzoom.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsBootstrapTable.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsColumnField/bgmsBasicField.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsColumnField/bgmsColumnField.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/imageViewerController.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/imageViewerService.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/imageTaggerController.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/imageTaggerService.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/openlayersService.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/bgmsImageViewer.js',
                './BGMS/dataentry/static/dataentry/angular/directives/bgmsImageHandler/bgmsImageTagger.js',
                './BGMS/dataentry/static/dataentry/angular/components/createTemplate/templateCreationController.js',
                './BGMS/dataentry/static/dataentry/angular/components/createTemplate/templateCreationService.js',
                './BGMS/dataentry/static/dataentry/angular/components/listTemplates/listTemplatesController.js',
                './BGMS/dataentry/static/dataentry/angular/components/listTemplates/listTemplatesService.js',
                './BGMS/dataentry/static/dataentry/angular/components/addBurialRecord/addBurialRecordController.js',
                './BGMS/dataentry/static/dataentry/angular/components/addBurialRecord/addBurialRecordService.js',
                './BGMS/dataentry/static/dataentry/angular/components/imageStatus/imageStatusController.js',
                './BGMS/dataentry/static/dataentry/angular/components/imageStatus/imageStatusService.js',
                './BGMS/dataentry/static/dataentry/angular/components/userActivity/userActivityController.js',
              ])
    .pipe(strip())
    .pipe(stripDebug())
    .pipe(concat('all-ang-de.js'))
    // .pipe(uglify({ mangle: false }))
    .pipe(uglify())
    .pipe(gulp.dest(paths.buildJs));
  },

  dmvanjs: function() {
    // datamatching vanilla js
    return gulp.src(['./BGMS/datamatching/static/datamatching/js/*.js'])
    .pipe(concat('all-dm.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./BGMS/BGMS/static/build/js/'));
  },

  generateServiceWorker: function() {
    var path = require('path');
    var fs = require('fs');
    var swPrecache = require('./bgms-sw-generator');

    return swPrecache.write(paths.serviceWorker, {
      maximumFileSizeToCacheInBytes: 60000000, // 10MB - this is high, but in dev vendor.js is really big. //changed to 60mb
      staticFileGlobs: [
        './BGMS/main/static/main/dist/*.{html,js,css}',
        './BGMS/main/static/main/dist/img/*.png',

        './BGMS/mapmanagement/static/mapmanagement/assets/img/*.png',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/*.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular/angular.min.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-animate/angular-animate.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-route/angular-route.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-resource/angular-resource.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular/angular.min.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/ui-bootstrap-tpls-0.13.4.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-ui-router.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/bower_components/angular-sanitize.min.js',
        './BGMS/mapmanagement/static/mapmanagement/bgms_angular/components/**/*.{html,js}',
        './BGMS/mapmanagement/static/mapmanagement/js/*.js',
        './BGMS/mapmanagement/static/mapmanagement/node_modules2/**/*.js',

        './BGMS/BGMS/static/build/**/*.{js,css}',
        './BGMS/BGMS/static/css/hover-effects.css',
        './BGMS/BGMS/static/css/floating-labels.css',
        './BGMS/BGMS/static/css/flexslider.css',
        './BGMS/BGMS/static/css/map-styles-custom.css',
        './BGMS/BGMS/static/images/Layers/icons/*.png',
        './BGMS/BGMS/static/images/logo/BGMS_logo_header.png',
        './BGMS/BGMS/static/images/modal/*.{png,jpg}',
        './BGMS/BGMS/static/js/*.js',

        './BGMS/BGMS/static/libs/bower_components/AdminLTE/dist-js/js/app.min.js',
        './BGMS/BGMS/static/libs/bower_components/jquery-validation/dist-js/jquery.validate.min.js',
        './BGMS/BGMS/static/libs/bower_components/jquery-validation/dist-js/additional-methods.min.js',
        './BGMS/BGMS/static/libs/bower_components/AdminLTE/dist-js/css/AdminLTE.min.css',
        './BGMS/BGMS/static/libs/bower_components/jquery/dist-js/jquery.min.js',
        './BGMS/BGMS/static/libs/bootstrap/fonts/glyphicons-halflings-regular.woff2',
        './BGMS/BGMS/static/libs/bower_components/jquery/dist-js/jquery.min.js',
        './BGMS/BGMS/static/libs/jquery-ui/v1.11.1/js/jquery-ui.min.js',
        './BGMS/BGMS/static/libs/bootstrap/js/bootstrap.min.js',
        './BGMS/BGMS/static/libs/bootstrap-dropdowns-enhancement/js/dropdowns-enhancement.js',
        './BGMS/BGMS/static/libs/pnotify/v2.0.1/js/pnotify.custom.min.js',
        './BGMS/BGMS/static/libs/pnotify/v2.0.1/js/pnotify.buttons.js',
        './BGMS/BGMS/static/libs/pnotify/v2.0.1/js/pnotify.confirm.js',
        './BGMS/BGMS/static/libs/pnotify/v2.0.1/js/pnotify.callbacks.js',
        './BGMS/BGMS/static/libs/pnotify/v2.0.1/css/pnotify.custom.min.css',
        './BGMS/BGMS/static/libs/jQuery-File-Upload/v9.9.3/js/vendor/jquery.ui.widget.js',
        './BGMS/BGMS/static/libs/jQuery-File-Upload/v9.9.3/js/jquery.iframe-transport.js',
        './BGMS/BGMS/static/libs/jQuery-File-Upload/v9.9.3/js/jquery.fileupload.js',
        './BGMS/BGMS/static/libs/bootstrap-datepicker/v1.4.0/js/bootstrap-datepicker.min.js',
        './BGMS/BGMS/static/libs/bootstrap-table/v1.7.0/js/bootstrap-table.min.js',
        './BGMS/BGMS/static/libs/bootstrap-table/extensions/flatJSON/bootstrap-table-flatJSON.min.js',
        './BGMS/BGMS/static/libs/css-element-queries/v0.2.1/js/ResizeSensor.js',
        './BGMS/BGMS/static/libs/ladda/v0.9.4/js/spin.min.js',
        './BGMS/BGMS/static/libs/ladda/v0.9.4/js/ladda.min.js',
        './BGMS/BGMS/static/libs/jquery.nanoscroller/v0.8.7/js/jquery.nanoscroller.min.js',
        './BGMS/BGMS/static/libs/jquery.maskedinput/v1.4.0/js/jquery.maskedinput.min.js',
        './BGMS/BGMS/static/libs/selectize/v0.12.1/js/standalone/selectize.min.js',
        './BGMS/BGMS/static/libs/jquery.flexslider/v2.5.0/js/jquery.flexslider.js',
        './BGMS/BGMS/static/libs/canvas-toBlob.js-master/canvas-toBlob.js',
        './BGMS/BGMS/static/libs/lodash/v4.13.1/lodash.min.js',
        './BGMS/BGMS/static/libs/bootstrap/css/bootstrap.min.css',
        './BGMS/BGMS/static/images/icons/gravestone.ico',
        './BGMS/BGMS/static/libs/bootstrap-datepicker/v1.4.0/css/bootstrap-datepicker3.min.css',
        './BGMS/BGMS/static/libs/bootstrap-table/v1.7.0/css/bootstrap-table.min.css',
        './BGMS/BGMS/static/libs/bootstrap-dropdowns-enhancement/css/dropdowns-enhancement.min.css',
        './BGMS/BGMS/static/libs/ionicons/v1.5.2/css/ionicons.min.css',
        './BGMS/BGMS/static/libs/selectize/v0.12.1/css/selectize.css',
        './BGMS/BGMS/static/libs/ladda/v0.9.4/css/ladda-themeless.min.css',
        './BGMS/BGMS/static/libs/jquery.nanoscroller/v0.8.7/css/nanoscroller.css',
        './BGMS/BGMS/static/libs/openlayers/v4.6.5-dist/ol.css',

        //'./BGMS/BGMS/static/fonts/font-awesome-4.5.0/css/font-awesome.min.css',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/css/fontawesome.min.css',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/css/solid.min.css',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/css/regular.min.css',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-400.eot',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-400.woff2',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-400.woff',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-400.ttf',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-400.svg',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-900.eot',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-900.woff2',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-900.woff',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-900.ttf',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-regular-900.svg',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-solid-900.woff2',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-solid-900.woff',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-solid-900.ttf',
        './BGMS/BGMS/static/fonts/fontawesome-free-5.6.3/webfonts/fa-solid-900.svg',
        //'./BGMS/BGMS/static/fonts/font-awesome-4.5.0/fonts/fontawesome-webfont.ttf?v=4.5.0',
        './BGMS/BGMS/static/fonts/bgms-font/style.css',
        './BGMS/BGMS/static/fonts/bgms-font/fonts/*.*',
        //'./BGMS/BGMS/static/fonts/font-awesome-4.5.0/fonts/fontawesome-webfont.*',
        './BGMS/BGMS/static/fonts/fertigo-pro/fertigo-pro.css',
        './BGMS/BGMS/static/fonts/fertigo-pro/webfonts/3200C0_0_0.woff2',
      ],
      stripPrefixMulti: {
        './BGMS/main/static/': '/',
        './BGMS/mapmanagement/static/': '/',
        './BGMS/BGMS/static/': '/',
      },
      verbose: false,
      version: Date.now(), // new version every time SW is generated, hence don't need to set this manually
                  // NOTE: this doesn't need to be incremental
    });
  },

};

gulp.task('clean', tasks.clean);
// individual tasks
// gulp.task('templates', req, tasks.templates);
// gulp.task('assets', tasks.assets);
gulp.task('mainsass', tasks.mainsass);
gulp.task('mapmanagementsass', tasks.mapmanagementsass);
gulp.task('mainsass_dev', tasks.mainsass_dev);
gulp.task('mapmanagementsass_dev', tasks.mapmanagementsass_dev);
gulp.task('dmsass_dev', tasks.dmsass_dev);
gulp.task('desass', tasks.desass);
gulp.task('admsass', tasks.admsass);
gulp.task('dmsass', tasks.dmsass);
gulp.task('lpsass', tasks.lpsass);
gulp.task('sass',gulp.parallel(['mainsass', 'mapmanagementsass', 'desass', 'admsass', 'dmsass', 'lpsass']));
gulp.task('mapvanjs',tasks.mapvanjs);
gulp.task('mapangjs',tasks.mapangjs);
gulp.task('mapauthangjs',tasks.mapauthangjs);
gulp.task('devanjs',tasks.devanjs);
gulp.task('deangjs',tasks.deangjs);
gulp.task('dmvanjs',tasks.dmvanjs);
gulp.task('scripts', gulp.parallel(['mapvanjs', 'mapangjs', 'mapauthangjs', 'devanjs', 'deangjs', 'dmvanjs']));
// gulp.task('lint:js', tasks.lintjs);
// gulp.task('optimize', tasks.optimize);
// gulp.task('test', tasks.test);

//Webpack tasks
gulp.task('webpack-staging', function() {
    return gulp.src('./bgms-vue/vue.config.js', {read: false})
    .pipe(shell('npm run build-staging --prefix bgms-vue'));
});

//Webpack tasks
gulp.task('webpack-production', function() {
    return gulp.src('./bgms-vue/vue.config.js', {read: false})
    .pipe(shell('npm run build-production --prefix bgms-vue'));
});

//Webpack tasks
gulp.task('webpack-development', function() {
    return gulp.src('./bgms-vue/vue.config.js', {read: false})
    .pipe(shell('npm run build-development --prefix bgms-vue'));
});

function minifySW(cb) {
  return pump([
        gulp.src(paths.serviceWorker, {base: './'}),
        uglify({ output: { comments: "some" } }),
        gulp.dest('./')
    ],
    cb
  );
}

exports.minifySW = minifySW;

// Use when modifying the service worker and you know you don't need to rebuild everything else
gulp.task('generateServiceWorker-dev', tasks.generateServiceWorker);

//var generateServiceWorkerAndMinify = gulp.series(['generateServiceWorker']);
gulp.task('generateServiceWorkerAndMinify', gulp.series(['generateServiceWorker-dev'], minifySW));

//npm tasks
gulp.task('npm-install', function() {
    return gulp.src(['./package.json', './bgms-vue/package.json'])
    .pipe(install());
});


// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init(
      // [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
      ['./BGMS/BGMS/static/js/*'], {
        proxy:  "localhost:8000"
    });
});

// --------------------------
// FIN TASK METHODS
// --------------------------


// --------------------------
// DEV/WATCH TASK
// --------------------------
// gulp.task('watch', ['assets', 'templates', 'sass', 'uglify', 'browser-sync'], function() {
gulp.task('watch1', gulp.series([uglify], function() {
  // --------------------------
  // watch:sass
  // --------------------------
  // gulp.watch('./client/scss/**/*.scss', ['reload-sass']);

  // --------------------------
  // watch:js
  // --------------------------
  gulp.watch('./BGMS/BGMS/static/js/*', ['lint:js', 'reload-js']);
  // --------------------------
  // watch:html
  // --------------------------
  // gulp.watch('./templates/**/*.html', ['reload-templates']);
  gutil.log(gutil.colors.bgGreen('Watching for changes...'));
}));


gulp.task('watch', function() {
  // gulp.watch('./BGMS/BGMS/static/js/*', ['uglify']).on("change", reload);
  // --------------------------
  // watch:js
  // --------------------------
  gulp.watch('./BGMS/BGMS/static/js/*', gulp.series(['scripts']));
  // --------------------------
  // watch:sass
  // --------------------------
  gulp.watch('./BGMS/BGMS/static/sass/**/*.scss', gulp.series(['mainsass_dev', 'mapmanagementsass_dev', 'dmsass_dev', 'admsass', 'desass']));
  // --------------------------
  // watch:ServiceWorker
  // --------------------------
  gulp.watch('./bgms-sw-generator/service-worker.tmpl', gulp.series(['generateServiceWorker-dev']));

  gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

gulp.task('watch-dev', function() {
  // --------------------------
  // watch:vue
  // --------------------------
  gulp.watch('./bgms-vue/src/**/*.vue', gulp.series(['webpack-development']));
  gulp.watch('./bgms-vue/src/**/*.ts', gulp.series(['webpack-development']));
  gulp.watch('./BGMS/BGMS/static/js/*', gulp.series(['scripts']));
  gulp.watch('./BGMS/BGMS/static/sass/**/*.scss', gulp.series(['mainsass_dev', 'mapmanagementsass_dev', 'dmsass_dev', 'admsass', 'desass']));
  gulp.watch('./bgms-sw-generator/service-worker.tmpl', gulp.series(['generateServiceWorker-dev']));
  gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

//vue-test
gulp.task('vue-test', function() {
    return gulp.src('./bgms-vue/package.json')
    .pipe(shell('npm run vue-test --prefix ./bgms-vue/'))
});

// build task
gulp.task('build-staging', gulp.series([
  // 'clean',
//   'templates',
  // 'assets',
  'npm-install',
  'sass',
  'scripts',
  'webpack-staging',
  'generateServiceWorker-dev',
  'vue-test',
]));

// build task
gulp.task('build-production', gulp.series([
  'npm-install',
  'sass',
  'scripts',
  'webpack-production',
  'generateServiceWorkerAndMinify'
]));

// build task
gulp.task('build-development', gulp.series([
  'npm-install',
  'sass',
  'scripts',
  'webpack-development',
  'generateServiceWorker-dev',
  'vue-test',
  'watch-dev',
]));

// Use when modifying the service worker and you know you don't need to rebuild everything else
gulp.task('generateServiceWorker-dev', tasks.generateServiceWorker);
