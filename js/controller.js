carPoolingApp.controller('chooseCtrl', function($scope, $http) {

    $scope.userList = [{
        "name": "Tommaso Berlose", 
        "address": "Via Otello Putinati 122, Ferrara",
        "alternative_address": "",
        "maxDur": "0",
        "notWith": "",
        "selected": "false"}
        ];
/*
    if ($scope.search == "") {
        $scope.data = $scope.userList;
    } else {
        for (var i = 0; i < userList.length; i++) {
            if ((userList[i].name).contains($scope.search))
                $scope.data.append(userList[i]);
        };
    }
/*
    $http.get("http://www.w3schools.com/angular/customers.php")
    .success(function(response) {$scope.userList = response.records;});
    *//*
    $scope.addPerson = true;
    if ($scope.userList.length == 0) 
        $scope.addPerson = false;
*/
    $scope.toggleAddPerson = function() {
        $scope.addPerson = !$scope.addPerson;
    };

    /*
        {
        name: $scope.nameInput, 
        address: $scope.addressInput,
        alternative_address: $scope.alternativeAddress,
        max_dur: $scope.maxDur,
        not_with: $scope.notWith,
        selected: false
        }
    

    $scope.userAdd = function() {
        var user = {
            name: $scope.nameInput, 
            address: $scope.addressInput,
            alternative_address: $scope.alternativeAddress,
            max_dur: $scope.maxDur,
            not_with: $scope.notWith,
            selected: false
        };
        $scope.nameInput = ""; 
        $scope.addressInput = "";
        $scope.alternativeAddress = "";
        $scope.maxDur = "";
        $scope.notWith = "";

        $scope.userList.push(user);
    };

    $scope.userEdit = function() {
        $scope.userList.push({todoText:$scope.todoInput, done:false});
    };

    $scope.userRemove = function() {
        $scope.userList.push({todoText:$scope.todoInput, done:false});
    };*/
});
