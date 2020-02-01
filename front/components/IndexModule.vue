<template>
  <div class="block">
    <el-row v-for="(module, i) in modules" :key="module.title">
      <div v-if="i % 2 === 0" class="module">
        <el-col :span="10">
          <el-image
            :src="module.image"
            class="image"
          />
        </el-col>
        <el-col :span="14">
          <el-row>
            <span class="title">{{ module.title }}</span>
          </el-row>
          <el-row>
            <span class="content">{{ module.content }}</span>
          </el-row>
        </el-col>
      </div>
      <div v-else class="module">
        <el-col :span="14">
          <span class="title">{{ module.title }}</span>
          <span class="content">{{ module.content }}</span>
        </el-col>
        <el-col :span="10">
          <el-image
            :src="module.image"
            class="image"
          />
        </el-col>
      </div>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      modules: [
        {
          title: '接口测试',
          image: require('assets/img/module-01.jpg'),
          content: '完善的接口测试功能支持，全局变量替换，接口间参数提取与关联，分隔符与正则断言支持，fixture等应有尽有！'
        },
        {
          title: 'UI自动化',
          image: require('assets/img/module-02.jpg'),
          content: '关键字驱动框架设计，灵活多变，满足一切自动化测试需求！Selenium与Appium双引擎，支持PC和移动端用例混合运行，让自动化不在难！'
        }
      ]
    }
  }
}
</script>

<style scoped>
.image {
  width: 250px;
  height: 250px;
  vertical-align: middle;
  border-style: none;
  border-radius: 100px;
}

.el-col {
  padding-top: 15px;
  padding-bottom: 15px;
}

.title {
  display: block;
  font-size: 32px;
  padding-top: 50px;
  padding-bottom: 10px;
  text-align: left;
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.content {
  display: block;
  font-size: 14px;
  padding-top: 10px;
  padding-bottom: 50px;
  text-align: left;
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.module {
  padding-left: 150px;
  padding-right: 150px;
}
</style>
