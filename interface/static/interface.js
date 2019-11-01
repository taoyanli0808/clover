
function add_header() {
    // 这里是动态拼接html语句，带着样式，拼凑成页面的  "key []  value []"
    var html = '<div class="layui-row">' +
      '<div class="layui-input-inline  layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="h_key layui-input">' +
      '</div>' +
      '<div class="layui-input-inline  layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="h_value layui-input">' +
      '</div>' +
      '<div class="layui-input-inline  layui-col-md1">' +
        '<button class="layui-btn layui-btn-danger delete">' +
          '<i class="layui-icon layui-icon-delete" style="font-size: 30px; color: #1E9FFF;"></i>' +
        '</button>' +
      '</div>' +
    '</div>'
    $('#h_section').append(html);
    $('#h_section').show();
    $('#c_section').show();
    $('.delete').click(delete_element);
}

function add_param() {
    // 这里是动态拼接html语句，带着样式，拼凑成页面的  "key []  value []"
    var html = '<div class="layui-row">' +
      '<div class="layui-input-inline layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="p_key layui-input">' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="p_value layui-input">' +
      '</div>' +
      '<div class="layui-input-inline  layui-col-md1">' +
        '<button class="layui-btn layui-btn-danger delete">' +
          '<i class="layui-icon layui-icon-delete" style="font-size: 30px; color: #1E9FFF;"></i>' +
        '</button>' +
      '</div>' +
    '</div>'
    $('#p_section').append(html);
    $('#p_section').show();
    $('#c_section').show();
    $('.delete').click(delete_element);
}

function add_assert() {
    // 这里是动态拼接html语句，带着样式，拼凑成页面的  "jsonpath []  expect []"
    var html = '<div class="layui-row">' +
     '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入断言" autocomplete="off" class="a_key layui-input">' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md3">' +
        '<select id="a_op" lay-filter="team" lay-verify="required">' +
          '<option value="in">包含</option>' +
          '<option value="not in">不包含</option>' +
          '<option value="=">等于</option>' +
          '<option value="!=">不等于</option>' +
          '<option value=">">大于</option>' +
          '<option value=">=">大于等于</option>' +
          '<option value="<">小于</option>' +
          '<option value="<=">小于等于</option>' +
        '</select>' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输断言值" autocomplete="off" class="a_value layui-input">' +
      '</div>' +
      '<div class="layui-input-inline  layui-col-md1">' +
        '<button class="layui-btn layui-btn-danger delete">' +
          '<i class="layui-icon layui-icon-delete" style="font-size: 30px; color: #1E9FFF;"></i>' +
        '</button>' +
      '</div>' +
    '</div>'
    $('#a_section').append(html);
    $('#a_section').show();
    $('#c_section').show();
    $('.delete').click(delete_element);
    layui.form.render()
}

function add_extract() {
    // 这里是动态拼接html语句，带着样式，拼凑成页面的  "jsonpath []  expect []"
    var html = '<div class="layui-row">' +
      '<div class="layui-input-inline layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="e_key layui-input">' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md5">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入标题" autocomplete="off" class="e_value layui-input">' +
      '</div>' +
      '<div class="layui-input-inline  layui-col-md1">' +
        '<button class="layui-btn layui-btn-danger delete">' +
          '<i class="layui-icon layui-icon-delete" style="font-size: 30px; color: #1E9FFF;"></i>' +
        '</button>' +
      '</div>' +
    '</div>'
    $('#e_section').append(html);
    $('#e_section').show();
    $('#c_section').show();
    $('.delete').click(delete_element);
}

function add_parameter() {

    // 需要发送给服务器的数据，是测试接口时，在页面上填写的内容。
    var data = {
        'team': $('#team').val(),
        'project': $('#project').val(),
        'method': $('#method').val(),
        'host': $('#host').val(),
        'path': $('#path').val(),
        'header': {},
        'param': {},
        'assert': [],
        'extract': []
    }

    // 使用each函数遍历每一个header的key，按照each函数的索引
    // 分别取出header的key和value，保存在data['header']。
    $('.h_key').each(function(index, element){
        var key = $('.h_key').eq(index).val();
        var value = $('.h_value').eq(index).val();
        data['header'][key] = value;
    })

    // 使用each函数遍历每一个parameter的key，按照each函数的索引
    // 分别取出parameter的key和value，保存在data['param']。
    $('.p_key').each(function(index, element){
        var key = $('.p_key').eq(index).val();
        var value = $('.p_value').eq(index).val();
        data['param'][key] = value;
    })

    // jsonpath是断言的表达式，jsonpath结果与expect匹配
    // 如果符合预期则成功，否则判定为失败。
    // 使用each函数遍历每一个assert的jsonpath，按照each函数的索引
    // 分别取出assert的jsonpath作为key和expect作为value，保存在data['assert']。
    $('.a_key').each(function(index, element){
        var key = $('.a_key').eq(index).val();
        var value = $('.a_value').eq(index).val();
        var operation = $('.a_op').eq(index).val();
        data['assert'].push({
            'rule': key,
            'expect': value,
            'operation': operation
        })
    })

    $('.e_key').each(function(index, element){
        var key = $('.e_key').eq(index).val();
        var value = $('.e_value').eq(index).val();
        data['expect'].push({
            'expr': key,
            'variable': value
        })
    })

    return data;
}

function delete_element() {
    $(this).parent().parent().remove();
}

function debug_success(data) {
    console.log(data);
    // 先清空数据，否则append函数会不断累加结果。
    $('#response').empty()
    // 讲返回的结果append到response区域，代码和json数据显示需要用pre与code标签，json.stringify使用参数null, 4缩进4个空格。
    $('#response').append('<pre><code>' + JSON.stringify(data['data'], null, 4) + '</code></pre>')
    alert(data['message'])
}

function fail(data) {
    console.log(data);
}

function send_request() {
    // 这里要注意请求需要加蓝图的url_prefix即/interface
    var url = '/interface/api/v1/debug';
    var data = add_parameter();
    http(url, data, 'POST', debug_success, fail);
}

function save_success() {
    console.log(data);
    alert("保存用例成功，case_id" + data['data'])
}

function save_request() {
    // 这里要注意请求需要加蓝图的url_prefix即/interface
    var url = '/interface/api/v1/save';
    var data = add_parameter();
    http(url, data, 'POST', save_success, fail);
}

$(function() {
    $('#h_section').hide();
    $('#p_section').hide();
    $('#a_section').hide();
    $('#e_section').hide();
    $('#c_section').hide();

    $('#header').click(add_header);
    $('#param').click(add_param);
    $('#assert').click(add_assert);
    $('#extract').click(add_extract);
    $('#debug').click(send_request);
    $('#save').click(save_request);
});