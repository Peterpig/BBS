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
        var option_first = $("input[name=option]").val();
        if (option_first === "") {
            layer.tips("请至少填写一个选项！", "#option", {tips: [1, '#3595CC'],time: 2500});
            return
        }
        $(".option").each(function() {
            option.push($(this).val());
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
    var html = '<input class="msl option" rows="1" maxlength="120" id="option'+ len + '" name="option' + len + '" placeholder="请输入要投票的选项"></input>';
    if (len === 3) {
        $("#option").after(html);
    }else{
        len = len - 1;
        $("#option"+len).after(html);
    }

}
