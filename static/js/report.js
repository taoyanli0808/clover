
function drawPie(id, data) {
    var myChart = echarts.init(document.getElementById(id));
    var option = {
        backgroundColor: '#F5F5F5', //背景色
        title: {
            text: '测试统计数据',
            x: 'center'
        },

        legend: {
            orient: 'vertical',
            x: 'left',
            data: ['成功', '失败', '未检验']
        },


        color:['#3c763d','#a94442','#0099CC'],

        calculable: true,

        series: [{
            name: '测试结果',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            startAngle: 135,
            data: [
                {
                    value: data[0],
                    name: '成功',
                    itemStyle: {
                        normal: {
                            label: {
                                formatter: '{b} : {c} ({d}%)',
                                textStyle: {
                                    align: 'left',
                                    fontSize: 15,
                                }
                            },
                            labelLine: {
                                length: 40,
                            }
                        }
                    }
                },
                {
                    value: data[1],
                    name: '失败',
                    itemStyle: {
                        normal: {
                            label: {
                                formatter: '{b} : {c} ({d}%)',
                                textStyle: {
                                    align: 'right',
                                    fontSize: 15,
                                }
                            },
                            labelLine: {
                                length: 40,
                            }
                        }
                    }
                },
                {
                    value: data[2],
                    name: '未检验',
                    itemStyle: {
                    normal: {
                        label: {
                            formatter: '{b} : {c} ({d}%)',
                            textStyle: {
                                align: 'right',
                                fontSize: 15,
                            }
                        },
                        labelLine: {
                            length: 40,
                        }
                    }
                }
            }],
        }]
    };
    // 为echarts对象加载数据
    myChart.setOption(option);
}

function generate_table_detail(data, id) {
    // 拼接table数据
    var html = "";
    for (var i=0; i<data.length; i++) {
        var slice = '<tr class="all">' +
            '<td class="text-center">' + data[i]['_id'] + '</td>' +
            '<td class="text-center">' + data[i]['host'] + '</td>' +
            '<td class="text-center">' + data[i]['method'] + '</td>' +
            '<td class="text-center">' + data[i]['status'] + '</td>' +
            '<td class="text-center">' + data[i]['message'] + '</td>' +
            '</tr>'
        html = html + slice;
    }
    $('#' + id).append(html);
}

function success(data) {
    console.log(data)

    var data = data['data'];

    $('#start').text(data[0]['time']['start']);
    $('#end').text(data[0]['time']['end']);
    $('#spend').text(data[0]['time']['cost']);
    $('#total').text(data[0]['count']['total']);
    $('#run').text(data[0]['count']['run']);
    $('#skip').text(data[0]['count']['skip']);

    drawPie('pie', [data[0]['count']['success'], data[0]['count']['fail'], data[0]['count']['skip']]);

    $('#t-total').html(data[0]['count']['total']);
    $('#t-success').html(data[0]['count']['success']);
    $('#t-fail').html(data[0]['count']['fail']);
    $('#t-skip').html(data[0]['count']['skip']);

    // 筛选成功与失败的数据，还有跳过的数据
    total = data[0]['result'];
    success = [];
    fail = [];
    skip = [];

    console.log(total)
    for (var i=0; i<total.length; i++) {
        console.log(total[i]['message']);
        if (total[i]['message'] == '测试通过！') {
            success.push(total[i])
        } else {
            fail.push(total[i])
        }
    }

    generate_table_detail(total, 'panel-data-0');
    generate_table_detail(success, 'panel-data-1');
    generate_table_detail(fail, 'panel-data-2');
    generate_table_detail(skip, 'panel-data-3');
}

function fail(data) {
    console.log(data)
}

$(function() {
    // 请求后端返回测试报告
    // 测试报告通过url的最后一个字段（run_id）去取
    var url = host + '/interface/api/v1/report';
    var uri = window.location.href;
    var slice = uri.split("/");
    var data = {
        'run_id': slice[slice.length-1]
    };
    http(url, data, 'GET', success, fail);
});