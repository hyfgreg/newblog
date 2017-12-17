
//Rest the value when reply-dialog-box dismiss
function undo_reply() {
    $('#replied_id').val(-1);
}

function go_to_reply(id, visitor_name) {
    $('html, body').animate({scrollTop:  $('#submit-comment').offset().top}, 500);
    $('#replied_id').val(id);
    $('#reply-dialog-box').remove();
    $('#submit-comment-container').prepend('<div class="alert alert-info alert-dismissable" id="reply-dialog-box">' +
            '<button type="button" class="close" data-dismiss="alert" onclick="undo_reply()">&times;</button>' +
            '回复给<strong><i>' + visitor_name +'</i></strong> </div>');
}

//Reset the replied_id value when refresh page
window.onload = function(){
    $('#replied_id').val(-1);
}