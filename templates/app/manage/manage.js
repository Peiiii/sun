
function getScreenSize(){
    var width=screen.width;
    var body=$('body');
    body.removeClass('screen-xs screen-md');
    if(width<500)body.addClass('screen-xs');
    else body.addClass('screen-md');
}
function initManage(){
    getScreenSize();
    $(window).on('resize',()=>{getScreenSize();})
}
$(document).ready(()=>{
    initManage();
})