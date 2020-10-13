(function() {
  "use strict";

  angular.module("BettingApp", ['ngSanitize']).controller("BettingController", [
    "$scope",
    "$log",
    "$http",
    "$timeout",
    function($scope, $log, $http, $timeout) {
      $scope.submitButtonText = 'Submit'
      // $scope.loading = false;
      // $scope.lineerror = false;
      // function getOdds(jobID) {
      //   var timeout = "";
    
      //   var poller = function() {
      //     $http.get('/results/'+jobID).
      //     success(function(data, status, headers, config) {
      //       if(status === 202){
      //         $log.log(data,status);
      //       } else if (status === 200){
      //         $log.log(data);
      //         $scope.loading = false;
      //         $scope.submitButtonText = "Submit";
      //         $scope.dataResults = data
      //         $timeout.cancel(timeout);
      //         return false;
      //       }
      //       timeout = $timeout(poller, 2000)
      //     }).
      //     error(function(error){
      //       $log.log(error);
      //       $scope.loading = false;
      //       $scope.submitButtonText = "Submit"
      //       $scope.lineerror = true;
      //     });
      //   };
      //   poller();
      // }

      // //Gets called first when the button is clicked
      // $scope.getResults = function() {
      //   var userInput = $scope.radio;
      //   if(userInput != 'NFL' && userInput != 'CFB'){
      //     userInput = 'NFL'
      //   }
      //   $http.post('/start', {'radio': userInput}).success(function(results){
      //       $log.log(results);
      //       getOdds(results)
      //       $scope.lineerror = false;
      //       $scope.dataResults = null;
      //       $scope.loading = true;
      //       $scope.submitButtonText = 'Loading...'
      //   }).
      //   error(function(error){
      //       $log.log(error);
      //   });
      // };

      $scope.queryResults = function() {
        $log.log("1")
        var userInput = $scope.radio;
         $log.log(userInput)
        if(userInput != 'NFL' && userInput != 'CFB'){
          userInput = 'NFL'
        }
        $http.post('/getLines', {'radio': userInput}).success(function(results){
          $scope.dataResults = results
        }).error(function(err){
          $log.log(err)
        });
      };

    }
  ]);
})();
