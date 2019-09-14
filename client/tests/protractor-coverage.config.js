var istanbul = require("istanbul");
var collector = new istanbul.Collector();

var fs = require("fs");
var specs = JSON.parse(fs.readFileSync("tests/specs.json"));

// The test directory for downloaded files
var tmpDir = "/tmp/globaleaks-downloads";

exports.config = {
  framework: "jasmine",

  baseUrl: "http://127.0.0.1:8082/",

  troubleshoot: false,
  rootElement: 'html',
  directConnect: true,

  params: {
    "testFileDownload": true,
    "verifyFileDownload": false,
    "tmpDir": tmpDir
  },

  specs: specs,

  capabilities: {
    "browserName": "chrome",
    "chromeOptions": {
      args: ["--window-size=1280,1024"],
      prefs: {
        "download": {
          "prompt_for_download": false,
          "default_directory": tmpDir
        }
      }
    }
  },

  allScriptsTimeout: 60000,

  jasmineNodeOpts: {
    isVerbose: true,
    includeStackTrace: true,
    defaultTimeoutInterval: 60000
  },

  plugins: [
    {
      package: "protractor-console-plugin",
      failOnWarning: false,
      failOnError: false,
      logWarnings: true,
      exclude: []
    },
    {
      inline: {
        postTest: async function() {
          await browser.driver.executeScript("return __coverage__;").then(function(coverageResults) {
            collector.add(coverageResults);
          });
        }
      }
    }
  ],

  onPrepare: function() {
    browser.gl = {
      "utils": require("./utils.js"),
      "pages": require("./pages.js")
    };

    browser.addMockModule("disableTooltips", function() {
      angular.module("disableTooltips", []).config(["$uibTooltipProvider", function($uibTooltipProvider) {
        $uibTooltipProvider.options({appendToBody: true, trigger: "none", enable: false});
        $uibTooltipProvider.options = function() {};
      }]);
    });
  },

  onComplete: async function() {
    await browser.driver.executeScript("return __coverage__;").then(function(coverageResults) {
      collector.add(coverageResults);

      istanbul.Report.create("lcov", {
        dir: "coverage/",
        includeAllSources: true
      }).writeReport(collector, true);
    });
  }
};
