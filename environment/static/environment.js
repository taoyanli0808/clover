
function init_team() {
  var url = "/environment/api/v1/aggregate"
  var data = {
    "type": "team",
    "key": "team"
  }
  http(url, data, 'post', function(data) {
    var html = ""
    for (key in data['data']) {
      html += '<option value="' + data['data'][key]['_id'] + '">' + data['data'][key]['_id'] + '</option>'
    }
    $('#team').append(html)
  }, function(data) {
    console.log(data)
  })
}

$(function () {
  init_team()
})