function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

document.addEventListener("DOMContentLoaded", () => {
    new ClipboardJS('.code-btn');

    $('#grub-form').submit( function (e) {
        // Получаем грабберы
        var grubbers = [];
        $('.input_checkbox:checkbox:checked').each(function () {
            grubbers.push($(this).val());
        });

        // Получаем тип пейлоада
        var payloadType = '';
        $("[aria-selected=true]").val(function() {
            payloadType = $(this).attr("aria-controls");
        });

        // Запрашиваем пейлоад
        $.ajax({
          url: '/api/makePayload',
          method: 'POST',
          dataType: 'json',
          data: JSON.stringify({
              'grubbers': grubbers,
              'payload_type': payloadType
          }),
          success: function(data) {
              if(data['success'])
                  $("#code-" + payloadType).text(data['payload']);
              else
                  alert('Error: ' + data['error']);
          }
        });

        e.preventDefault();
    });

    $('#btnDeleteAll').click(function (e) {
        $.ajax({
          url: '/api/delete',
          method: 'POST',
          dataType: 'json',
          data: JSON.stringify({'action': 'delete_all'}),
          success: function(data) {
              if(data['success'])
                  document.location.reload();
              else
                  alert('Error: ' + data['error']);
          }
        });
    });

    $('#btnDownloadDOM').click(function (e) {
        var content = $("#domContent").text();
        download("dom.html", content);
    });

    $('a[id^="btnDeleteEvent"]').on('click', function() {
       var eventID = parseInt(this.id.replace('btnDeleteEvent', ''));
       $.ajax({
          url: '/api/delete',
          method: 'POST',
          dataType: 'json',
          data: JSON.stringify({'action': 'delete_one', 'id': eventID}),
          success: function(data) {
              if(data['success'])
                  document.location.reload();
              else
                  alert('Error: ' + data['error']);
          }
        });
    });
});
