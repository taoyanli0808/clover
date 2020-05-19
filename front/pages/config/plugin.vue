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
            <span>待开放</span>
            <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          </div>
          <div class="text item">
            <el-image :src="image.src" style="width: 100%; height: 100%;" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PostmanPlugin from '~/components/plugin/PostmanPlugin.vue'
import CharlesPlugin from '~/components/plugin/CharlesPlugin.vue'

export default {
  components: {
    PostmanPlugin,
    CharlesPlugin
  },
  data () {
    return {
      team: '',
      project: '',
      plugin: '',
      file: '',
      fileList: [],
      image: { src: require('assets/img/plugin.png'), alt: 'plugin' }
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}

img {
  height: 50%;
}
</style>
