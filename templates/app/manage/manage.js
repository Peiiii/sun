

function initManage(){

function initMenu(){
    var menu=$('#app-menu');
    var app_box=$('#app-box');
    var items=menu.find('.menu-item');
    items.map((n,it)=>{
        var it=$(it);
        it.click(()=>{
            var url=it.attr('url');
            var re=$.get({url:url,async:false});
            var html=re.responseText;
            log(re);
            app_box.html(html);
        })
    })
}






initMenu();
}
$(document).ready(()=>{
//    initManage();
})