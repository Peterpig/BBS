function submit_content() {
    var title = $("#title").val();
    var content = $("#content").val();
    var tag = $("#select").find("option:selected").val();
    if (title === "") {
        layer.tips("文章标题不能为空！", "#title", {tips: [1, '#3595CC'],time: 2500});
        return
    }
    if (tag === "0") {
        layer.tips("请选择一个分类！", "#select", {tips: [1, '#3595CC'],time: 2500});
        return
    }
    $.post('/new/', {"title": title, "content": content}, function(d) {
        d = eval('('+d+')');
        if (d.response == 'ok') {
            location.href = '/t/'+d.data
        }else if(d.response == 'fail'){
            layer.alert(d.error, {icon: 5, shift: 6, time: 2000});
        }
    });
}