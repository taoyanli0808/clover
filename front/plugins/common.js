import Vue from 'vue'

const clover = {
  install (Vue, options) {
    /*
    * 由于后端暂时没有好的mysql请求出错处理方案，因此统一处理暂时放在前端。
    * 通常错误发生时是数据库字段确实或者表不存在这种需要手动处理的错误。
    */
    Vue.prototype.mysqlParser = function (message) {
      try {
        const msg = message.split('\n')[0].split(') (')[1]
        const info = msg.slice(0, msg.length - 1).split(',')
        return { code: info[0], message: info[1] }
      } catch (exception) {
        return { code: 0, message: 'ok' }
      }
    }
    /*
    * 动态下载文件的方法，参数为自定义文件名和文件内容。
    */
    Vue.prototype.download = function (filename, text) {
      const pom = document.createElement('a')
      pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text))
      pom.setAttribute('download', filename)
      if (document.createEvent) {
        const event = document.createEvent('MouseEvents')
        event.initEvent('click', true, true)
        pom.dispatchEvent(event)
      } else {
        pom.click()
      }
    }
  }
}

Vue.use(clover)
