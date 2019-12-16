<template>
  <el-table
    :data="tableData"
    style="width: 100%"
  >
    <el-table-column
      prop="date"
      label="日期"
      width="180"
    />
    <el-table-column
      prop="name"
      label="姓名"
      width="180"
    />
    <el-table-column
      prop="address"
      label="地址"
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
</template>

<script>
export default {
  data () {
    return {
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄'
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄'
      }]
    }
  },
  methods: {
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
            type: 'team',
            id_list: [row._id]
          }),
          headers: {
            'Content-Type': 'application/json;'
          }
        }).then((res) => {
          this.refresh()
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
