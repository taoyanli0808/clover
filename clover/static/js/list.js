
function fail(data) {
    console.log(data);
    alert(data);
}

function detail(value, row, index) {
	return ['<a href=' + value + '"/clover/interface/api/v1/trigger?cases=">触发用例</a>'].join("")
}

function success(data) {
    console.log(data);
    var cases = data['data'];
    // $('#cases').bootstrapTable({
    //     search:true,
    //     pageSize:"50",
    //     ageNumber:"1",
    //     sidePagination:"client",
    //     pagination:true,
    //     striped: true,                      //是否显示行间隔色
    //     showColumns: true,                  //是否显示所有的列
    //     data: cases,
    //     columns: [{
    //         field: '_id',
    //         title: '用例编号'
    //     }, {
    //         field: 'method',
    //         title: '请求方法'
    //     }, {
    //         field: 'host',
    //         title: '请求地址'
    //     }, {
    //         field: '_id',
    //         title: '查看详情',
    //         formatter: detail //添加超链接的方法
    //     }]
    // });
}

$(function () {
    var url = '/interface/api/v1/list';
    var data = {};
    var method = 'GET';
    http(url, data, method, success, fail)
})