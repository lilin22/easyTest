<template>
  <div>
    <el-menu :default-active="activeIndex" mode="horizontal" @select="switchSelected"
             background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" >
      <el-menu-item index="1">测试用例</el-menu-item>
      <el-menu-item index="2">任务列表</el-menu-item>
      <el-menu-item index="3">自动化脚本开发</el-menu-item>
      <el-menu-item index="4">图表分析</el-menu-item>
      <el-menu-item index="5">下载</el-menu-item>
      <el-submenu index="6">
        <template slot="title">个人中心</template>
        <el-menu-item index="6-1">我的资料</el-menu-item>
        <el-menu-item index="6-2">会员充值</el-menu-item>
        <el-menu-item index="6-3">退出</el-menu-item>
      </el-submenu>
      <el-button type="text" @click="dialogLogoutVisible = true" style="color: rgba(219,148,85,0.97);float: right;margin-top: 12px;margin-right: 10px">退出</el-button>
      <el-button type="text" @click="dialogSetPasswordVisible = true" style="color: rgba(219,148,85,0.97);float: right;margin-top: 12px;margin-right: 10px">修改密码</el-button>
      <el-avatar style="float: right;margin-top: 12px;margin-right: 20px" src="https://img1.baidu.com/it/u=2122215506,2188592051&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=526"></el-avatar>
      <el-button type="text" style="color: lightseagreen;float: right;margin-top: 12px;margin-right: 10px">欢迎你,{{ username }}</el-button>
<!--      <el-button type="text" style="color: lightseagreen;float: right;margin-top: 12px;margin-right: 20px">{{ projectGroupName }}</el-button>-->
      <el-select id="select_default" v-model="defaultProjectGroup" popper-class="select-projectGroup" :popper-append-to-body="false" style="float: right;margin-top: 12px;margin-right: 20px;width: 3.5cm" @change="changeProjectGroup" placeholder="更新中...">
        <el-option id="select_options"
          v-for="item in projectGroupOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-dialog id="modifyPsw" title="修改密码" :custom-class="'modifyPswSye'" :visible.sync="dialogSetPasswordVisible" width="20%">
        <el-form label-width="80px">
          <el-form-item label="原 密 码:">
            <el-input type="password" v-model="user.old_password" style="width: 200px;margin-left:15px"></el-input>
          </el-form-item>
          <el-form-item label="新 密 码:">
            <el-input type="password" v-model="user.new_password" style="width: 200px;margin-left:15px"></el-input>
          </el-form-item>
          <el-form-item label="确认新密码:" label-width="100px">
            <el-input type="password" v-model="user.repeat_password" style="width: 200px"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogSetPasswordVisible = false">取 消</el-button>
          <el-button type="primary" @click="setPassword">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog id="logout" title="提示" :custom-class="'logoutSye'" :visible.sync="dialogLogoutVisible" width="20%">
        <span style="float: left">您要退出系统吗？</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogLogoutVisible = false">取 消</el-button>
          <el-button type="primary" @click="logout">确 定</el-button>
        </span>
      </el-dialog>
    </el-menu>
  </div>
</template>

