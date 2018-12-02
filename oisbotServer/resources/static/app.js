function clearfield() {
    document.getElementById("ifield").value = "";
}

(function(){
        var app = angular.module("chatbot", []);

        var MainController = function($scope, $http,){
            $scope.message = "kana";
            var answer = {"answer":"Tere, mina olen ÕIS2 chatbot! Abi saamiseks kirjuta help"};
            $scope.questions = [];
            $scope.questions.push([answer, "False"]);
            var container = $(".container");
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
                // document.getElementsByTagName('img') .attr("src", 'https://i.redd.it/vc9207gbcr121.png');

                $scope.questions.push([response.data,'False']);
                container.stop().animate({ scrollTop: container[0].scrollHeight}, 100);

            },
            function(response){
                var answer = {"answer":"Ma tõesti ei tea. "};
                $scope.questions.push([answer,'False']);
                container.stop().animate({ scrollTop: container[0].scrollHeight}, 100)
            }
            );
        };

        };
        app.controller("MainController", MainController);
    }());