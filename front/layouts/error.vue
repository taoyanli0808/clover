<template>
  <div class="container">
    <h1 v-if="error.statusCode === 404">
      <div class="error">
        <el-row>
          <el-image :src="image.page_not_found" class="image" />
        </el-row>
        <el-row>
          <span>请求地址不存在，{{ second }}秒后将跳转到首页。</span>
        </el-row>
      </div>
    </h1>
    <h1 v-else>
      An error occurred
    </h1>
  </div>
</template>

<script>
export default {
  props: ['error'],
  data () {
    return {
      second: 5,
      image: {
        page_not_found: require('assets/img/page_not_found.jpg')
      }
    }
  },
  created () {
    setInterval(this.count, 1000)
  },
  methods: {
    count () {
      if (this.second === 0) {
        this.$router.push({
          path: '/'
        })
      } else {
        this.second--
      }
    }
  }
}
</script>

<style scoped>
.error {
  text-align: center;
}

.image {
  width: 600px;
  height: 300px;
  text-align: center;
}
</style>
