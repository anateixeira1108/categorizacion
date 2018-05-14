'use strict';
/**
 * Iniciando Configuracion de angular
 */
var coreApp = angular.module(
    'coreApp', 
    [
        'ngRoute', 
        'ngUpload', 
        'ngCookies', 
        'ui.utils', 
        'ui.bootstrap', 
        'cargar-requisitos',
        'control-tabulador',
        '$strap.directives',
    ]);

coreApp.config(['$interpolateProvider', '$provide', '$filterProvider', '$compileProvider', '$controllerProvider', '$sceProvider'
    , function ($interpolateProvider, $provide, $filterProvider, $compileProvider, $controllerProvider, $sceProvider) {
        coreApp.register = {
            controller: $controllerProvider.register,
            directive: $compileProvider.directive,
            filter: $filterProvider.register,
            factory: $provide.factory,
            service: $provide.service
        };

        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
        $sceProvider.enabled(false);
    }
]);


coreApp.config(['$httpProvider', function ($httpProvider) {
    // Use x-www-form-urlencoded Content-Type
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    // Override $http service's default transformRequest
    $httpProvider.defaults.transformRequest = [function (data) {
        /**
         * The workhorse; converts an object to x-www-form-urlencoded serialization.
         * @param {Object} obj
         * @return {String}
         */
        var param = function (obj) {
            var query = '';
            var name, value, fullSubName, subName, subValue, innerObj, i;

            for (name in obj) {
                value = obj[name];

                if (value instanceof Array) {
                    for (i = 0; i < value.length; ++i) {
                        subValue = value[i];
                        fullSubName = name + '[' + i + ']';
                        innerObj = {};
                        innerObj[fullSubName] = subValue;
                        query += param(innerObj) + '&';
                    }
                } else if (value instanceof Object) {
                    for (subName in value) {
                        subValue = value[subName];
                        fullSubName = name + '[' + subName + ']';
                        innerObj = {};
                        innerObj[fullSubName] = subValue;
                        query += param(innerObj) + '&';
                    }

                } else if (value !== undefined && value !== null) {
                    query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
                }
            }

            return query.length ? query.substr(0, query.length - 1) : query;
        };

        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];

}]);

coreApp.run(function ($rootScope, $templateCache) {
    $rootScope.$on('$viewContentLoaded', function () {
        $templateCache.removeAll();
    });

    $rootScope.patterns = {
        rif: /^[JGVEP][-][0-9]{8}[-][0-9]$/,
        telefono: /^[0-9]{4}-?[0-9]{7}$/,
        cedula: /^[VE]-?([0-9]{6,8})$/,
        postal: /^[0-9]{4}$/
    }
    $rootScope.MESES = {
        Ene: '01', Feb: '02', Mar: '03', Abr: '04', May: '05', Jun: '06',
        Jul: '07', Ago: '08', Sep: '09', Oct: '10', Nov: '11', Dic: '12'
    };
    _.str.include('Underscore.string', 'string');

});

coreApp.factory('sharedService', function ($rootScope) {
    return {
        broadcast: function (data, type) {
            $rootScope.$broadcast('broadcastHandler', data, type);
        }
    };
});


coreApp.factory('safeApply', function ($rootScope) {
    return function ($scope, fn) {
        var phase = $scope.$root.$$phase;
        if (phase == '$apply' || phase == '$digest') {
            if (fn) {
                $scope.$eval(fn);
            }
        } else {
            if (fn) {
                $scope.$apply(fn);
            } else {
                $scope.$apply();
            }
        }
    }
});

coreApp.factory('windowLocationOrigin', function ($rootScope, $window) {
    var origin = window.location.origin;
    if (!window.location.origin) {
        origin = $window.location.protocol + "//" + $window.location.hostname + ($window.location.port ? ':' + $window.location.port : '');
    }
    return origin;
});


/**
 * Finalizando Configuracion de angular
 */

//Directivas
coreApp.directive('testDirective', function ($parse, $log) {
    return {
        link: function (scope, elem, attrs) {
            // $log.info("test de prueba... imprimiendo por consola");
            // $log.info(elem);
            // $log.info(scope);
        }
    };
});

//directva para numeros positivos numbers-only
coreApp.directive('numbersOnly', function ($parse) {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, modelCtrl) {
            modelCtrl.$parsers.push(function (inputValue) {
                if (inputValue == undefined) return ''
                var transformedInput = inputValue.replace(/[^0-9]/g, '');
                if (transformedInput != inputValue) {
                    modelCtrl.$setViewValue(transformedInput);
                    modelCtrl.$render();
                }

                return transformedInput;
            });
        }
    };
});

