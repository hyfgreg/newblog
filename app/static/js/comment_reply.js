//Rest the value when reply-dialog-box dismiss
function undo_reply() {
    $('#replied_id').val(-1);
};

function go_to_reply(id, visitor_name) {
    $('html, body').animate({scrollTop: $('#submit-comment').offset().top}, 500);
    $('#replied_id').val(id);
    $('#reply-dialog-box').remove();
    $('#submit-comment-container').prepend('<div class="alert alert-info alert-dismissable" id="reply-dialog-box">' +
        '<button type="button" class="close" data-dismiss="alert" onclick="undo_reply()">&times;</button>' +
        '回复给<strong><i>' + visitor_name + '</i></strong> </div>');
};

//Reset the replied_id value when refresh page
window.onload = function () {
    $('#replied_id').val(-1);
};

function go_to_page(id, page) {

    $.ajax({
        url: '/comments_ajax',
        type: 'POST',
        async: true,
        data: {
            id: id, page: page
        },
        dataType: 'json',
        beforeSend: function (xhr) {
            // console.log(xhr)
            // console.log('发送前')
        },
        success: show_comments,
        error: function (xhr) {
            console.log('错误')
        },
        complete: function () {
        }
    });

}

function show_comments(resp) {
    // console.log(resp);
    var data = resp.data;
    var c_div = $('.comments-div');
    c_div.html('');
    // var new_c = '';
    // new_c += '<hr><ul id="comments" class="comments">';
    // for (var i = 0; i < data.length; i++) {
    //     sc_html = '<li class="comment"><div class="clearfix">';
    //     if (data[i]['reply_to'] == 'notReply') {
    //         sc_html += '<h4 class="pull-left"><b>' + data[i]['visitor_name'] + '</b></h4></div>';
    //     } else {
    //         sc_html += '<h4 class="pull-left"><b>' + data[i]['visitor_name'] + '</b> 回复 <b>' + data[i]['reply_to'] + '</b></h4></div>';
    //     }
    //     sc_html += '<p><em></em></p><p><em>' + data[i]['content'] + '</em></p><p></p>';
    //     sc_html += '<div class="clearfix"><span class="label label-success glyphicon glyphicon-time">'
    //     sc_html += '<span>' + timeformat(data[i]['timestamp']) + '</span></span></div>';
    //     sc_html += '<div class="pull-right"><button class="btn btn-info btn-xs" onclick="go_to_reply()"';
    //     sc_html += '</li><hr>';
    //     new_c += sc_html;
    // }
    // new_c += '</ul>';
    var new_ul = document.createElement('ul');
    new_ul.setAttribute('class', 'comments');
    new_ul.setAttribute('id', 'comments');
    for (var i = 0; i < data.length; i++) {
        var new_li = document.createElement('li');
        new_li.setAttribute('class', 'comment');
        var name_div = document.createElement('div');
        name_div.setAttribute('class', 'clearfix');
        var name_h4 = document.createElement('h4');
        name_h4.setAttribute('class', 'pull-left');
        var name_b = document.createElement('b');
        name_b.innerHTML = data[i]['visitor_name'];
        name_h4.appendChild(name_b);
        name_div.appendChild(name_h4);
        new_li.appendChild(name_div);

        $(new_li).append('<p><em></em></p>');
        $(new_li).append('<p><em>' + data[i]['content'] + '</em></p><p></p>');

        var new_bottom = document.createElement('div');
        $(new_bottom).addClass('clearfix');
        var new_date = document.createElement('div');
        $(new_date).addClass('pull-left');
        var span_out = document.createElement('span');
        $(span_out).addClass('label label-success glyphicon glyphicon-time');
        var span_in = document.createElement('span');
        $(span_in).append(timeformat(data[i]['timestamp']));
        $(span_out).append(span_in);

        var new_btn_div = document.createElement('div');
        $(new_btn_div).addClass('pull-right');
        var new_btn = document.createElement('button');
        $(new_btn).addClass('btn btn-info btn-xs');
        $(new_btn).attr('onclick', 'go_to_reply(' + data[i]['id'] + ',' + '"' + data[i]['visitor_name'] + '"' + ')');
        $(new_btn).append('<span class="glyphicon glyphicon-comment"></span>');
        $(new_btn).html('<span class="glyphicon glyphicon-comment"></span>' + ' 回复');

        $(new_btn_div).append(new_btn);

        $(new_bottom).append(span_out);
        $(new_bottom).append(new_btn_div);
        $(new_li).append(new_bottom);


        $(new_li).append('<hr>')
        new_ul.appendChild(new_li)
    }
    c_div.append('<hr>');
    c_div.append(new_ul);

}

function timeformat(time) {
    var data = new Date(time);
    var year = data.getFullYear();  //获取年
    var month = data.getMonth() + 1;    //获取月
    var day = data.getDate(); //获取日
    // var hours = data.getHours();
    // var minutes = data.getMinutes();
    time = year + "年" + month + "月" + day + "日";
    return time;
}

$(function () {
    $("a").click(function () {
        var li_ac = $('.pagination').find('.active');
        $(li_ac).removeClass('active');
        $(this).parent().addClass('active')
    });
});

// function page_activate() {
//
//     $('a').on('click', function () {
//         $(this).parent().addClass('active')
//     });
//     // console.log(page)
//     // $(page).parent().addClass('active');
// }
