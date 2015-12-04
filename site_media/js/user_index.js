        function ImageUpload(){
            $(".fileForm").ajaxSubmit(function(d){
                if (d.code == 'error') {
                    layer.msg('上传失败');
                }else if(d.code == 'success'){
                    var data = d.data;
                    var url = data.url;
                    var str = '<img height="200px" src="'+ url +' "></img>';
                    $(".header_icon img").attr('src', url);

                    $.post('/profile/change_header_img/', {'url': url}, function(data){
                            if(data=="ok"){ 
                                // layer.msg('上传成功！', function(){
                                //     location.reload();
                                // });
                                layer.msg('上传成功！', {
                                        icon: 1,
                                        time: 1500
                                    }, function(){
                                        location.reload();
                                    }); 
                            }else{
                                layer.msg(data);
                            }
                        });
                }
            })
        }
        $(".header_icon").click(function(){
            var text_id = $(this).attr('data-id');
            var that = $(this);
            layer.open({
                type: 1,
                title: '上传图片',
                area: ['420px', '240px'], //宽高
                shade: 0.6,
                moveType: 1,
                content: "<form class='fileForm' method='post' action='https://sm.ms/api/upload'><table class='fileTable'><tr><td>上传图片：</td><td><input id='smfile' name='smfile' type='file' multiple='true'></td></tr><tr><td></td><td id='img_show'><button type='button' onclick='ImageUpload()' class='button_small'>上传</button></td></tr></table></form>",
            });
        })

        $(".change_pw").click(function(){
            var old = $("#password_current").val();
            var new1 = $("#password_new").val();
            var new2 = $("#password_new2").val();
            if (old === "") {
                layer.tips("请填写原密码！", "#password_current", {tips: [1, '#3595CC'],time: 2000});
                return
            }

            if (new1 === "") {
                layer.tips("请填写新密码！", "#password_new", {tips: [1, '#3595CC'],time: 2000});
                return
            }

            if (old === new1) {
                layer.tips("新旧密码不能一致！", "#password_current", {tips: [1, '#3595CC'],time: 2000});
                return
            }
            if (new1.length < 6 ) {
                layer.tips("密码不能少于6位！", "#password_new", {tips: [1, '#3595CC'],time: 2000});
                return
            }
            if (new2 !== new1) {
                layer.tips("两次密码不一致！", "#password_new2", {tips: [1, '#3595CC'],time: 2000});
                return
            }

            var data = {'data':JSON.stringify({'old':old, 'new1':new1, 'new2':new2})}
            $.post('/profile/resetpass/', data, function(d){
                if (d == "ok") {
                    layer.alert('修改密码成功！', {
                                skin: 'layui-layer-lan',
                                closeBtn: 0,
                                shift: 1 //动画类型,
                            }, function(){
                                location.href="/login/"
                            })
                }else{
                    layer.alert(d, {
                                title: '错误',
                                skin: 'layui-layer-lan',
                                closeBtn: 0,
                                shift: 6 //动画类型
                    })
                }
            })
        })
