
function debug_handler() {
    var data = {
        "name": $(""),
        "commands": parser()
    }
    var url = HOST + '/automation/api/v1/debug'
    http(url, data, 'POST', function (data) {
        console.log("成功！")
    }, function (data) {
        console.log("出错！")
    })
}

$(function () {
    $("#catalog").accordion();
    $("#catalog li").draggable({
        appendTo: "body",
        helper: "clone"
    });
    $("#cart ol").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function (event, ui) {
            $(this).find(".placeholder").remove();
            var classify = ui.draggable.attr("classify");
            var command = ui.draggable.attr("command");
            var html = commands[classify][command]();
            $("<li></li>").html(html).appendTo(this);
        }
    }).sortable({
        items: "li:not(.placeholder)",
        sort: function () {
            // 获取由 droppable 与 sortable 交互而加入的条目
            // 使用 connectWithSortable 可以解决这个问题，但不允许您自定义 active/hoverClass 选项
            $(this).removeClass("ui-state-default");
        }
    });
    $('#debug').click(debug_handler)
});