app.controller('chooseCtrl', function($scope) {
    $scope.userList = [
        {
            name: "Tommaso", 
            address: "Via Otello Putinati 122, Ferrara",
            alternative_address: "",
            max_dur: 0,
            not_with: "",
            selected: false}
    ];
    /*
    $scope.hideUpload = false;

    $scope.hideUpload = function() {
        $scope.hideUpload = true;
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