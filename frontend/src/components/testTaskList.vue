<template>
  <div>
    <nav-menu :activeIndex="activeIndex" :username="username" ref="NavMenu" :projectGroupOptions="projectGroupOptions"></nav-menu>
    <div style="margin-top: 50px;margin-left: 15px;margin-right: 15px">
      <el-row style="float: left">
        <i class="el-icon-info"></i>
        <label style="color: #2a6496;font-size: 5px">只显示最近10次的测试任务</label>
      </el-row>
      <br>
      <br>
      <div>
        <el-tabs v-model="project_id" @tab-click="handlerTaskChange">
          <el-tab-pane v-for="(item,index) in projects" :label="item.project" :name="item.project_id.toString()" :key="index"></el-tab-pane>
        </el-tabs>
      </div>
      <el-table
        height="800"
        :data="tasksList"
        border
        :header-cell-style="{background:'rgba(114,162,165,0.96)',color:'#0f0f10'}"
        :row-class-name="tableRowClassName"
        :default-sort="{prop:'createTime','order':'descending'}">
        <el-table-column label="序号" type="index" width="50">
        </el-table-column>
        <el-table-column
          prop="id"
          label="任务ID"
          sortable
          width="100"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="taskName"
          label="任务名称"
          width="300px"
          sortable
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="casesTotal"
          label="用例数"
          width="150px"
          sortable
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          width="150"
          prop="runMode"
          :formatter="rmFormat"
          label="运行模式"
          sortable>
        </el-table-column>
        <el-table-column
          width="150"
          prop="runNum"
          label="重复次数"
          sortable>
        </el-table-column>
        <el-table-column
          width="150"
          prop="repeatMode"
          :formatter="rpmFormat"
          label="重复模式"
          sortable>
        </el-table-column>
        <el-table-column
          width="120"
          prop="runTime"
          label="定时任务"
          sortable>
        </el-table-column>
        <el-table-column
          width="150"
          prop="taskRunFlag"
          :formatter="trfFormat"
          label="状态"
          sortable>
        </el-table-column>
        <el-table-column
          width="150"
          label="用例进度"
          sortable>
          <span slot-scope="scope">
            <template v-if="scope.row.taskRunFlag === 'unRun'">
              <span>0.00%</span>
          </template>
          <template v-if="scope.row.taskRunFlag === 'True'">
            <el-tooltip placement="top">
              <div slot="content">成功：{{successedTotal}}<br>失败：{{failedTotal}}<br>待执行：{{pendingTotal}}</div>
              <span>{{process}}</span>
            </el-tooltip>
          </template>
          <template v-if="scope.row.taskRunFlag === 'False' || scope.row.taskRunFlag === 'Destroy'">
              <span>100.00%</span>
          </template>
          </span>
        </el-table-column>
        <el-table-column
          width="150"
          prop="ratio"
          label="通过率"
          sortable>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="创建时间"
          sortable>
        </el-table-column>
        <el-table-column
          prop="modifyTime"
          label="更新时间"
          sortable>
        </el-table-column>
        <el-table-column fixed="right" label="操作">
          <span slot-scope="scope">
            <el-button type="text" icon="el-icon-refresh" @click="refreshTask(scope.row)">刷新</el-button>
            <el-button type="text" v-if="scope.row.taskRunFlag === 'True' && scope.row.optUser === username" style="display: none" icon="el-icon-monitor" @click="runConsole(scope.row)">控制台</el-button>
            <el-button type="text" v-if="scope.row.taskRunFlag === 'True' && scope.row.optUser === username" icon="el-icon-refresh-left" style="color: #f66539" @click="destroytVisible(scope.row)">撤销</el-button>
            <el-button type="text" v-if="scope.row.taskRunFlag == 'False' || scope.row.taskRunFlag == 'Destroy'" icon="el-icon-view" @click="viewReport(scope.row)">查看报告</el-button>
            <el-button type="text" v-if="scope.row.isDisplayReRun === 'True'" icon="el-icon-refresh-right" @click="reRunFailed(scope.row)">失败重跑</el-button>
          </span>
        </el-table-column>
      </el-table>
      <el-dialog id="csmdlg" title="控制台" :custom-class="'csmdlgSye'" :visible="dialogConsoleVisible" :before-close='closeConsoleDialog' width="60%" height="50%">
        <el-input id="csm" type="textarea" :rows="25" v-model="consoleMsg"></el-input>
      </el-dialog>
      <el-dialog id="destroyPersonTask" title="警告" :custom-class="'destroyPersonTaskSye'" :visible.sync="dialogDestroytVisible" width="20%">
        <span style="float: left">您要撤销该任务吗？</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogDestroytVisible = false">取 消</el-button>
          <el-button type="primary" @click="destroyTask">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import NavMenu from "./navMenu"
  import {
    checkRunningTask,
    saveTestTask,
    startRunTask,
    testtasksList,
    queryKcpPersonTask,
    queryKcpProcessTask,
    destroyKcpTask,
    loginKcp,
    queryOnePersonTask,
    queryOneProcessTask,
    destroyOneTask,
    loginOne,
    updateTestTask
  } from "../apis/apis"
  import {Loading} from "element-ui";
    export default {
      name: "testTaskList",
      components: {NavMenu},
      data() {
        return {
          activeIndex: "2",
          dialogConsoleVisible: false,
          dialogDestroytVisible: false,
          ws_url:"",
          consoleMsg:"",
          kcpToken:"",
          oneToken:"",
          successedTotal:0,
          failedTotal:0,
          pendingTotal:0,
          process:"0.00%",
          kcp_ws:"ws://172.16.23.63:1689/",
          one_ws:"ws://172.16.23.61:1689/",
          projectGroupOptions:JSON.parse(sessionStorage.getItem('projectGroupOptions')),
          projectGroupProjectList:JSON.parse(sessionStorage.getItem('projectGroupProjectList')),
          username: JSON.parse(sessionStorage.getItem('username')),
          headers: {Authorization: 'Bearer ' + JSON.parse(sessionStorage.getItem('token'))},
          projectGroup_id:0,
          projects:JSON.parse(sessionStorage.getItem('projects')),
          project_id:sessionStorage.getItem("defaultProjectId"),
          tasksList: [],
          taskCaseList: [],
          firstTaskName:"",
          kcpBaseURI: "",
          oneBaseURI: "http://172.16.23.61:11120",
          taskId:0,
          row: new Object(),
          reRunFailedVisible:false,
          reportURL:"",
          offset: 300,
          rescnrt: {
            code: 0
          },
          reqSaveTask: {
            taskName: "",
            casesTotal:0,
            taskRunFlag: "",
            optUser: JSON.parse(sessionStorage.getItem('username')),
            projectGroup_id:0,
            project_id:0,
            runMode:"",
            runPlatform:"",
            runNum:0,
            repeatMode:"",
            runTime:"",
            reRunFlag:"True"
          },
          resSaveTask: {
            taskId:0,
            taskName: "",
            taskRunFlag: "",
            optUser: ""
          },
          reqRunTask: {
            taskId: 0,
            taskName: "",
            project_id: 0,
            runFlag: "",
            runMode:"0",
            runPlatform:"",
            runNum:0,
            repeatMode:"",
            runTime:"",
            reRunFlag:"True"
          },
          resRunTask: {
            code: 0,
            msg: "",
            runningFlag: ""
          }
        }
      },
      methods: {
        trfFormat(row,column) {
          if (row.taskRunFlag === "True") {
            return "正在执行"
          } else if (row.taskRunFlag === "Destroy") {
            return "已撤销"
          } else if (row.taskRunFlag === "unRun") {
            return "未执行"
          } else {
            return "已完成"
          }
        },
        rmFormat(row,column) {
          if (row.runMode === "1") {
            return "全部执行"
          } else {
            return "失败即停止"
          }
        },
        rpmFormat(row,column) {
          if (row.repeatMode === "01") {
            return "顺序迭代"
          } else {
            return "逐一迭代"
          }
        },
        async refreshTask(row) {
          let params = {"id": row["id"]}
          await testtasksList(this.headers, params).then(taskRes => {
            // console.log(res.results[0]["taskRunFlag"],res.results[0]["ratio"])
            // row["taskRunFlag"] = res.results[0]["taskRunFlag"]
            // row["ratio"] = res.results[0]["ratio"]
            let params = {"username": "admin", "password": "admin"}
            if (this.project_id === '1') {
              loginKcp(params).then(res => {
                this.kcpToken = res.token
                let headers = {"token": this.kcpToken}
                let params = {
                  "project_id": this.project_id,
                  "optUser": this.username,
                  "testTask_id": row["id"],
                  "type": "refresh"
                }
                queryKcpPersonTask(headers, params).then(res => {
                  let param = {"headers": {"token": this.kcpToken}}
                  queryKcpProcessTask(headers, param).then(processRes => {
                    this.successedTotal = processRes["data"].successedTotal
                    this.failedTotal = processRes["data"].failedTotal
                    this.pendingTotal = processRes["data"].pendingTotal
                    this.process = processRes["data"].process
                    if (processRes["data"].process === "False") {
                      this.process = "100.00%"
                    }

                    if (taskRes.results[0].taskRunFlag === "False" || taskRes.results[0].taskRunFlag === "Destroy") {
                      row["taskRunFlag"] = res["data"]["taskRunFlag"]
                      row["process"] = this.process
                      row["ratio"] = res["data"]["ratio"]
                      row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                      row["modifyTime"] = taskRes.results[0].modifyTime
                    } else if (taskRes.results[0].taskRunFlag === "True" && row["process"] !== this.process) {
                      let params = {
                        "taskRunFlag": res["data"]["taskRunFlag"],
                        "successedTotal": this.successedTotal,
                        "failedTotal": this.failedTotal,
                        "pendingTotal": this.pendingTotal,
                        "process": this.process,
                        "ratio": res["data"]["ratio"],
                        "reRunFlag": res["data"]["reRunFlag"]
                      }
                      updateTestTask(row["id"], this.headers, params).then(updateRes => {
                        row["taskRunFlag"] = res["data"]["taskRunFlag"]
                        row["process"] = this.process
                        row["ratio"] = res["data"]["ratio"]
                        row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                        row["modifyTime"] = updateRes.modifyTime
                      })
                    } else if (taskRes.results[0].taskRunFlag === "unRun" && res["data"]["taskRunFlag"] === "True") {
                      let params = {
                        "taskRunFlag": res["data"]["taskRunFlag"],
                        "successedTotal": this.successedTotal,
                        "failedTotal": this.failedTotal,
                        "pendingTotal": this.pendingTotal,
                        "process": this.process,
                        "ratio": res["data"]["ratio"],
                        "reRunFlag": res["data"]["reRunFlag"]
                      }
                      updateTestTask(row["id"], this.headers, params).then(updateRes => {
                        row["taskRunFlag"] = res["data"]["taskRunFlag"]
                        row["process"] = this.process
                        row["ratio"] = res["data"]["ratio"]
                        row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                        row["modifyTime"] = updateRes.modifyTime
                      })
                    }
                  })
                })
              })
            } else if (this.project_id === '2') {
              loginOne(params).then(res => {
                this.oneToken = res.token
                let headers = {"token": this.oneToken}
                let params = {
                  "project_id": this.project_id,
                  "optUser": this.username,
                  "testTask_id": row["id"],
                  "type": "refresh"
                }
                queryOnePersonTask(headers, params).then(res => {
                  let param = {"headers": {"token": this.oneToken}}
                  queryOneProcessTask(headers, param).then(processRes => {
                    this.successedTotal = processRes["data"].successedTotal
                    this.failedTotal = processRes["data"].failedTotal
                    this.pendingTotal = processRes["data"].pendingTotal
                    this.process = processRes["data"].process
                    if (processRes["data"].process === "False") {
                      this.process = "100.00%"
                    }

                    if (taskRes.results[0].taskRunFlag === "False" || taskRes.results[0].taskRunFlag === "Destroy") {
                      row["taskRunFlag"] = res["data"]["taskRunFlag"]
                      row["process"] = this.process
                      row["ratio"] = res["data"]["ratio"]
                      row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                      row["modifyTime"] = taskRes.results[0].modifyTime
                    } else if (taskRes.results[0].taskRunFlag === "True" && row["process"] !== this.process) {
                      let params = {
                        "taskRunFlag": res["data"]["taskRunFlag"],
                        "successedTotal": this.successedTotal,
                        "failedTotal": this.failedTotal,
                        "pendingTotal": this.pendingTotal,
                        "process": this.process,
                        "ratio": res["data"]["ratio"],
                        "reRunFlag": res["data"]["reRunFlag"]
                      }
                      updateTestTask(row["id"], this.headers, params).then(updateRes => {
                        row["taskRunFlag"] = res["data"]["taskRunFlag"]
                        row["process"] = this.process
                        row["ratio"] = res["data"]["ratio"]
                        row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                        row["modifyTime"] = updateRes.modifyTime
                      })
                    } else if (taskRes.results[0].taskRunFlag === "unRun" && res["data"]["taskRunFlag"] === "True") {
                      let params = {
                        "taskRunFlag": res["data"]["taskRunFlag"],
                        "successedTotal": this.successedTotal,
                        "failedTotal": this.failedTotal,
                        "pendingTotal": this.pendingTotal,
                        "process": this.process,
                        "ratio": res["data"]["ratio"],
                        "reRunFlag": res["data"]["reRunFlag"]
                      }
                      updateTestTask(row["id"], this.headers, params).then(updateRes => {
                        row["taskRunFlag"] = res["data"]["taskRunFlag"]
                        row["process"] = this.process
                        row["ratio"] = res["data"]["ratio"]
                        row["isDisplayReRun"] = taskRes.results[0].isDisplayReRun
                        row["modifyTime"] = updateRes.modifyTime
                      })
                    }
                  })
                })
              })
            }
          })
        },

        runConsole(row) {
          this.dialogConsoleVisible = true
          this.getConsoleMessage()
        },
        destroytVisible(row) {
          this.dialogDestroytVisible = true
          this.taskId = row['id']
          this.row = row
        },
        async destroyTask() {
          let _this = this
          if (this.project_id === '1') {
            // 查询该任务是否已经结束，未结束则撤销
            let params = {"username":"admin","password":"admin"}
            await loginKcp(params).then(res => {
            if (res.code === 2000) {
              this.visitorAuthToken = res.token
              let headers = {"token":this.visitorAuthToken}
              let params = {"project_id":this.project_id,"optUser":this.username,"testTask_id":this.taskId,"type":"destroy"}
              queryKcpPersonTask(headers,params).then(res => {
                if (res.code === 5000) {
                  this.dialogDestroytVisible = false
                  const options = {
                    text: "拼命撤销当前任务中，此过程可能比较耗时，请稍后",
                    customClass: "login_loading",
                    spinner: "el-icon-loading",
                    lock: true,
                    background:'rgba(0,0,0,0.5)'
                  }
                  this.loadingInstance = Loading.service(options)

                  destroyKcpTask(headers,params).then(res => {
                    if (res.code === 2000) {
                      this.loadingInstance.close()
                      const options_success = {
                        text: "任务撤销成功",
                        customClass: "login_loading",
                        spinner: "el-icon-success",
                        lock: true,
                        background:'rgba(0,0,0,0.5)'
                      }
                      this.loadingInstanceSuccess = Loading.service(options_success)
                      setTimeout(() => {
                        this.loadingInstanceSuccess.close()
                      }, 3000)
                      setTimeout(() => {
                        this.refreshTask(this.row)
                      }, 2000)
                    } else {
                      this.loadingInstance.close()
                      const options_fail = {
                        text: "任务撤销失败，请稍后重试",
                        customClass: "login_loading",
                        spinner: "el-icon-error",
                        lock: true,
                        background:'rgba(0,0,0,0.5)'
                      }
                      this.loadingInstanceFail = Loading.service(options_fail)
                      setTimeout(() => {
                        this.loadingInstanceFail.close()
                      }, 3000)
                    }
                  }).catch(function (error) {
                    _this.loadingInstance.close()
                    _this.$message.error({
                      type:"error",
                      showClose: true,
                      offset:_this.offset,
                      message:"接口请求异常或超时，撤销结果以企业微信通知为准"
                    })
                  })
                } else if (res.code === 2000){
                  this.dialogDestroytVisible = false
                  this.$message({
                    type: "success",
                    showClose: true,
                    offset: this.offset,
                    message: "任务已结束"
                  })
                }
              }).catch(function (error) {
                _this.$message.error({
                  type:"error",
                  showClose: true,
                  offset:_this.offset,
                  message:"接口请求异常"
                })
              })
            } else {
              this.$message({
                type: "error",
                showClose: true,
                offset: this.offset,
                message: "登录失败"
              })
            }
            }).catch(function (error) {
              _this.$message.error({
                type:"error",
                showClose: true,
                offset:_this.offset,
                message:"获取授权失败，请联系管理员！"
              })
            })
          } else if (this.project_id === '2') {
            // 查询该任务是否已经结束，未结束则撤销
            let params = {"username":"admin","password":"admin"}
            await loginOne(params).then(res => {
            if (res.code === 2000) {
              this.oneToken = res.token
              let headers = {"token":this.oneToken}
              let params = {"project_id":this.project_id,"optUser":this.username,"testTask_id":this.taskId,"type":"destroy"}
              queryOnePersonTask(headers,params).then(res => {
                if (res.code === 5000) {
                  this.dialogDestroytVisible = false
                  const options = {
                    text: "拼命撤销当前任务中，此过程可能比较耗时，请稍后",
                    customClass: "login_loading",
                    spinner: "el-icon-loading",
                    lock: true,
                    background:'rgba(0,0,0,0.5)'
                  }
                  this.loadingInstance = Loading.service(options)

                  destroyOneTask(headers,params).then(res => {
                    if (res.code === 2000) {
                      this.loadingInstance.close()
                      const options_success = {
                        text: "任务撤销成功",
                        customClass: "login_loading",
                        spinner: "el-icon-success",
                        lock: true,
                        background:'rgba(0,0,0,0.5)'
                      }
                      this.loadingInstanceSuccess = Loading.service(options_success)
                      setTimeout(() => {
                        this.loadingInstanceSuccess.close()
                      }, 3000)
                      setTimeout(() => {
                        this.refreshTask(this.row)
                      }, 2000)
                    } else {
                      this.loadingInstance.close()
                      const options_fail = {
                        text: "任务撤销失败，请稍后重试",
                        customClass: "login_loading",
                        spinner: "el-icon-error",
                        lock: true,
                        background:'rgba(0,0,0,0.5)'
                      }
                      this.loadingInstanceFail = Loading.service(options_fail)
                      setTimeout(() => {
                        this.loadingInstanceFail.close()
                      }, 3000)
                    }
                  }).catch(function (error) {
                    _this.loadingInstance.close()
                    _this.$message.error({
                      type:"error",
                      showClose: true,
                      offset:_this.offset,
                      message:"接口请求异常或超时，撤销结果以企业微信通知为准"
                    })
                  })
                } else if (res.code === 2000){
                  this.dialogDestroytVisible = false
                  this.$message({
                    type: "success",
                    showClose: true,
                    offset: this.offset,
                    message: "任务已结束"
                  })
                }
              }).catch(function (error) {
                _this.$message.error({
                  type:"error",
                  showClose: true,
                  offset:_this.offset,
                  message:"接口请求异常"
                })
              })
            } else {
              this.$message({
                type: "error",
                showClose: true,
                offset: this.offset,
                message: "登录失败"
              })
            }
            }).catch(function (error) {
              _this.$message.error({
                type:"error",
                showClose: true,
                offset:_this.offset,
                message:"获取授权失败，请联系管理员！"
              })
            })
          }
        },
        getConsoleMessage() {
          let _this = this
          if (_this.project_id === "1") {
            _this.ws_url = _this.kcp_ws
          } else if (_this.project_id === "2") {
            _this.ws_url = _this.one_ws
          }
          if ("WebSocket" in window) {
            let ws = new WebSocket(_this.ws_url)
            // console.log(ws){

            ws.onopen = function() {
              ws.send(_this.username)

              ws.onmessage = function(evt) {
                _this.consoleMsg += evt.data
                // console.log("收到消息：" + evt.data)
                if (_this.dialogConsoleVisible === true) {
                  let csm = document.getElementById('csm')
                  csm.scrollTop = csm.scrollHeight
                  ws.onclose = function () {
                    // _this.$message({
                    //   type: "success",
                    //   showClose: true,
                    //   offset: _this.offset,
                    //   message: '任务已结束'
                    // })
                    // console.log("连接已关闭")
                  }
                }
              }
            }

            ws.onclose = function () {
              // _this.$message({
              //   type: "success",
              //   showClose: true,
              //   offset: _this.offset,
              //   message: '任务已结束'
              // })
              // console.log("连接已关闭")
            }
          } else {
            _this.$message({
              type: "error",
              showClose: true,
              offset: _this.offset,
              message: '浏览器不支持控制台!'
            })
            // console.log("浏览器不支持!")
          }
        },
        closeConsoleDialog() {
          this.dialogConsoleVisible = false
        },
        //检测当前项目是否有测试任务
        async checkNotRunningTask(projectId) {
          let params = {"project": projectId}
          await checkRunningTask(this.headers, params).then(res => {
            let {code} = res
            this.rescnrt.code = code
          })
        },
        handlerTaskChange(name) {
          // console.log(name.name)
          if (name.name !== undefined) {
            sessionStorage.setItem("defaultProjectId",name.name)
          }
          this.project_id = sessionStorage.getItem("defaultProjectId")
          this.getTasksList()
        // console.log(name)
        // this.currentProjectId = name.name
        // console.log("11222")
        // this.getCasesList()
      },
        //保存测试任务
        async saveRunTestTask(taskName, taskRunFlag, projectGroup_id,project_id,runMode,runPlatform,runNum,repeatMode) {
          this.reqSaveTask.taskName = taskName
          this.reqSaveTask.taskRunFlag = taskRunFlag
          this.reqSaveTask.projectGroup_id = projectGroup_id
          this.reqSaveTask.project_id = project_id
          this.reqSaveTask.runMode = runMode
          this.reqSaveTask.runPlatform = runPlatform
          this.reqSaveTask.runNum = runNum
          this.reqSaveTask.repeatMode = repeatMode
          // console.log(this.reqSaveTask)
          await saveTestTask(this.headers, this.reqSaveTask).then(res => {
            let {id, taskName, optUser, taskRunFlag} = res
            this.resSaveTask.taskId = id
            this.resSaveTask.taskName = taskName
            this.resSaveTask.optUser = optUser
            this.resSaveTask.taskRunFlag = taskRunFlag
          })
        },
        //启动测试任务
        async runTestTask(taskName, project_id,taskRunFlag) {
          this.reqRunTask.taskId = this.resSaveTask.taskId
          this.reqRunTask.taskName = taskName
          this.reqRunTask.project_id = project_id
          this.reqRunTask.runFlag = taskRunFlag
          this.reqRunTask.runMode = this.reqSaveTask.runMode
          this.reqRunTask.runPlatform = this.reqSaveTask.runPlatform
          this.reqRunTask.runNum = this.reqSaveTask.runNum
          this.reqRunTask.repeatMode = this.reqSaveTask.repeatMode
          // console.log(this.reqRunTask)
          await startRunTask(this.headers, this.reqRunTask).then(res => {
            let {code, msg, runningFlag} = res
            this.resRunTask.code = code
            this.resRunTask.msg = msg
            this.resRunTask.runningFlag = runningFlag
          })
        },
        async reRunFailed(row) {
          let params = {"id":row["id"]}
          await testtasksList(this.headers,params).then(res =>{
             if (res.results[0]["isDisplayReRun"] === "True"){
                let taskName = row["taskName"] + "_失败重跑"
                let project_id = row["project_id"]
                let projectGroup_id = row["projectGroup_id"]
                let taskRunFlag = "unRun"
                let runMode = "1"
                let runPlatform = row["runPlatform"]
                let runNum = 1
                let repeatMode = "02"
                let _this = this
                this.checkNotRunningTask(project_id).then(res => {
                  // console.log(this.rescnrt.code)
                  if (this.rescnrt.code === 2000) {
                    this.$message({
                      type: 'error',
                      showClose: true,
                      offset: this.offset,
                      message: '当前项目有测试任务在进行，请稍后提交'
                    })
                  } else {
                    this.saveRunTestTask(taskName, taskRunFlag, projectGroup_id, project_id,runMode,runPlatform,runNum,repeatMode).then(res => {
                      if (this.resSaveTask.taskName === taskName) {
                        this.runTestTask(taskName,project_id,taskRunFlag).then(res => {
                          if (this.resRunTask.code === 2000) {
                            // this.$message({
                            //   type: 'success',
                            //   showClose: true,
                            //   duration: 5000,
                            //   offset: this.offset,
                            //   message: '测试任务【' + taskName + '】执行中...'
                            // })
                            const options_task = {
                                text: '测试任务【' + taskName + '】执行中，即将刷新',
                                customClass: "login_loading",
                                spinner: "el-icon-success",
                                lock: true,
                                background:'rgba(0,0,0,0.5)'
                              }
                              this.loadingInstanceTask = Loading.service(options_task)
                              // sessionStorage.setItem("flag","2")
                              setTimeout(() => {
                                // this.dialogFormVisible = false
                                this.loadingInstanceTask.close()
                                this.$router.go(0)
                                }, 8000)
                          } else {
                            this.$message.error({
                              type: "error",
                              showClose: true,
                              offset: this.offset,
                              message: "当前项目有测试任务在进行，请稍后提交"
                            })
                          }
                        })
                      }
                    }).catch(function (error) {
                      _this.$message.error({
                        type:"error",
                        showClose: true,
                        offset:_this.offset,
                        message:"该测试任务已存在"
                      })
                    })
                  }
                })
             } else {
               this.$message({
                type: 'info',
                showClose: true,
                offset: this.offset,
                message: '当前任务已关闭该功能'
              })
             }
          })
        },
        viewReport(row) {
          // console.log(row)
          // this.project_id = row["project_id"]
          this.taskId = row["id"]
          let username = row["optUser"]
          if (this.project_id === '1') {
            this.reportURL = this.kcpBaseURI + "/" + username + "/" + this.taskId + "/allure_report/index.html"
          } else if (this.project_id === '2') {
            this.reportURL = this.oneBaseURI + "/" + username + "/" + this.taskId + "/allure_report/index.html"
          }
          window.open(this.reportURL,"_blank")
        },
        tableRowClassName(row) {
          if (row.row.ratio === "100.00%") {
            return 'success-row-task'
          }else{
            return 'warning-row-task'
          }
        },
        switchSelected(index, keyPath) {
          // console.log(index, typeof (index), keyPath)
          if (index === "1") {
            this.$router.push({name: 'casesList'})
          }
        },
        async getTasksList() {
          // if (this.project_id !== "10") {
          //   this.getConsoleMessage()
          // }
          let params = {"page":1,
            "page_size":10,
            "projectGroup_id": sessionStorage.getItem('projectGroup'),
            "project_id": sessionStorage.getItem('defaultProjectId'),
            // "optUser": JSON.parse(sessionStorage.getItem('username')),
            "ordering": "-createTime"}
          const options = {
            text: "正在加载...",
            customClass: "login_loading",
            spinner: "el-icon-loading",
            lock: true,
            background: 'rgba(0,0,0,0)'
          }
          this.loadingTasks = Loading.service(options)
          await testtasksList(this.headers,params).then(res =>{
            this.loadingTasks.close()
            this.tasksList = res.results
            if (this.tasksList[0].taskRunFlag === "True") {
              this.refreshTask(this.tasksList[0])
            }
          })
        },
      },
      mounted() {
        this.getTasksList()
        this.$refs.NavMenu.changeProjectGroup()
      }
    }
