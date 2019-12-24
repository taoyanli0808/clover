<template>
  <div>
    <TeamSelector v-on:selectedTeam="selectedTeam" />
    <el-table
      :data="data"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column
        prop="environment.project"
        label="项目"
        width="180"
      />
      <el-table-column
        prop="environment.team"
        label="团队"
        width="180"
      />
      <el-table-column
        prop="request.name"
        label="用例"
        width="180"
      />
      <el-table-column
        prop="request.method"
        label="方法"
        width="80"
      />
      <el-table-column
        prop="request.name"
        label="用例"
        width="180"
      />
      <el-table-column
        prop="request.host"
        label="域名"
        width="180"
      />
      <el-table-column
        prop="request.path"
        label="路径"
        width="180"
      />
      <el-table-column
        prop="created"
        label="创建时间"
        width="180"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            @click="handleAdd(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-plus"
            type="primary"
          >
            添加
          </el-button>
          <el-button
            @click="handleEdit(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-edit"
            type="warning"
          >
            编辑
          </el-button>
          <el-button
            @click="handleDelete(scope.$index, scope.row)"
            size="mini"
            icon="el-icon-delete"
            type="danger"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import TeamSelector from '~/components/TeamSelector.vue'

export default {
  components: {
    TeamSelector
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
    refresh () {
      const params = {
        limit: this.limit,
        skip: this.page * this.limit
      }
      if (this.team !== '') {
        params.environment = {}
        params.environment.team = this.team
      }
      this.$axios
        .post('/api/v1/interface/search', params)
        .then((res) => {
          console.log(res)
          this.total = res.data.total
          this.data = res.data.data
        })
    },
    selectedTeam (value) {
      this.team = value
      this.refresh()
    },
    handleAdd (index, row) {
      this.$router.push({
        path: '/interface/create'
      })
    },
    handleEdit (index, row) {
      this.$router.push({
        path: '/interface/edit'
      })
    },
    handleDelete (index, row) {
      this.$confirm('此操作将永久删除该接口, 是否继续?', '删除接口', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios({
          url: '/api/v1/interface/delete',
          method: 'post',
          data: JSON.stringify({
            id_list: [row._id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          this.fetch()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>
