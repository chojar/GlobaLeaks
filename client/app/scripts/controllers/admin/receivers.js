GLClient.controller('AdminReceiversCtrl', ['$scope', '$modal',
function($scope, $modal) {

  $scope.save_receiver = function(receiver) {

    if (receiver.gpg_key_remove == true) {
      receiver.gpg_key_armor = '';
    }

    if (receiver.gpg_key_armor !== undefined &&
        receiver.gpg_key_armor != '') {
      receiver.gpg_key_remove = false;
    }

    var updated_receiver = new $scope.admin.receiver(receiver);

    return $scope.update(updated_receiver);

  }

  $scope.save_all = function () {
    angular.forEach($scope.admin.receivers, function (receiver, key) {
      $scope.save_receiver(receiver);
    });
  };

  $scope.perform_delete = function(receiver) {
    var idx = _.indexOf($scope.admin.receivers, receiver);

    receiver['$delete'](function(){
      $scope.admin.receivers.splice(idx, 1);
    });

  };

  $scope.receiverDeleteDialog = function(receiver){
    var modalInstance = $modal.open({
        templateUrl:  'views/partials/receiver_delete.html',
        controller: 'ConfirmableDialogCtrl',
        resolve: {
          object: function () {
            return receiver;
          }
        }

    });

    modalInstance.result.then(
       function(result) { $scope.perform_delete(result); },
       function(result) { }
    );
  };

  $scope.sortableOptions = {
    stop: function(e, ui) {
      $scope.update_receivers_order();
    }
  };

  $scope.reorder_receivers_alphabetically = function () {
    $scope.admin.receivers = _($scope.admin.receivers).sortBy(function (receiver) {
      return receiver.name;
    });

    $scope.update_receivers_order();

    $scope.save_all();
  };

  $scope.update_receivers_order = function() {
    var i = 0;
    angular.forEach($scope.admin.receivers, function(receiver, key) {
        receiver.presentation_order = i + 1;
        i += 1;
    });
  }

}]);

GLClient.controller('AdminReceiversEditorCtrl', ['$scope', 'passwordWatcher', 'CONSTANTS',
  function($scope, passwordWatcher, CONSTANTS) {

    $scope.timezones = CONSTANTS.timezones;

    passwordWatcher($scope, 'receiver.password');

    $scope.editing = false;

    $scope.toggleEditing = function () {
      $scope.editing = $scope.editing ^ 1;
    };

    $scope.isSelected = function (context) {
      return $scope.receiver.contexts.indexOf(context.id) !== -1;
    };

    $scope.toggle = function (context) {
      var idx = $scope.receiver.contexts.indexOf(context.id);
      if (idx === -1) {
        $scope.receiver.contexts.push(context.id);
      } else {
        $scope.receiver.contexts.splice(idx, 1);
      }
    };

}]);

GLClient.controller('AdminReceiverAddCtrl', ['$scope', 'passwordWatcher',
  function($scope, passwordWatcher) {

    $scope.new_receiver = {};

    $scope.add_receiver = function() {
      receiver = new $scope.admin.new_receiver();

      receiver.name = $scope.new_receiver.name;
      receiver.mail_address = $scope.new_receiver.email;

      receiver.$save(function(new_receiver){
        $scope.admin.receivers.push(new_receiver);
        $scope.new_receiver = {};
      });
    }

}]);
