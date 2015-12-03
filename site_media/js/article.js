function upload_img(id){
    option_id = id;
    layer.open({
        type: 1,
        title: '上传图片',
        area: ['420px', '240px'], //宽高
        btn: ['确定','取消'], //按钮
        content: "<form class='fileForm' method='post' action='https://sm.ms/api/upload'><table class='fileTable'><tr><td>上传图片：</td><td><input id='smfile' name='smfile' type='file' multiple='true'></td></tr><tr><td></td><td id='img_show'><button type='button' onclick='ImageUpload()' class='button_small'>上传</button></td></tr></table></form>",
    });
}
function ImageUpload(){
    $(".fileForm").ajaxSubmit(function(d){
        if (d.code == 'error') {
            layer.msg('上传失败');
        }else if(d.code == 'success'){
            var data = d.data;
            var url = data.url;
            option_dic.url = url;
            var str = '<img height="200px" src="'+ url +' "></img>';
            $("#upload_"+option_id).html(str);
            layer.msg('上传成功！', {icon: 1,time: 1500})

            // $.post('/profile/change_header_img/', {'url': url}, function(data){
            //         if(data=="ok"){ 
            //             // layer.msg('上传成功！', function(){
            //             //     location.reload();
            //             // });
            //             layer.msg('上传成功！', {
            //                     icon: 1,
            //                     time: 1500
            //                 }, function(){
            //                     location.reload();
            //                 }); 
            //         }else{
            //             layer.msg(data);
            //         }
            //     });
        }
    })
}
$("#add_option").click(function(){
    var len = $('.vote-list').length;
    var tmpl ='<div class="vote-list">\
            <table>\
                <tbody>\
                <tr align="center">\
                    <td class="img-table" id=upload_'+len+'><button onclick="upload_img('+len+')" class="header_icon button_small">上传图片</button></td>\
                    <td><textarea class="msl option" id=utext_'+len+' rows="5" maxlength="120" id="option" name="option_d1" placeholder="请输入要投票的选项"></textarea></td>\
                    <td>\
                    <button type="button" onclick=OptionPost("'+len+'") class="button_small">确认添加选项</button></td>\
                    <td></td>\
                </tr>\
                </tbody>\
            </table>\
        </div>'
    $('.art-content').append(tmpl);
})

function OptionPost(id, post_id){
    var url = $("#upload_"+id+" img").attr("src");
    var content = $("#utext_"+id).val();

    if ((url !=="" && typeof url !=="undefined")|| content !== "") {
        if (typeof url ==="undefined") {
            url = ""
        }
        var post_id = $('.art-title').attr('id')
        var data = {'url':url, 'content':content, 'post_id':post_id};

        $.post('/add_option/', {'data':JSON.stringify(data)}, function(d) {
            alert(d);
        }, 'json');
    }else{
        layer.msg('请填写要添加选项的图片或内容！', {time: 2500});
        return
    }
}