<script>
  import {modifyPassword} from "../apis/apis"
  export default {
    name: "NavMenu",
    data() {
      return {
        headers: {Authorization: 'Bearer ' + JSON.parse(sessionStorage.getItem('token'))},
        // username: JSON.parse(sessionStorage.getItem('username')),
        offset: 300,
        dialogLogoutVisible: this.isdialogLogoutVisible,
        dialogSetPasswordVisible: this.isdialogSetPasswordVisible,
        user: {
          "old_password": "",
          "new_password": "",
          "repeat_password": "",
        },
        defaultProjectGroup:sessionStorage.getItem("defaultProjectGroup"),
        first:0
      }
    },
    props: ['activeIndex', 'username','projectGroupOptions'],
    methods: {
      switchSelected(index, keyPath) {
        sessionStorage.setItem("flag",index)
        if (index === "1") {
          this.$router.push({name: 'casesList'})
        } else if (index === "2") {
          this.$router.push({
            name: 'taskList',
          })
        } else if (index === "4") {
          this.$router.push({
            name: 'projectsGraph',
          })
        } else if (index === "5") {
          this.$router.push({
            name: 'download',
          })
        } else {
          sessionStorage.setItem("flag","1")
          this.$router.push({name: 'casesList'})
        }
      },
      changeProjectGroup(val) {
        if (val === undefined) {
          this.$parent.projectGroupOptions = JSON.parse(sessionStorage.getItem('projectGroupOptions'))
          if (sessionStorage.getItem("defaultProjectGroup") !== null){
            this.defaultProjectGroup = sessionStorage.getItem("defaultProjectGroup")
          }
        }
        this.first += 1
        if ((val === undefined) && (this.first === 1) && (sessionStorage.getItem("flag") === null)) {
          setTimeout(() => {
            this.defaultProjectGroup = this.$parent.defaultProjectGroup
            sessionStorage.setItem("defaultProjectGroup",this.defaultProjectGroup)
          }, 1000)
        }
        for (let index in this.$parent.projectGroupProjectList) {
          if(this.$parent.projectGroupProjectList[index].projectGroup_id === val) {
            this.$parent.projects = this.$parent.projectGroupProjectList[index].data
            this.$parent.projectGroupId = this.$parent.projectGroupProjectList[index].projectGroup_id
            this.$parent.defaultProjectId = this.$parent.projectGroupProjectList[index].data[0].project_id.toString()
            this.defaultProjectGroup = this.$parent.projectGroupProjectList[index].projectGroup
            sessionStorage.setItem("projects",JSON.stringify(this.$parent.projects))
            sessionStorage.setItem("projectGroup",this.$parent.projectGroupId)
            sessionStorage.setItem("defaultProjectGroup",this.defaultProjectGroup)
            sessionStorage.setItem("defaultProjectId",this.$parent.defaultProjectId)
            this.$parent.defaultProjectId = sessionStorage.getItem("defaultProjectId")
          }
        }
        if (sessionStorage.getItem("flag") === null || sessionStorage.getItem("flag") === "1") {
          this.$parent.handlerChange(name)
        } else if (sessionStorage.getItem("flag") === "2") {
          this.$parent.handlerTaskChange(name)
        }
      },
      logout() {
        this.dialogLogoutVisible = false
        sessionStorage.clear()
        this.$router.push({name: 'login'})
      },
      async setPassword() {
        let _this = this
        let params = {
          "old_password": this.user.old_password,
          "new_password": this.user.new_password,
          "repeat_password": this.user.repeat_password
        }
        await modifyPassword(this.headers, params).then(res => {
          if (res.code === 2000) {
            this.dialogSetPasswordVisible = false
            this.$message({
              type: 'success',
              showClose: true,
              offset: this.offset,
              message: '修改密码成功'
            })
          } else {
            this.$message.error({
              type: "error",
              showClose: true,
              offset: this.offset,
              message: res.err_msg
            })
          }
        }).catch(function (error) {
          if (error.response) {
            _this.$message.error({
              type: "error",
              showClose: true,
              offset: _this.offset,
              message: "请求接口错误"
            })
          }
        })
      }
    },
    watch: {
      isdialogLogoutVisible(val) {
        this.dialogLogoutVisible = val
      },
      isdialogSetPasswordVisible(val) {
        this.dialogSetPasswordVisible = val
      }
    }
  }

</script>
<style>
  #select_default {
    border-style: solid;
    border-color: lightseagreen !important;
    background-color: rgb(84, 92, 100) !important;
    color: lightseagreen !important;
  }
  #select_options {
    float: left;
    /*background-color: rgb(84, 92, 100) !important;*/
    color: lightseagreen !important;
  }
  .select-projectGroup {
    background-color: rgb(84, 92, 100) !important;
  }

  #modifyPsw {
    top: 10%;
  }

  #modifyPsw .modifyPswSye {
    border-radius: 10px;
  }

  #modifyPsw .el-dialog__header {
    background-color: rgba(213, 236, 170, 0.9);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #modifyPsw .el-dialog__body {
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #modifyPsw .el-dialog__footer{
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #logout {
    top: 10%;
  }

  #logout .logoutSye {
    border-radius: 10px;
  }

  #logout .el-dialog__header {
    background-color: rgba(213, 236, 170, 0.9);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #logout .el-dialog__body {
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #logout .el-dialog__footer{
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }
</style>