</script>

<style>
  .el-table .warning-row-task {
    background: oldlace;
  }

  .el-table .success-row-task {
    background: #f0f9eb;
  }

  #csmdlg {
    top: 1%;
  }

  #csmdlg .csmdlgSye{
    border-radius: 10px;
  }

  #csmdlg .el-dialog__header {
    background-color: rgba(213, 219, 216, 0.9);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #csmdlg .el-dialog__body {
    background-color: rgba(243, 242, 223, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #csm {
    background-color: rgba(17, 9, 5, 0.90);
    color: #FFFFFF;
  }

  #csmktbraindlg {
    top: 1%;
  }

  #csmktbraindlg .csmktbraindlgSye{
    border-radius: 10px;
  }

  #csmktbraindlg .el-dialog__header {
    background-color: rgba(213, 219, 216, 0.9);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #csmktbraindlg .el-dialog__body {
    background-color: rgba(243, 242, 223, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #csmktbrain {
    background-color: rgba(17, 9, 5, 0.90);
    color: #FFFFFF;
  }

  #destroyPersonTask {
    top: 16%;
  }

    #destroyPersonTask .destroyPersonTaskSye{
    border-radius: 10px;
  }

  #destroyPersonTask .el-dialog__header {
    background-color: rgba(213, 219, 216, 0.9);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #destroyPersonTask .el-dialog__body {
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  #destroyPersonTask .el-dialog__footer{
    background-color: rgba(246, 246, 244, 0.68);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }
</style>
