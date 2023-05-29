<template>
  <div>
    <nav-menu :activeIndex="activeIndex" :username="username" ref="NavMenu" :projectGroupOptions="projectGroupOptions"></nav-menu>
    <div style="margin-top: 50px;margin-left: 15px;margin-right: 15px">
      <el-table
          :data="toolsData"
          border
          :header-cell-style="{background:'rgba(83,170,175,0.96)',color:'#0f0f10'}"
          style="width: 100%"
          :default-sort="{prop:'updateTime','order':'descending'}">
          <el-table-column label="序号" type="index" width="50">
          </el-table-column>
          <el-table-column
            prop="toolName"
            label="软件名称"
            width="300px"
            sortable
            show-overflow-tooltip>
          </el-table-column>
          <el-table-column
            prop="toolDesc"
            label="描述"
            sortable>
          </el-table-column>
          <el-table-column
            prop="author"
            label="作者"
            sortable>
          </el-table-column>
          <el-table-column
            prop="version"
            label="版本"
            sortable>
          </el-table-column>
          <el-table-column
            prop="updateTime"
            label="更新时间"
            sortable>
          </el-table-column>
          <el-table-column fixed="right" label="操作">
            <span slot-scope="scope">
              <el-button type="text" icon="el-icon-download" @click="downLoadTool(scope.row)">下载</el-button>
            </span>
          </el-table-column>
        </el-table>
    </div>
  </div>
</template>

<script>
  import NavMenu from "./navMenu"

  export default {
    name: "toolDownLoad",
    components: {NavMenu},
    data() {
      return {
        activeIndex: "5",
        projectGroupOptions:JSON.parse(sessionStorage.getItem('projectGroupOptions')),
        username: JSON.parse(sessionStorage.getItem('username')),
        projectGroupProjectList:JSON.parse(sessionStorage.getItem('projectGroupProjectList')),
        toolsData: [],
      }
    },
    methods: {
      downLoadTool(row) {
        let url = ""
        this.dluTool(url)
      },
      dluTool(url) {
        let a = document.createElement("a")
        a.setAttribute("download","")
        a.href = url
        a.click()
      },
    },
  }
</script>

<style scoped>

</style>
