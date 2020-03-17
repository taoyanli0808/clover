<template>
  <div>
    <el-row>
      <el-col><TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" /></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-table
          :data="data"
          @selection-change="handleSelectionChange"
          v-loading="loading"
          element-loading-text="拼命加载中"
          style="width: 100%"
          border
        >
          <el-table-column
            prop="id"
            label="ID"
            width="80"
          />
          <el-table-column
            prop="project"
            label="项目"
            width="150"
          />
          <el-table-column
            prop="team"
            label="团队"
            width="150"
          />
          <el-table-column
            prop="name"
            label="用例"
            width="180"
          />
          <el-table-column
            fixed="right"
            label="操作"
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                @click="handleAdd(scope.$index, scope.row)"
                size="mini"
                icon="el-icon-video-play"
                type="primary"
              >
                添加
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          @current-change="handleCurrentChange"
          :total="total"
          background
          layout="total, prev, pager, next, jumper"
        />
      </el-col>
      <el-col :span="12">
        <div>aaa</div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    TeamProjectCascader
  },
  data () {
    return {
      data: [],
      total: 0,
      limit: 10,
      page: 0,
      team: '',
      project: ''
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
      this.refresh()
    },
    refresh () {
      this.loading = true
      const params = {
        limit: this.limit,
        offset: this.page * this.limit
      }
      if (this.team !== '') {
        params.team = this.team
      }
      if (this.project !== '') {
        params.project = this.project
      }
      this.$axios
        .post('/api/v1/interface/search', params)
        .then((res) => {
          if (res.data.status === 0) {
            this.total = res.data.total
            this.data = res.data.data
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              center: true
            })
          }
          this.loading = false
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '服务出错，请联系管理员',
            center: true
          })
          this.loading = false
        })
    },
    handleCurrentChange (value) {
      this.page = value - 1
      this.refresh()
    },
    handleAdd (index, row) {

    }
  }
}
</script>
