<template>
  <div class="container">
    <div class="block">
      <el-date-picker
        v-model="value2"
        :picker-options="pickerOptions"
        style="float: right;"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
      />
    </div>
    <Banner />
    <div class="block">
      <el-row>
        <el-col :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>套件稳定性</span>
              <el-tooltip class="item" effect="dark" content="套件执行失败计入一次不稳定" placement="top">
                <i class="el-icon-info" />
              </el-tooltip>
              <el-button style="float: right; padding: 3px 0" type="text">查看更多</el-button>
            </div>
            <div v-for="(item, i) in suite" :key="i" class="text item">
              {{ item.path + '-' + item.count }}
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>接口稳定性</span>
              <el-tooltip class="item" effect="dark" content="接口执行异常或断言失败计入一次不稳定" placement="top">
                <i class="el-icon-info" />
              </el-tooltip>
              <el-button style="float: right; padding: 3px 0" type="text">查看更多</el-button>
            </div>
            <div v-for="(item, i) in unstable" :key="i" class="text item">
              {{ item.path + '-' + item.count }}
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>接口耗时</span>
              <el-tooltip class="item" effect="dark" content="接口执行耗时时间排名，取最近一次执行时间" placement="top">
                <i class="el-icon-info" />
              </el-tooltip>
              <el-button style="float: right; padding: 3px 0" type="text">查看更多</el-button>
            </div>
            <div v-for="(item, i) in slow" :key="i" class="text item">
              {{ item.path + '-' + item.count }}
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Banner from '~/components/index/Banner.vue'

export default {
  Banner,
  data () {
    return {
      pickerOptions: {
        disabledDate (time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [
          {
            text: '最近一周',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一个月',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近半年',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },
      value1: '',
      value2: '',
      suite: [],
      unstable: [],
      slow: []
    }
  },
  mounted () {
    this.get_unstable_interface()
    this.get_slow_interface()
  },
  methods: {
    get_unstable_suite () {
      this.suite = [
        {
          'name': '/api/v1/test1',
          'count': 985
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        },
        {
          'name': '/api/v1/test2',
          'count': 112
        }
      ]
    },
    get_unstable_interface () {
      this.unstable = [
        {
          'path': '/api/v1/test1',
          'count': 985
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        }
      ]
    },
    get_slow_interface () {
      this.slow = [
        {
          'path': '/api/v1/test1',
          'count': 985
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        },
        {
          'path': '/api/v1/test2',
          'count': 112
        }
      ]
    }
  }
}
</script>

<style scoped>
.container {
  margin: 0 auto;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
