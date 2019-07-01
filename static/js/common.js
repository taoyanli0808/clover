
var HOST = 'http://127.0.0.1:9999';

function http(url, data, method, success, fail)
{
    var data = method == 'GET' ? data : JSON.stringify(data)
    $.ajax({
        type: method,
        contentType: "application/json; charset=utf-8",
        data: data,
        url: url,
        dataType: 'json',
        success: success,
        fail: fail
    });
}