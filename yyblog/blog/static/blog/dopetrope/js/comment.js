/**
 * @author Chine
 * using jquery form to submit comment with ajax
 */
var locked = false;

$(function(){
  $("#commentform").ajaxForm({
	beforeSubmit: checkComment,
	success: dealResponse,
    dataType: 'json'
  });

  $("input#not-robot").click(function() {
	$("#commentform").append("<input id=\"not-robot-input\" type=\"hidden\" name=\"not_robot\" value=\"1\" />");
	$(this).hide();
  });

  $('div.reply').live('click', function() {
	var name = $.trim($(this).siblings('header').children('cite').text());
	var id = $.trim($(this).parents('li:first').attr('id'));
	var commentId = id.split('-')[1];

	$('form#commentform input[type=button]:last')
	  .val('取消对' + name + '回应').show();
	$('html, body').scrollTop($('#commentform').offset().top);
	$('#id_comment_replied').val(commentId);
  });
  $('form#commentform input[type=button]:last').click(function() {
	var $hideId = $('#id_comment_replied');
	var commentId = $hideId.val();
	$hideId.val('');
	$(this).hide();
	$('html, body').scrollTop($('#comment-'+commentId).offset().top);
  });

  if (get_article_id !== undefined){
    $('form#commentform  #id_article_replied').val(get_article_id());
  }

});

// using jquery blockUI to show information
function block(msg) {
  $.blockUI({
	message: msg,
    css: {
      width: '350px',
      border: 'none',
      padding: '15px 5px',
      backgroundColor: '#000',
      '-webkit-border-radius': '3px',
      '-moz-border-radius': '3px',
	  'border-radius': '3px',
      opacity: .6,
      color: '#fff' ,
	  'font-weight': 'bold'
    }
  });
}

function checkComment(arr, $form, options) {
  if(locked)
	return false;

  // check if you have clicked the not-robot button
  if (!($('form#commentform input#not-robot-input').val())){
    block("评论失败，请点击我不是机器人按钮后在评论!");
    setTimeout($.unblockUI, 1500);
    return false;
  }
  for(itm in arr) {
	var obj = arr[itm];

	var name = obj.name;
	var value = obj.value;

	if(name == 'username'|| name=='user_email' || name=="content") {
	  if(value == '' || typeof value == undefined) {
		block("评论失败，请填写所有必填信息！");
		setTimeout($.unblockUI, 1500);
		return false;
	  }
	}
  }

  if(!locked)
	locked = true;
}

function dealResponse(jsonData, statusText){
  if (jsonData.success) {
	block(jsonData.msg);

    $("section#comments").replaceWith(jsonData.html);
	// reset the comment form
	$('textarea#message').val('');

	// set reply comment id to empty and hide cancel replay button
	$('#id_comment_replied').val('');
	$('form#commentform input[type=button]:last').hide();

    // show 'I am not robot button and delete the hidden robot input'
    $("input#not-robot").show();
    $('form#commentform input#not-robot-input').remove();

	//scroll to the new comment,if the element exists
    if ($('#comment-'+jsonData.id).length > 0){
	  $('html, body').scrollTop($('#comment-'+jsonData.id).offset().top);
    }
    setTimeout($.unblockUI, 1500);
	// $.unblockUI();

  }else{
    block(jsonData.msg);
    setTimeout($.unblockUI, 1500);
  }

  if(locked) locked = false;
}
