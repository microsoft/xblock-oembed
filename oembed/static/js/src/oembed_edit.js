/* Copyright (c) Microsoft Corporation. All Rights Reserved.
   Licensed under the MIT license. See LICENSE file on the project webpage for details. */
/* Javascript for OEmbedXBlock. */
function OEmbedXBlock(runtime, element) {

  var clear_name_button = $('.clear-display-name', element);
  var display_name = $(element).find('#edit_display_name');
  var document_url = $(element).find('#edit_document_url');
  var save_button = $('.save-button', element);
  var validation_alert = $('.validation_alert', element);
  var defaultName = display_name.attr('data-default-value');
  var error_message_div = $('.xblock-editor-error-message', element);
  var xblock_inputs_wrapper = $('.xblock-inputs', element);

  ToggleClearDefaultName();
  IsUrlValid();

  $('.clear-display-name', element).bind('click', function() {
        $(this).addClass('inactive');
        display_name.val(defaultName);
  });

  function SaveEditing(){
    var display_name_val = display_name.val().trim();
    var document_url_val = document_url.val().trim();

    
    var data = {
      display_name: display_name_val,
      document_url: document_url_val
    };

    error_message_div.html();
    error_message_div.css('display', 'none');
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      if (response.result === 'success') {
                window.location.reload(false);
      } else {
                error_message_div.html('Error: '+response.message);
                error_message_div.css('display', 'block');
      }
    });
  }

  function ToggleClearDefaultName(name, button){
        if (display_name.val() == defaultName){
            if (!clear_name_button.hasClass('inactive')){
                clear_name_button.addClass('inactive');
            }
        }
        else {
            clear_name_button.removeClass('inactive');
        }
  }

  display_name.bind('keyup', function(){
    ToggleClearDefaultName();
  });

  document_url.bind('keyup', function(){
    IsUrlValid();
  });


  $('.cancel-button', element).bind('click', function() {
    runtime.notify('cancel', {});
  });
  
  function IsUrlValid(url) {
    var onedrive_url = document_url.val();

    if(/<iframe /i.test(onedrive_url)){
        validation_alert.addClass('covered');
        save_button.removeClass('disabled');
        document_url.removeClass('error');
        xblock_inputs_wrapper.removeClass('alerted');
        save_button.bind('click', SaveEditing);
        return true;
    }

    document_url.css({'cursor':'wait'});
    save_button.addClass('disabled').unbind('click');

    $.ajax({
        type: "POST",
        url: runtime.handlerUrl(element, 'check_url'),
        data: JSON.stringify({url: onedrive_url}),
        success: function(result) {
            if (result.status_code >= 400){
                validation_alert.removeClass('covered');
                document_url.addClass('error');
                xblock_inputs_wrapper.addClass('alerted');
            } else {
                validation_alert.addClass('covered');
                save_button.removeClass('disabled');
                document_url.removeClass('error');
                xblock_inputs_wrapper.removeClass('alerted');

                save_button.bind('click', SaveEditing);
            }
        },
        error: function(result) {
            validation_alert.removeClass('covered');
            save_button.addClass('disabled').unbind('click');
            document_url.addClass('error');
            xblock_inputs_wrapper.addClass('alerted');
        },

        complete: function() {
            document_url.css({'cursor':'auto'});
        }
    });
  }
  
  function isValidEmbedCode(code) {
    return /<iframe /i.test(code);
  }
  

  $(function ($) {
    /* Here's where you'd do things on page load. */
  });
}
