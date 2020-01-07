<template>
  <div class="container">
    <h1 v-if="error.statusCode === 404">
      <div class="error">
        <el-image :src="image.page_not_found" class="image" />
        <span>请求地址不存在，{{ second }}秒后将跳转到首页。</span>
      </div>
    </h1>
    <h1 v-else>An error occurred</h1>
  </div>
</template>

<script>
export default {
  data () {
    return {
      second: 0,
      image: {
        page_not_found: require('assets/img/page_not_found.jpg')
      }
    }
  },
  props: ['error'],
  created () {
    this.second = 5
    this.go()
  },
  methods: {
    go () {
      const router = this.$router
      let second = this.second
      setInterval(function () {
        if (second === 0) {
          router.push({
            path: '/'
          })
        } else {
          second--
        }
      }, 1000, router, second)
    }
  }
}
</script>

<style scoped>
.error {
  text-align: center;
}

.image {
  display: block;
  width: 300px;
  height: 300px;
  text-align: center;
}
</style>
