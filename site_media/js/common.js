
// 投票按钮
$(".JS-vote").click(function() {
    var that = $(this);
    var option_id = $(that).attr('id');
    if (option_id) {
        $.post('/post_vote/', {'option_id':option_id}, function(data){
            $(that).attr('disabled', 'disabled');
            $(that).text('已投票');

            if (data.response === "ok") {
                layer.alert('投票成功！', {
                    skin: 'layui-layer-lan',
                    closeBtn: 0,
                    shift: 1 //动画类型,
                })
                $(that).prev().prev().text(data.data+"票");
            }else{
                layer.alert(data.error, {
                    skin: 'layui-layer-lan',
                    closeBtn: 0,
                    shift: 6 //动画类型
                    })
            }
        }, "json")
    }
});

// 删除选项按钮
$(".JS-del-vote").click(function() {
    var that = $(this);
    var option_id = $(that).attr('id');
    if (option_id) {
        $.post('/post_vote_del/', {'option_id':option_id}, function(data){
            $(that).attr('disabled', 'disabled');

            if (data.response === "ok") {
                layer.alert('删除成功！', {
                    skin: 'layui-layer-lan',
                    closeBtn: 0,
                    shift: 1 //动画类型,
                }, function(){
                    location.reload();
                })

            }else{
                layer.alert(data.error, {
                    skin: 'layui-layer-lan',
                    closeBtn: 0,
                    shift: 6 //动画类型
                    })
            }
        }, "json")
    }
});
