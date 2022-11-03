
var defaults = require('lodash.defaults');
var fs = require('fs');
var glob = require('glob');
var mkdirp = require('mkdirp');
var path = require('path');
var prettyBytes = require('pretty-bytes');
var template = require('lodash.template');
var util = require('util');

function absolutePath(relativePath) {
  return path.resolve(process.cwd(), relativePath);
}

function getFileAndSizeForFile(file) {
  var stat = fs.statSync(file);

  if (stat.isFile()) {
    var buffer = fs.readFileSync(file);
    return {
      file: file,
      size: stat.size
    };
  }

  return null;
}

function getFilesAndSizesForGlobPattern(globPattern, excludeFilePath) {
  return glob.sync(globPattern.replace(path.sep, '/')).map(function(file) {
    // Return null if we want to exclude this file, and it will be excluded in
    // the subsequent filter().
    return excludeFilePath === absolutePath(file) ?
      null :
      getFileAndSizeForFile(file);
  }).filter(function(fileAndSize) {
    return fileAndSize !== null;
  });
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function generate(params, callback) {
  return new Promise(function(resolve, reject) {
    params = defaults(params || {}, {
      logger: console.log,
      maximumFileSizeToCacheInBytes: 2 * 1024 * 1024, // 2MB
      replacePrefix: '',
      staticFileGlobs: [],
      stripPrefix: '',
      stripPrefixMulti: {},
      templateFilePath: path.join(path.dirname(fs.realpathSync(__filename)), 'service-worker.tmpl'),
      verbose: false,
      version: 1,
    });

    // var relativeUrlToHash = {};
    var relativeUrls = [];
    var cumulativeSize = 0;
    params.stripPrefixMulti[params.stripPrefix] = params.replacePrefix;

    params.staticFileGlobs.forEach(function(globPattern) {
      var filesAndSizes = getFilesAndSizesForGlobPattern(globPattern, params.outputFilePath);

      filesAndSizes.forEach(function(fileAndSize) {
        if (fileAndSize.size <= params.maximumFileSizeToCacheInBytes) {
          var relativeUrl = fileAndSize.file
            .replace(
              new RegExp('^(' + Object.keys(params.stripPrefixMulti)
                  .map(escapeRegExp).join('|') + ')'),
              function(match) {
                return params.stripPrefixMulti[match];
              })
            .replace(path.sep, '/');

          relativeUrls.push(relativeUrl);
          if (params.verbose) {
            params.logger(
              util.format(
                'Caching static resource "%s" (%s)',
                fileAndSize.file,
                prettyBytes(fileAndSize.size)
              )
            );
          }

          cumulativeSize += fileAndSize.size;

        } else {
          params.logger(
            util.format(
              'Skipping static resource "%s" (%s) - max size is %s',
              fileAndSize.file,
              prettyBytes(fileAndSize.size),
              prettyBytes(params.maximumFileSizeToCacheInBytes)
            )
          );
        }
      });

    });

    // It's very important that running this operation multiple times with the same input files
    // produces identical output, since we need the generated service-worker.js file to change if
    // the input files changes. The service worker update algorithm,
    // https://w3c.github.io/ServiceWorker/#update-algorithm, relies on detecting even a single
    // byte change in service-worker.js to trigger an update. Because of this, we write out the
    // cache options as a series of sorted, nested arrays rather than as objects whose serialized
    // key ordering might vary.
    var precacheConfig = relativeUrls.sort().map(function(relativeUrl) {
      var url = relativeUrl.charAt(0) === '/' ? relativeUrl.substr(1) : relativeUrl;
      return "{% static '" + url + "' %}";
    });

    params.logger(
      util.format(
        'Total precache size is about %s for %d resources.',
        prettyBytes(cumulativeSize),
        relativeUrls.length
      )
    );

    fs.readFile(params.templateFilePath, 'utf8', function(error, data) {
      if (error) {
        if (callback) {
          callback(error);
        }

        return reject(error);
      }

      var populatedTemplate = template(data)({
        precacheConfig: JSON.stringify(precacheConfig, null, 2),
        version: params.version,
      });

      if (callback) {
        callback(null, populatedTemplate);
      }

      resolve(populatedTemplate);
    });

  });
}

function write(filePath, params, callback) {
  return new Promise(function(resolve, reject) {
    function finish(error, value) {
      if (error) {
        reject(error);
      } else {
        resolve(value);
      }

      if (callback) {
        callback(error, value);
      }
    }

    mkdirp.sync(path.dirname(filePath));

    // Keep track of where we're outputting the file to ensure that we don't
    // pick up a previously written version in our new list of files.
    // See https://github.com/GoogleChrome/sw-precache/issues/101
    params.outputFilePath = absolutePath(filePath);

    generate(params).then(function(serviceWorkerFileContents) {
      fs.writeFile(filePath, serviceWorkerFileContents, finish);
    }, finish);
  });
}

module.exports = {
  generate: generate,
  write: write
};
