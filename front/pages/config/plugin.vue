<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Postman插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <PostmanPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Jmeter插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <JmeterPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Httprunner插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <HTTPRunnerPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Charles插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <CharlesPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Fiddler插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <JmeterPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>MITMProxy</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <HTTPRunnerPlugin :team="team" :project="project" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import JmeterPlugin from '~/components/plugin/JmeterPlugin.vue'
import PostmanPlugin from '~/components/plugin/PostmanPlugin.vue'
import HTTPRunnerPlugin from '~/components/plugin/HTTPRunnerPlugin.vue'
import CharlesPlugin from '~/components/plugin/CharlesPlugin.vue'

export default {
  components: {
    JmeterPlugin,
    PostmanPlugin,
    HTTPRunnerPlugin,
    CharlesPlugin
  },
  data () {
    return {
      team: '',
      project: '',
      plugin: '',
      file: '',
      fileList: []
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
