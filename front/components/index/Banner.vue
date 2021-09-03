<template>
  <div>
    <el-card class="box-card">
      <div slot="header" style="float: left;">
        <span>卡片名称</span>
      </div>
      <div v-for="o in 4" :key="o" class="text item">
        <div>项目</div>
        <el-divider direction="vertical" />
        <div>方案</div>
        <el-divider direction="vertical" />
        <div>套件</div>
        <el-divider direction="vertical" />
        <div>接口</div>
        <el-divider direction="vertical" />
        <div>变量</div>
        <el-divider direction="vertical" />
        <div>关键字</div>
      </div>
    </el-card>
  </div>
</template>
