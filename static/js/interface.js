
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
      '<div class="layui-input-inline layui-col-md2">' +
        '<select class="a_extractor" lay-filter="team" lay-verify="required">' +
          '<option value="re">正则</option>' +
          '<option value="delimiter">分隔符</option>' +
        '</select>' +
      '</div>' +
     '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输入断言" autocomplete="off" class="a_expression layui-input">' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md3">' +
        '<select class="a_condition" lay-filter="team" lay-verify="required">' +
          '<option value="equal">等于</option>' +
          '<option value="not_equal">不等于</option>' +
          '<option value="contain">包含</option>' +
          '<option value="not_contain">不包含</option>' +
          '<option value="greater">大于</option>' +
          '<option value="not_less">大于等于</option>' +
          '<option value="less">小于</option>' +
          '<option value="not_greater">小于等于</option>' +
        '</select>' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" name="title" required  lay-verify="required" placeholder="请输断言值" autocomplete="off" class="a_expected layui-input">' +
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
      '<div class="layui-input-inline layui-col-md2">' +
        '<select class="e_extractor" lay-filter="team" lay-verify="required">' +
          '<option value="re">正则</option>' +
          '<option value="delimiter">分隔符</option>' +
        '</select>' +
      '</div>' +
     '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" required  lay-verify="required" placeholder="请输入表达式" autocomplete="off" class="e_expression layui-input">' +
      '</div>' +
      '<div class="layui-input-inline layui-col-md3">' +
        '<input type="text" required  lay-verify="required" placeholder="请输入变量名" autocomplete="off" class="e_variable layui-input">' +
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
    layui.form.render()
}

function add_parameter() {

    // 需要发送给服务器的数据，是测试接口时，在页面上填写的内容。
    var data = {
        'environment': {
            'team': $('#team').val(),
            'project': $('#project').val(),
        },
        'request': {
            'method': $('#method').val(),
            'host': $('#host').val(),
            'path': $('#path').val(),
            'header': {},
            'param': {},
        },
        'assert': [],
        'extract': []
    }

    // 使用each函数遍历每一个header的key，按照each函数的索引
    // 分别取出header的key和value，保存在data['header']。
    $('.h_key').each(function(index, element){
        var key = $('.h_key').eq(index).val();
        var value = $('.h_value').eq(index).val();
        data['request']['header'][key] = value;
    })

    // 使用each函数遍历每一个parameter的key，按照each函数的索引
    // 分别取出parameter的key和value，保存在data['param']。
    $('.p_key').each(function(index, element){
        var key = $('.p_key').eq(index).val();
        var value = $('.p_value').eq(index).val();
        data['request']['param'][key] = value;
    })

    /*
    // 这里是断言数据，断言需要先提取响应信息，再将响应与预期值比较；
    // 因此这里需要使用正则或者分隔符提取器，需要输入提取表达式；
    // 比较条件只支持先定的几种，如需支持更多条件需扩展common.interface.expect模块。
     */
    $('.a_extractor').each(function(index, element){
        data['assert'].push({
            'extractor': $('.a_extractor').eq(index).val(),
            'expression': $('.a_expression').eq(index).val(),
            'condition': $('.a_condition').eq(index).val(),
            'expected': $('.a_expected').eq(index).val()
        })
    })

    $('.e_extractor').each(function(index, element){
        var key = $('.e_key').eq(index).val();
        var value = $('.e_value').eq(index).val();
        data['extract'].push({
            'extractor': $('.e_extractor').eq(index).val(),
            'expression': $('.e_expression').eq(index).val(),
            'variable': $('.e_variable').eq(index).val()
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
    var content = data['data']['response']['content']
    $('#response').append('<pre><code>' + JSON.stringify(content, null, 4) + '</code></pre>')
    alert(data['message'])
}

function fail(data) {
    console.log(data);
    // 先清空数据，否则append函数会不断累加结果。
    $('#response').empty()
    // 讲返回的结果append到response区域，代码和json数据显示需要用pre与code标签，json.stringify使用参数null, 4缩进4个空格。
    $('#response').append('<pre><code>' + JSON.stringify(data['data'], null, 4) + '</code></pre>')
    alert(data['message'])
}

function send_request() {
    // 这里要注意请求需要加蓝图的url_prefix即/interface
    var url = '/interface/api/v1/debug';
    var data = add_parameter();
    http(url, data, 'POST', debug_success, fail);
}

function save_success(data) {
    console.log(data);
    alert("保存用例成功，case_id: " + data['data'])
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