//directiva para validar que el archivo sea requerido valid-file
coreApp.directive('validFile', function () {
    return {
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue(el.val());
                    ngModel.$render();
                });
            });
        }
    }
});

coreApp.directive('telMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            el.inputmask('9999-9999999');
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue(el.val());
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('zipMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            el.inputmask('9999');
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue(el.val());
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('rifMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            $.extend($.inputmask.defaults.definitions, {
                'r': {
                    'validator': '[jgvepJGVEP]',
                    'cardinality': 1,
                    'casing': 'upper',
                    'prevalidator': null
                }
            });
            el.inputmask('r-999999[9][9]-9', {placeholder: '', showMaskOnHover: false});
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue(_.str.capitalize(el.val()));
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('ciMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            $.extend($.inputmask.defaults.definitions, {
                'c': {
                    'validator': '[veVE]', 'cardinality': 1,
                    'casing': 'upper', 'prevalidator': null
                }
            });
            el.inputmask('c-999999[9][9]', {placeholder: ''});
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue(_.str.capitalize(el.val()));
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('moneyFormat', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attrs, ngModel) {
            elem.bind('change', function () {
                scope.$apply(function () {
                    var num = _.str.toNumber(elem[0].value.replace(",", "."), 2)
                    ngModel.$setViewValue(_.str.numberFormat(num, 2, ',', '.'));
                    ngModel.$render();
                });
            });
            elem.bind('click', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue("");
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('numberFormat', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attrs, ngModel) {
            elem.bind('change', function () {
                scope.$apply(function () {
                    var num = _.str.toNumber(elem[0].value.replace(",", "."), 2)
                    ngModel.$setViewValue(_.str.numberFormat(num, "", ',', '.'));
                    ngModel.$render();
                });
            });
            elem.bind('click', function () {
                scope.$apply(function () {
                    ngModel.$setViewValue("");
                    ngModel.$render();
                });
            });
        }
    };
});


//directva para eliminar caracteres especiales none-special-character
coreApp.directive('noneSpecialCharacter', function ($parse) {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, modelCtrl) {
            modelCtrl.$parsers.push(function (inputValue) {
                if (inputValue == undefined) return ''
                var transformedInput = inputValue.replace(/[^a-zA-Z 0-9.,-\\& $]+/g, '');
                if (transformedInput != inputValue) {
                    modelCtrl.$setViewValue(transformedInput);
                    modelCtrl.$render();
                }

                return transformedInput;
            });
        }
    };
});

//directva para eliminar caracteres especiales none-special-character
coreApp.directive('onlyCharacter', function ($parse) {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, modelCtrl) {
            modelCtrl.$parsers.push(function (inputValue) {
                if (inputValue == undefined) return ''
                var transformedInput = inputValue.replace(/[^a-zA-ZñÑ\s\W $]+/g, '');
                if (transformedInput != inputValue) {
                    modelCtrl.$setViewValue(transformedInput);
                    modelCtrl.$render();
                }

                return transformedInput;
            });
        }
    };
});


coreApp.directive('moneyMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            el.inputmask('9[9][9][9][9][9][9][.9[9]]', {placeholder: '', showMaskOnHover: true});
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$render();
                });
            });
        }
    };
});

coreApp.directive('dateMask', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, el, attrs, ngModel) {
            el.inputmask('dd/mm/yyyy', {placeholder: '', onBeforeMask: function(value) { 
                return ($(this).attr('value') || value).trim();
            }});
            el.bind('change', function () {
                scope.$apply(function () {
                    ngModel.$render();
                });
            });
        }
    };
});



