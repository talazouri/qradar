(function(){


var qguard = angular.module("qguard" ,['ngRoute',"mainCtrl"] );


    qguard.config(["$routeProvider","$interpolateProvider", function($routeProvider,$interpolateProvider) {
        $routeProvider.
        when('/chooseAssets', {
            templateUrl:"/templates/chooseAssets.html",
             controller:"chooseAssets"
        }).
        when('/analyzedAssets', {
            templateUrl:"/templates/analyzedAssets.html"
            // controller:"analyzedAssets"
        })
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

    }]);

}());


