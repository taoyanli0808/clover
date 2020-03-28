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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
            <TeamProjectCascader v-on:selectedTeamProject="selectedTeamProject" />
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
import TeamProjectCascader from '~/components/TeamProjectCascader.vue'

export default {
  components: {
    JmeterPlugin,
    PostmanPlugin,
    HTTPRunnerPlugin,
    CharlesPlugin,
    TeamProjectCascader
  },
  data () {
    return {
      team: '',
      project: '',
      plugin: '',
      file: '',
      fileList: []
    }
  },
  methods: {
    selectedTeamProject (value) {
      this.team = value.team
      this.project = value.project
    }
  }
}
</script>
