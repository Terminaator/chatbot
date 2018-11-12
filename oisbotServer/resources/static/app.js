function clearfield() {
    document.getElementById("ifield").value = "";
}

(function(){
        var app = angular.module("chatbot", []);

        var MainController = function($scope, $http,){
            $scope.message = "kana";
            var answer = {"answer":"Tere, mina olen ÕIS2 resources! Abi saamiseks kirjuta help"};
            $scope.questions = [];
            $scope.questions.push([answer, "False"]);

            $scope.addItem = function(question){
                clearfield();
            $scope.questions.push([question,'True']);
            var dataobject = {
                question: question
            };
             $http({
               method: 'POST',
               url: 'api/question',
               data: dataobject,
               headers: {
                   'Content-Type':  'application/json',
                   'Access-Control-Allow-Origin': 'true',
                    "X-Requested-With": "XMLHttpRequest",

               }
            }).then(function(response){
                var preanswer = response;
                var a = preanswer.toString().split("\n");
                var f = "";
                for (let l in a){
                    f +=l + "<br>"
                     }
                $scope.answer = f;

                $scope.questions.push([response.data,'False']);

            },
            function(response){
                var answer = {"answer":"Ma tõesti ei tea. "};
                $scope.questions.push([answer,'False']);
            }
            );
        };

        };
        app.controller("MainController", MainController);
    }());