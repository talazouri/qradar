(function() {

    var mainCtrl = angular.module('mainCtrl',[]);

    mainCtrl.controller('chooseAssets',['$scope','$http',function($scope,$http){
        $scope.SendData = function() {
            $http({
                url: 'rest/assets',
                method: "GET",
                headers: {'Content-Type': 'application/json'},
                params: {task_id:1}
            }).success(function (data) {
                console.log(data)
            });
        }
    }]);

}());