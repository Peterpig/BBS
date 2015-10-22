$(function(){
    var type = getQueryString('t');
    console.log(type);
    if (type === "2") {
        ChangePanel(2);
    }else{
        ChangePanel(1);
    }
    $("#id_password").keydown(function(e){ 
            var curKey = e.which; 
            if(curKey == 13){ 
                searchData(1)
                return false; 
            } 
    }); 
     $("#id_password2_r").keydown(function(e){ 
            var curKey = e.which; 
            if(curKey == 13){ 
                searchData(2)
                return false; 
            } 
    }); 

})

    function ChangePanel(type){
        if (type === 1) {
            $("#register-form").hide();
            $("#login-form").show();
            $("#register-panel").attr({"class":""});
            $("#login-panel").attr({"class":"active"});
            $("#login-form").attr({"class":"m-t animated fadeInDown"});
        }else{
            $("#login-form").hide();
            $("#login-panel").attr({"class":""});
            $("#register-panel").attr({"class":"active"});
            $("#register-form").show();
            $("#register-form").attr({"class":"m-t animated fadeInDown"});
        }
    }
    //提交查询
    function searchData(type){
        if (type === 1) {
            var username = $("#id_username").val();
            var password = $("#id_password").val();
            if (username == "") {
                layer.tips("请填写账号！", "#id_username", {tips: [1, '#3595CC'],time: 2000});
                return
            };
            if (password == "") {
                layer.tips("请填写密码！", "#id_password", {tips: [1,'#3595CC'], time: 2000});
                return
            };
            $.post('/login/', {"username": username, "password": password}, function(data) {
                if( data == "account_err" ){
                    layer.tips("账号或密码错误！", '#id_username', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "not_active"){
                    layer.tips("账号被禁用，请联系管理员！", '#id_username', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "err"){
                    layer.alert('登陆失败，请重试！', {
                                    skin: 'layui-layer-lan'
                                    ,closeBtn: 0
                                    ,shift: 6 //动画类型
                                });
                }else{
                    location.href = '/';
                }
            });
        }else if( type === 2){
            var username = $("#id_username_r").val();
            var email = $("#id_email_r").val();
            var password = $("#id_password_r").val();
            var password2 = $("#id_password2_r").val();
            if (username == "") {
                layer.tips("请填写账号！", "#id_username_r", {tips: [1, '#3595CC'],time: 2000});
                return
            };
            if (username.length < 6) {
                layer.tips("用户名必须大于6位！", "#id_username_r", {tips: [1, '#3595CC'],time: 2000});
                return
            };
            if (email == "") {
                layer.tips("请填写Email！", "#id_email_r", {tips: [1, '#3595CC'],time: 2000});
                return
            };
            if (password == "") {
                layer.tips("请填写密码！", "#id_password_r", {tips: [1,'#3595CC'], time: 2000});
                return
            };
            if (password.length < 6) {
                layer.tips("密码必须大于6位！", "#id_password_r", {tips: [1,'#3595CC'], time: 2000});
                return
            };
            if (password2 == "") {
                layer.tips("请填写密码！", "#id_password2_r", {tips: [1,'#3595CC'], time: 2000});
                return
            };
            if (password != password2) {
                layer.tips("两次密码不一致!", '#id_password2_r', {tips: [1, '#3595CC'],time: 2000});
                return
            }
            $('#register-form').ajaxSubmit(function(data){
                if( data == "empty" ){
                    layer.tips("请填写完整信息", '#id_password2_r', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "password_not_same"){
                    layer.tips("两次密码不一致!", '#id_password2_r', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "email"){
                    layer.tips("Email格式有问题!", '#id_email_r', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "exact"){
                    layer.tips("用户名已经存在！", '#id_email_r', {tips: [1, '#3595CC'],time: 2000});
                }else if(data == "err"){
                      layer.alert('注册失败，请重试！', {
                                    skin: 'layui-layer-lan'
                                    ,closeBtn: 0
                                    ,shift: 6 //动画类型
                                });
                }else if(data == 'ok'){
                    layer.alert('注册成功！', {
                                    skin: 'layui-layer-lan'
                                    ,closeBtn: 0
                                    ,shift: 1 //动画类型
                                },
                                function(){
                                    location.href = '/';
                                    });

                }
            });
        }
        
    }

    function sleep(d){
        for(var t = Date.now();Date.now() - t <= d;);
    }
    function getQueryString(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    }