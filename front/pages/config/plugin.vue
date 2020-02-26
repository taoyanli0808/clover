<template>
  <div>
    <el-row :gutter="20">
      <el-col span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Postman插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <PostmanPlugin />
          </div>
        </el-card>
      </el-col>
      <el-col span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Jmeter插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
            <JmeterPlugin />
          </div>
        </el-card>
      </el-col>
      <el-col span="8">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Httprunner插件</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
            <HTTPRunnerPlugin />
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

export default {
  components: {
    JmeterPlugin,
    PostmanPlugin,
    HTTPRunnerPlugin
  },
  data () {
    return {
      plugin: '',
      file: '',
      fileList: []
    }
  }
}
</script>
