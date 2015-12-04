function submit_content() {
    var title = $("#title").val();
    var content = $("#content").val();
    var type = $("input[type=radio]:checked").val();
    var tag = $("#select").find("option:selected").val();
    var option = new Array();

    if (title === "") {
        layer.tips("文章标题不能为空！", "#title", {tips: [1, '#3595CC'],time: 2500});
        return
    }
    if (type === "2") {
        var option_first = $("textarea[name=option_d1]").val();
        if (option_first === "") {
            layer.tips("请至少填写一个选项！", "#option", {tips: [1, '#3595CC'],time: 2500});
            return
        }
        $(".btnAndInput .option").each(function() {
            if ($(this).val() !== "") {
                var id = $(this).attr('id');

                var dic = {};
                dic.val = $(this).val();
                dic.img = $("#"+id+"_img").val();
                option.push(dic);
            };
        })
    }
    if (tag === "0") {
        layer.tips("请选择一个分类！", "#select", {tips: [1, '#3595CC'],time: 2500});
        return
    }
    var post_dic = {"title": title, "content": content, "option":option, "tag":tag, "type":type};
    var data_dict = {"data_dict":JSON.stringify(post_dic)}
    $.post('/new/', data_dict, function(d) {
        if (d.response == 'ok') {
            layer.alert('发表成功！', {
                skin: 'layui-layer-molv' //样式类名
                ,closeBtn: 0
            }, function(){
                location.href = '/t/'+d.data;
            });

        }else if(d.response == 'fail'){
            layer.alert(d.error, {icon: 5, shift: 6, time: 2000});
        }
    }, 'json');
}

function add_option() {
    var len = $(".option").length;
    var html = '<div class="btnAndInput"><textarea class="msl option" rows="5" maxlength="120" id="option'+ len + '" name="option' + len + '" placeholder="请输入要投票的选项"></textarea><button type="button" class="button_small" data-id="option'+ len + '">添加图片</button><input type="text" id="option'+len+'_img" name="option'+len+'_img" value="" hidden>';
    if (len === 3) {
        $("#option2").parent().after(html);
    }else{
        len = len - 1;
        $("#option"+len).parent().after(html);
    }

}

function ImageUpload(text_id){
    $("[data-id='"+text_id+"']").attr('disabled','disabled');
    $(".fileForm").ajaxSubmit(function(d){
        if (d.code == 'error') {
            layer.msg('上传失败');
        }else if(d.code == 'success'){
            var data = d.data;
            var url = data.url;

            // 隐藏图片地址
            $("#"+text_id+"_img").attr('value',url);

            // 关闭弹框
            layer.closeAll();
            $("[data-id='"+text_id+"']").removeAttr('disabled')

            // 转换图片ID
            var num = text_id_to_num(text_id);
            pic_list.push({'alt':'', 'pid':parseInt(num), 'src':url, 'thumb':url});

            // 删除原来的button，并且重新追加一个button 用来显示图册
            var strp = "ViewPic('"+ num +"')";
            $("[data-id='"+text_id+"']").remove()
            var html_str = "<button class='btn' onclick="+strp+">图片已上传,点击查看</button>";
            $("#"+text_id).after(html_str);

            layer.msg('上传成功！',{
                icon:1
            });
        }
    })
}
function ViewPic(num){
    json_dic = {
                "title": "图片预览", //相册标题
                "id": 1, //相册id
                "start": parseInt(num), //初始显示的图片序号，默认0
                "data": pic_list
            }
    layer.photos({
        photos: json_dic,
    });
}

$(function(){
    $(".btnAndInput .button_small").click(function(){
        var text_id = $(this).attr('data-id');
        var that = $(this);
        layer.open({
            type: 1,
            title: '上传图片',
            skin: 'layui-layer-rim', //加上边框
            area: ['420px', '240px'], //宽高
            shade: 0.6,
            moveType: 1,
            content: "<form class='fileForm' method='post' action='https://sm.ms/api/upload'><table class='fileTable'><tr><td>上传图片：</td><td><input id='smfile' name='smfile' type='file' multiple='true'></td></tr><tr><td></td><td id='img_show'><button type='button' onclick=ImageUpload('"+text_id+"') class='button_small'>上传</button></td></tr></table></form>",
        });
    })
})

function text_id_to_num(text_id){
    var num = text_id.slice(-1);
    if (num === "n" ) {
        //启示值为0
        num = 0
    }
    return num
}