<template>
  <div class="container">
    <el-timeline>
      <el-timeline-item
        timestamp="初始化"
        placement="top"
        icon="el-icon-info"
        color="#67C23A"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>接口运行信息</span>
          </div>
          <el-row>
            <el-col :span="8">
              <label>接口ID：</label>{{ log.interface_id }}
            </el-col>
            <el-col :span="8">
              <label>团队：</label>{{ log.team }}
            </el-col>
            <el-col :span="8">
              <label>项目：</label>{{ log.project }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <label>接口名：</label>{{ log.interface_name }}
            </el-col>
            <el-col :span="8">
              <label>开始时间：</label>{{ log.start }}
            </el-col>
            <el-col :span="8">
              <label>结束时间：</label>{{ log.end }}
            </el-col>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="处理请求"
        placement="top"
        icon="el-icon-info"
        color="#67C23A"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>接口请求信息</span>
          </div>
          <el-row>
            <el-col :span="8">
              <label>请求域名：</label>{{ log.request.host }}
            </el-col>
            <el-col :span="8">
              <label>请求路径：</label>{{ log.request.path }}
            </el-col>
            <el-col :span="8">
              <label>请求方法：</label>{{ log.request.method }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <label>请求体类型：</label>{{ log.request.mode }}
            </el-col>
            <el-col :span="8">
              <label>超时时间：</label>{{ log.request.timeout }}
            </el-col>
            <el-col :span="8">
              <label>重试次数：</label>{{ log.request.retry }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求地址：</label>{{ log.request.url }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求头：</label>{{ log.request.header }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求参数：</label>{{ log.request.parameter }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求体：</label>{{ log.request.body }}
            </el-col>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="变量替换"
        placement="top"
        icon="el-icon-question"
        color="#E6A23C"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>变量替换后请求信息</span>
          </div>
          <el-row>
            <el-col :span="8">
              <label>请求域名：</label>{{ log.replace.host }}
            </el-col>
            <el-col :span="8">
              <label>请求路径：</label>{{ log.replace.path }}
            </el-col>
            <el-col :span="8">
              <label>请求地址：</label>{{ log.replace.url }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求头：</label>{{ log.replace.header }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求参数：</label>{{ log.replace.parameter }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <label>请求体：</label>{{ log.replace.body }}
            </el-col>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="处理响应"
        placement="top"
        icon="el-icon-warning"
        color="#F56C6C"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>接口响应信息</span>
          </div>
          <el-row>
            <el-col :span="8">
              <label>响应状态：</label>{{ log.response.code }}
            </el-col>
            <el-col :span="8">
              <label>响应短语：</label>{{ log.response.reason }}
            </el-col>
            <el-col :span="8">
              <label>请求耗时：</label>{{ log.response.elapsed }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <label>响应头：</label>
              <JsonViewer :value="log.response.header" />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <label>响应数据：</label>
              <JsonViewer :value="log.response.data" />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <label>cookie：</label>
              <JsonViewer :value="log.response.cookie" />
            </el-col>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="断言结果"
        placement="top"
        icon="el-icon-warning"
        color="#F56C6C"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>响应断言信息</span>
          </div>
          <div v-if="log.validator">
            <div v-for="(item, i) in log.validator.result" :key="i">
              <el-row>
                <el-col :span="8">
                  <label>提取器：</label>{{ item.extractor }}
                </el-col>
                <el-col :span="8">
                  <label>表达式：</label>{{ item.expression }}
                </el-col>
                <el-col :span="8">
                  <label>比较器：</label>{{ item.operate }}
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="8">
                  <label>期望值：</label>{{ item.expect }}
                </el-col>
                <el-col :span="8">
                  <label>实际值：</label>{{ item.actual }}
                </el-col>
                <el-col :span="8">
                  <label>断言结果：</label>{{ item.status }}
                </el-col>
              </el-row>
              <el-divider />
            </div>
            <label>结果状态：</label>{{ log.validator.status }}
          </div>
          <div v-else>
            []
          </div>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="断言性能"
        placement="top"
        icon="el-icon-s-opportunity"
        color="#409EFF"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>响应性能断言</span>
          </div>
          <el-row>
            <el-col :span="8">
              <label>开始时间：</label>{{ log.performance.start }}
            </el-col>
            <el-col :span="8">
              <label>结束时间：</label>{{ log.performance.end }}
            </el-col>
            <el-col :span="8">
              <label>请求耗时：</label>{{ log.performance.elapsed }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <label>性能阈值：</label>{{ log.performance.threshold }}
            </el-col>
            <el-col :span="8">
              <label>结果状态：</label>{{ log.performance.status }}
            </el-col>
          </el-row>
        </el-card>
      </el-timeline-item>
      <el-timeline-item
        timestamp="传递参数"
        placement="top"
        icon="el-icon-question"
        color="#E6A23C"
        size="large"
      >
        <el-card>
          <div slot="header" class="clearfix">
            <span>提取参数传递给后续接口</span>
          </div>
          <div v-if="log.extractor">
            <div v-for="(item, i) in log.extractor" :key="i">
              <el-row>
                <el-col :span="6">
                  <label>提取器：</label>{{ item.selector }}
                </el-col>
                <el-col :span="6">
                  <label>表达式：</label>{{ item.expression }}
                </el-col>
                <el-col :span="6">
                  <label>变量名：</label>{{ item.variable }}
                </el-col>
                <el-col :span="6">
                  <label>变量值：</label>{{ item.result }}
                </el-col>
              </el-row>
              <el-divider />
            </div>
          </div>
          <div v-else>
            []
          </div>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
import JsonViewer from 'vue-json-viewer'

export default {
  components: {
    JsonViewer
  },
  props: {
    log: {
      type: Object,
      default () {
        return {}
      }
    }
  }
}
</script>

<style scoped>
.container {
  padding-left: 10px;
  padding-right: 10px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.el-row {
  padding-top: 10px;
  padding-bottom: 10px;
}

.download {
  float: right;
}
</style>
