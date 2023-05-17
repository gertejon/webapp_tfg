$(document).ready(function() {
    $('#instrumentFilter').on('submit', function(e) {
      e.preventDefault(); // Evita el envío del formulario
  
      // Obtén los valores seleccionados en los filtros
      var quality = $('#quality').val();
      var brand = $('#brand').val();

      // getting url parameter
      var type_name = window.location.pathname.split('/').pop();

      // Realiza una petición AJAX para obtener los resultados filtrados
      $.ajax({
        url: '/instruments/' + type_name + '/',
        method: 'GET',
        data: {
          quality: quality,
          brand: brand
        },
        success: function(data) {
          // Actualiza la sección de resultados en tu página con los productos filtrados
          $('#product-results').html(data);
        },
        error: function(xhr, textStatus, errorThrown) {
          // Maneja los errores si es necesario
          console.error(errorThrown);
        }
      });
    });
});
  