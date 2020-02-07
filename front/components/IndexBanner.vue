<template>
  <div class="banner">
    <el-row>
      <el-col :span="4" v-for="item in data" :key="item.description">
        <el-row class="card">
          <el-col :span="8" :style="{background: item.color}" class="icon">
            <i :class="item.icon" />
          </el-col>
          <el-col :span="16" class="content">
            <div><span class="number">{{ item.number }}</span></div>
            <div><span class="description">{{ item.description }}</span></div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: {
        team: {
          'number': 0,
          'description': '团队数量',
          'icon': 'el-icon-office-building',
          'color': '#FDE9D9'
        },
        project: {
          'number': 0,
          'description': '项目数量',
          'icon': 'el-icon-s-custom',
          'color': '#DAEEF3'
        },
        variable: {
          'number': 0,
          'description': '变量数量',
          'icon': 'el-icon-s-flag',
          'color': '#F2DBDB'
        },
        keyword: {
          'number': 0,
          'description': '关键字数量',
          'icon': 'el-icon-s-promotion',
          'color': '#EAF1DD'
        },
        interface: {
          'number': 0,
          'description': '接口数量',
          'icon': 'el-icon-s-ticket',
          'color': '#C6D9F1'
        },
        suite: {
          'number': 0,
          'description': '套件数量',
          'icon': 'el-icon-s-grid',
          'color': '#DDD9C3'
        }
      }
    }
  },
  mounted () {
    this.count()
  },
  methods: {
    count () {
      this.$axios
        .get('/api/v1/index/count', {})
        .then((res) => {
          if (res.data.status === 0) {
            // this.data = res.data.data
            for (const i in res.data.data) {
              this.data[i].number = res.data.data[i]
            }
          } else {
            const result = this.mysqlParser(res.data.data)
            if (result.code === 0) {
              this.$message({
                type: 'error',
                message: res.data.message,
                center: true
              })
            } else {
              this.$alert(result.message, {
                title: '数据库错误',
                type: 'error'
              })
            }
          }
        }).catch((res) => {
          this.$message({
            type: 'error',
            message: '服务异常，请联系管理员！',
            center: true
          })
        })
    }
  }
}
</script>

<style scoped>
.banner {
  background-color: #F2F2F2;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-left: -20px;
  margin-right: -20px;
}

.card {
  padding-left: 10px;
  padding-right: 10px;
}

.icon {
  height: 100px;
  font-size: 24px;
  border-radius: 5px 0 0 5px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  border-radius: 0 5px 5px 0;
  background-color: #FFFFFF;
}

.number {
  font-size: 48px;
  line-height: 70px;
}

.description {
  font-size: 14px;
  line-height: 30px;
  background-color: #FFFFFF;
}
</style>
