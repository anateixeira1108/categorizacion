/* Angular Test for file upload */
(function(){ 
  
  var app = angular.module('cargar-requisitos', ['ngUpload']);

  app.controller(
    'ShowLoadedController',
    ['$scope', 
      function ($scope) {
        $scope.fileNameChanged = function(elem, flag){
          console.log(elem);
          if(flag=="doc"){
            $(
              $(
                elem
              ).parent(
                '.zona-iconos'
              ).siblings(
                '.nombre-requisito'
                ).get(0)
            ).children('.icono-carga-realizada').remove();

            $(
              $(
                elem
              ).parent(
                '.zona-iconos'
              ).siblings(
                '.nombre-requisito'
                ).get(0)
            ).append('<span class ="icono-carga-realizada">\
              &nbsp;&nbsp;&nbsp;</span>\
              <i \
              rel = "tooltip" \
              data-toggle="tooltip" \
              title="Ya ha sido cargado" \
              class="fa fa-check icono-carga-realizada icono-accion" \
              style="color:green;"\
              ></i>');

            $("[rel='tooltip']").tooltip();
        }
      }
      }
    ]
  );  
})();