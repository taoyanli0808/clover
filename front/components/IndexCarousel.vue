<template>
  <div class="block">
    <el-carousel height="500px">
      <el-carousel-item v-for="image in images" :key="image.alt">
        <el-image :src="image.src" :fit="fill" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  data () {
    return {
      images: [
        { src: require('assets/img/carousel-01.jpg'), alt: 'python' },
        { src: require('assets/img/carousel-02.jpg'), alt: 'flask' },
        { src: require('assets/img/carousel-03.jpg'), alt: 'jenkins' },
        { src: require('assets/img/carousel-04.jpg'), alt: 'docker' }
      ]
    }
  }
}
</script>
