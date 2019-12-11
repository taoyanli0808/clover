<template>
  <div class="block">
    <el-carousel height="760px">
      <el-carousel-item v-for="item in images" :key="item.alt">
        <el-image
          style="width: 100%; height: 100%"
          :src="item.img"
          :fit="fit"
        />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  data () {
    return {
      images: [
        {
          img: require('../assets/img/carousel-01.png'),
          alt: 'carousel-01.png'
        },
        {
          img: require('../assets/img/carousel-02.png'),
          alt: 'carousel-02.png'
        },
        {
          img: require('../assets/img/carousel-03.jpeg'),
          alt: 'carousel-03.png'
        }
      ]
    }
  }
}
</script>

<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
</style>
