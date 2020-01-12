<template>
  <div class="block">
    <el-carousel :interval="5000" :height="height" type="card">
      <el-carousel-item v-for="image in images" :key="image.alt">
        <el-image :src="image.src" style="width: 100%; height: 100%" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  data () {
    return {
      height: '500px',
      images: [
        { src: require('assets/img/carousel-01.jpg'), alt: 'python' },
        { src: require('assets/img/carousel-02.jpg'), alt: 'flask' },
        { src: require('assets/img/carousel-03.jpg'), alt: 'jenkins' },
        { src: require('assets/img/carousel-04.jpg'), alt: 'docker' }
      ]
    }
  },
  mounted () {
    this.height = 0.85 * `${document.documentElement.clientHeight}` + 'px'
  }
}
</script>
