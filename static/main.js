(function () {
  'use strict';

  angular.module('PheRS', [])

  .controller('PheRS_Controller', ['$scope', '$log', '$http',
  function($scope, $log, $http) {

  $scope.getResults = function() {

    
    var disease = $scope.diseaseSelect;
    var icd9s = $scope.icd9Select;

    // fire the API request
    $http.post('/get_input', {"disease": disease,"icd9s":icd9s}).
      then(function(results) {
        $scope.results=results.data;
        $log.log(results.data);
      },function(error) {
        $log.log(error);
      });

  };
  return $scope.results;

}
]);

}());