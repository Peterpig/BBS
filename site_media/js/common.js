
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
        layer.confirm('确定要删除该选项？', {
            btn: ['确定','取消'] //按钮
        }, function(){
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
        }, function(){
            return;
        });
    }

});

// 删除选项按钮
$(".JS-del-posts").click(function() {
    var that = $(this);
    var option_id = $(that).attr('data-id');
    if (option_id) {
        layer.confirm('确定要删除该文章吗？', {
            btn: ['确定','取消'] //按钮
        }, function(){
            $.post('/post_posts_del/', {'option_id':option_id}, function(data){
                // $(that).attr('disabled', 'disabled');
                if (data.response === "ok") {
                    layer.alert('删除成功！', {
                        skin: 'layui-layer-lan',
                        closeBtn: 0,
                        shift: 1 //动画类型,
                    }, function(){
                        location.href = '/';
                    })

                }else{
                    layer.alert(data.error, {
                        skin: 'layui-layer-lan',
                        closeBtn: 0,
                        shift: 6 //动画类型
                        })
                }
            }, "json")
        }, function(){
            return;
        });
    }
});
