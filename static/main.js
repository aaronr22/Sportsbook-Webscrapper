(function() {
  "use strict";




  angular.module("BettingApp", ['ngSanitize']).controller("BettingController", [
    "$scope",
    "$log",
    "$http",
    "$timeout",
    function($scope, $log, $http, $timeout) {
      function getOdds(jobID) {
        var timeout = "";
    
        var poller = function() {
          $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202){
              $log.log(data,status);
            } else if (status === 200){
              $log.log(data);
              $scope.dataResults = data
              $timeout.cancel(timeout);
              return false;
            }
            timeout = $timeout(poller, 2000)
          });
        };
        poller();
      }


      $scope.getResults = function() {
        $log.log("world");

        $http.post('/start').success(function(results){
            $log.log(results);
            getOdds(results)
        }).
        error(function(error){
            $log.log(error);
        });
      };
    }
  ]);
})();
