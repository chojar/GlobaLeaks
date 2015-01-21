'use strict';

var translations = {
 GLOBALEAKS: "{{NodeName}} makes use of GlobaLeaks software specifically designed to protect the identity of the submitter and of the receiver in the exchange of leaked materials."
};

var GLClient = angular.module('GLClient', [
    'ngRoute',
    'ui.bootstrap',
    'ui.sortable',
    'ang-drag-drop',
    'monospaced.elastic',
    'resourceServices',
    'submissionUI',
    'blueimp.fileupload',
    'pascalprecht.translate',
    'GLClientFilters'
  ]).
  config(['$routeProvider', '$translateProvider', '$tooltipProvider',
    function($routeProvider, $translateProvider, $tooltipProvider) {

    $routeProvider.
      when('/wizard', {
        templateUrl: 'views/wizard/main.html',
        controller: 'WizardCtrl',
        header_title: 'GlobaLeaks Wizard',
        header_subtitle: 'Step-by-step setup'
      }).
      when('/submission', {
        templateUrl: 'views/submission/main.html',
        controller: 'SubmissionCtrl',
        header_title: 'Blow the Whistle',
        header_subtitle: ''
      }).
      when('/receipt', {
        templateUrl: 'views/submission/receipt.html',
        controller: 'ReceiptController',
        header_title: 'Submission successfully completed!',
        header_subtitle: 'Write down your keycode'
      }).
      when('/status/:tip_id', {
        templateUrl: 'views/receiver/tip.html',
        controller: 'StatusCtrl',
        header_title: 'Receiver Interface',
        header_subtitle: 'Tip Status Page'
      }).
      when('/status', {
        templateUrl: 'views/whistleblower/tip.html',
        controller: 'StatusCtrl',
        header_title: 'Whistleblower Interface',
        header_subtitle: 'Tip Status Page'
      }).
      when('/receiver/firstlogin', {
        templateUrl: 'views/receiver/firstlogin.html',
        controller: 'ReceiverFirstLoginCtrl',
        header_title: 'Receiver First Login',
        header_subtitle: ''
      }).
      when('/receiver/preferences', {
        templateUrl: 'views/receiver/preferences.html',
        controller: 'ReceiverPreferencesCtrl',
        header_title: 'Receiver Interface',
        header_subtitle: 'Preferences'
      }).
      when('/receiver/tips', {
        templateUrl: 'views/receiver/tips.html',
        controller: 'ReceiverTipsCtrl',
        header_title: 'Receiver Interface',
        header_subtitle: 'Your Tips'
      }).
      when('/receiver/activities', {
        templateUrl: 'views/receiver/activities.html',
        controller: 'ReceiverNotificationCtrl',
        header_title: 'Receiver Interface',
        header_subtitle: 'Recent Activities'
      }).
      when('/admin/landing', {
        templateUrl: 'views/admin/landing.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Landing Page'
      }).
      when('/admin/content', {
        templateUrl: 'views/admin/content.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Content Settings'
      }).
      when('/admin/contexts', {
        templateUrl: 'views/admin/contexts.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Contexts Configuration'
      }).
      when('/admin/fields', {
        templateUrl: 'views/admin/fields.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Fields Configuration'
      }).
      when('/admin/receivers', {
        templateUrl: 'views/admin/receivers.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Receivers Configuration'
      }).
      when('/admin/mail', {
        templateUrl: 'views/admin/mail.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Mail Configuration'
      }).
      when('/admin/advanced_settings', {
        templateUrl: 'views/admin/advanced.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Advanced Settings'
      }).
      when('/admin/password', {
        templateUrl: 'views/admin/password.html',
        controller: 'AdminCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Password Configuration'
      }).
      when('/admin/overview/users', {
        templateUrl: 'views/admin/users_overview.html',
        controller: 'OverviewCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Users Overview'
      }).
      when('/admin/overview/tips', {
        templateUrl: 'views/admin/tips_overview.html',
        controller: 'OverviewCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Tips Overview'
      }).
      when('/admin/overview/files', {
        templateUrl: 'views/admin/files_overview.html',
        controller: 'OverviewCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Files Overview'
      }).
      when('/admin/anomalies', {
        templateUrl: 'views/admin/anomalies.html',
        controller: 'AnomaliesCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Anomalies'
      }).
      when('/admin/stats', {
        templateUrl: 'views/admin/stats.html',
        controller: 'StatisticsCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'System Stats'
      }).
      when('/admin/activities', {
        templateUrl: 'views/admin/activities.html',
        controller: 'ActivitiesCtrl',
        header_title: 'Administration Interface',
        header_subtitle: 'Recent Activities'
      }).
      when('/admin', {
        templateUrl: 'views/admin.html',
        controller: 'LoginCtrl',
        header_title: 'Login',
        header_subtitle: ''
      }).
      when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl',
        header_title: 'Login',
        header_subtitle: ''
      }).
      when('/start', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        header_title: '',
        header_subtitle: ''
      }).
      when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        header_title: '',
        header_subtitle: ''
      }).
      otherwise({
        redirectTo: '/'
      });

      $translateProvider.useStaticFilesLoader({
        prefix: 'l10n/',
        suffix: '.json'
      });

      $tooltipProvider.options( {appendToBody: true} );
}]).
  run(['$http', '$rootScope', '$route', 'Authentication', function ($http, $rootScope, $route, Authentication) {

     var globaleaksRequestInterceptor = function(data, headers) {

        headers = angular.extend(headers(), Authentication.headers());

        return data;
    };

    $http.defaults.transformRequest.push(globaleaksRequestInterceptor);

    function overrideReload(e) {
       if (((e.which || e.keyCode) == 116) || /* F5 */
           ((e.which || e.keyCode) == 82 && (e.ctrlKey || e.metaKey))) {  /* (ctrl or meta) + r */ 
           e.preventDefault();
           $rootScope.$broadcast("REFRESH");
       }
    };

    $(document).bind("keydown", overrideReload);

    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        if (current.$$route) {
          $rootScope.header_title = current.$$route.header_title;
          $rootScope.header_subtitle = current.$$route.header_subtitle;
          $rootScope.errors = [];
        }
    });

    document.cookie = 'cookiesenabled=true;';
    if (document.cookie == "") {
      $rootScope.cookiesEnabled = false;
    } else {
      $rootScope.cookiesEnabled = true;
      $.removeCookie('cookiesenabled');
    }

    /* initialization of privacy detection variables */
    $rootScope.privacy = 'unknown';
    $rootScope.anonymous = false;
}]);
