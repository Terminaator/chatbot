function clearfield() {
    document.getElementById("ifield").value = "";
}



(function () {
    let app = angular.module("chatbot", []);

    let MainController = function ($scope, $http,) {
        $scope.message = "kana";
        let answer = {"answer": "Tere, mina olen ÕIS2 chatbot! Abi saamiseks kirjuta help"};
        $scope.questions = [];
        $scope.questions.push([answer, "False"]);
        let container = $(".container");
        $scope.addItem = function () {
            let question = document.getElementById('ifield').value;
            document.getElementById('ifield').hidden = true;
            clearfield();
            if (question.length !== 0) {
                $scope.questions.push([question, 'True']);
                let dataobject = {
                    question: question
                };

                $http({
                    method: 'POST',
                    url: 'api/question',
                    data: dataobject,
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': 'true',
                        "X-Requested-With": "XMLHttpRequest",
                    }
                }).then(function (response) {
                        $scope.questions.push([response.data, 'False']);
                        container.stop().animate({scrollTop: container[0].scrollHeight}, 100);
                    },
                    function () {
                        let answer = {"answer": "Ma tõesti ei tea. "};
                        $scope.questions.push([answer, 'False']);
                        container.stop().animate({scrollTop: container[0].scrollHeight}, 100)
                    }
                );
            }

        };

    };
    app.controller("MainController", MainController);
}());