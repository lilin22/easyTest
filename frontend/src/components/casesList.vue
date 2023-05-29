<template>
  <div>
    <nav-menu :activeIndex="activeIndex" :username="username" ref="NavMenu" :projectGroupOptions="projectGroupOptions"></nav-menu>
<!--      <div>-->
<!--        <child v-on:getCurrentProjectGroupId="changeProjectGroup"></child>-->
<!--      </div>-->
    <div style="margin-top: 30px;margin-left: 15px;margin-right: 15px">
      <el-form ref="search" :model="search" label-width="100px">
        <el-row>
          <el-col :span="4">
              <el-form-item label="业务模块:" label-width="80px" style="width: 300px">
                  <el-select v-model="search.moduleOptions.value" :multiple="true" :key="moduleKey" filterable placeholder="请选择">
                    <el-option
                      v-for="item in search.moduleOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
  <!--                  <el-option label="冒烟测试" value="1"></el-option>-->
  <!--                  <el-option label="全部" value="['1','2']"></el-option>-->
                  </el-select>
                </el-form-item>
          </el-col>
          <el-col :span="4">
              <el-form-item label="用例编号:" label-width="80px" style="width: 300px">
                <el-input v-model="search.caseNo" placeholder="关键字"></el-input>
              </el-form-item>
          </el-col>
          <el-col :span="4">
              <el-form-item label="用例标题:" label-width="80px" style="width: 300px">
                <el-input v-model="search.title" placeholder="关键字"></el-input>
              </el-form-item>
          </el-col>
          <el-col :span="4">
              <el-form-item label="类型:" label-width="44px" style="width: 300px">
<!--                <label>类型：</label>-->
                <el-select v-model="search.typeOptions.value" placeholder="请选择">
                  <el-option
                    v-for="item in search.typeOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
<!--                  <el-option label="冒烟测试" value="1"></el-option>-->
<!--                  <el-option label="全部" value="['1','2']"></el-option>-->
                </el-select>
              </el-form-item>
          </el-col>
          <el-col :span="4">
              <el-form-item label="等级:" label-width="44px" style="width: 300px">
<!--                <label>等级：</label>-->
                <el-select v-model="search.levelOptions.value" :multiple="true" placeholder="请选择">
                  <el-option
                    v-for="item in search.levelOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
<!--                <el-select v-model="search.level" :multiple="true" placeholder="请选择">-->
<!--                  <el-option label="紧急" value="1"></el-option>-->
<!--                  <el-option label="高" value="2"></el-option>-->
<!--                  <el-option label="中" value="3"></el-option>-->
<!--                  <el-option label="低" value="4"></el-option>-->
<!--                  <el-option label="无关紧要" value="5"></el-option>-->
              </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-button type="success" icon="el-icon-search" @click="searchcases">搜索</el-button>
            <el-button type="warning" icon="el-icon-s-open" @click="reset">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <div style="margin-top: 15px;margin-left: 15px;margin-right: 15px">
      <div>
        <el-tabs v-model="defaultProjectId" @tab-click="handlerChange">
          <el-tab-pane v-for="(item,index) in projects" :label="item.project" :name="item.project_id.toString()" :key="index"></el-tab-pane>
        </el-tabs>
      </div>
      <u-table
        height="450"
        ref = "multipleTable"
        :data="caseslist"
        use-virtual
        border
        :header-cell-style="{background:'rgba(114,162,165,0.96)',color:'#0f0f10'}"
        :row-class-name="tableRowClassName"
        style="width: 100%;height: 100%;overflow: auto"
        @selection-change="selectionChange">
    <!--    max-height="600"-->
    <!--    :default-sort="{prop:'modifyTime','order':'descending'}">-->
        <u-table-column
          type="selection"
          width="55">
        </u-table-column>
        <u-table-column label="序号" type="index" width="50"></u-table-column>
        <u-table-column
          prop="caseNo"
          label="用例编号"
          sortable>
        </u-table-column>
        <u-table-column
          prop="busmodule"
          label="业务模块"
          :formatter="moduleFormat"
          show-overflow-tooltip>
        </u-table-column>
        <u-table-column
          prop="casename"
          label="用例标题"
          width="600"
          show-overflow-tooltip>
        </u-table-column>
        <u-table-column
          prop="caseType"
          label="类型"
          :formatter="typeFormat"
          sortable>
        </u-table-column>
        <u-table-column
          prop="caseLevel"
          label="等级"
          :formatter="levelFormat"
          sortable>
        </u-table-column>
        <u-table-column
          prop="caseFile"
          label="文件名称">
        </u-table-column>
        <u-table-column
          prop="caseModule"
          label="类名">
        </u-table-column>
        <u-table-column
          prop="casePcFunction"
          label="函数">
        </u-table-column>
        <u-table-column
          prop="addTime"
          label="创建时间"
          sortable>
        </u-table-column>
        <u-table-column
          prop="modifyTime"
          label="修改时间"
          sortable>
        </u-table-column>
      </u-table>
      <div style="margin-top: 20px;float: left">
        <el-button @click="tgaSelected()">全选</el-button>
      </div>
      <div style="margin-top: 20px;float: right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
          :page-sizes=[10,20,30,50,100,500,1000,5000,10000,20000,30000]
          :page-size="pagesize"
          layout="total ,sizes, prev, pager, next,jumper"
          :total="total">
        </el-pagination>
      </div>
    </div>
    <div style="margin-top: 80px;margin-left: 275px;margin-right: 275px">
      <el-steps :active="stepActive" :finish-status="stepStatus">
        <el-step title="服务检测" description="启动自动化任务必备条件检查"/>
        <el-step title="提交测试任务" description="通过设置不同参数满足自动化多场景使用"/>
      </el-steps>
      <el-button type="primary" style="float:left;text-align:left;margin-top: 10px;margin-bottom: 50px;" @click="submitTestTask">开始测试</el-button>
      <el-dialog id="sdDete" :visible="dialogEnvDeteVisible" :custom-class="'sdDeteSye'" :before-close='closeEnvDialog' width="600px">
        <template slot="title">
          <div style="color: #FFFFFF">服务检测</div>
        </template>
        <el-form :label-position="labelPosition">
          <div v-if="submitProjectId==='1'">
            <el-form-item label="1. kcpBridge服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="kcpBridgeStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="kcpBridgeStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="kcpBridgeStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
            <el-form-item label="2. kcpCtl服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="kcpCtlStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="kcpCtlStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="kcpCtlStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
            <el-form-item label="3. allure服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="kcpAllureStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="kcpAllureStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="kcpAllureStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
          </div>
          <div v-if="submitProjectId==='2'">
            <el-form-item label="1. oneBridge服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="oneBridgeStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="oneBridgeStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="oneBridgeStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
            <el-form-item label="2. oneCtl服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="oneCtlStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="oneCtlStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="oneCtlStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
            <el-form-item label="3. allure服务状态" label-width=250px style="margin-left: 90px">
              <i v-if="oneAllureStatus==='false'" class="el-icon-error" style="color: #ec2755;"></i>
              <i v-if="oneAllureStatus==='deteing'" class="el-icon-loading" style="color: #ff4938;"></i>
              <i v-if="oneAllureStatus==='true'" class="el-icon-success" style="color: #5daf34;"></i>
            </el-form-item>
          </div>
        </el-form>
        <el-button @click="EnvDeteAgain" type="warning" style="margin-top: 10px;margin-right: 50px">重新检测</el-button>
        <el-button @click="startTestTask" :disabled=nextValue type="primary" style="margin-top: 10px">下一步</el-button>
        <br>
        <br>
      </el-dialog>
      <el-dialog id="submitTask" :visible.sync="dialogFormVisible" :custom-class="'submitTaskSye'" :before-close='closeSubmitTaskDialog' width=30%>
        <template slot="title">
          <div style="color: #FFFFFF">提交测试任务</div>
        </template>
        <el-form :model="form">
          <el-form-item label="任务名称:" label-width=80px>
            <el-input v-model="form.taskname" style="width:80%;position:absolute;left:0px;" autocomplete="off"></el-input>
          </el-form-item>
          <div>
            <el-form-item label="运行模式:" label-width=80px>
              <el-select style="position:absolute;left:0px;width: 150px" v-model="form.defaultModeValue" @change="selectItem">
                <el-option v-for="item in form.modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="info" plain style="position:absolute;right:0px;" @click="advanceSettings">高级选项</el-button>
            </el-form-item>
            <div v-if='advanceVisible'>
              <hr style="margin-top: 50px">
              <el-form-item label="重复执行" label-width=80px style="margin-top: 20px;">
                <el-form-item label="运行:" label-width=50px style="margin-top: 30px;">
                  <el-input type="number" v-model.number="form.num" min="1" style="width:20%;position:absolute;left:0px;" autocomplete="off"></el-input>
                  <label style="position:absolute;left:25%;">次</label>
                </el-form-item>
              </el-form-item>
              <el-form-item label="定时任务" label-width=80px style="margin-top: 20px;">
                <el-form-item label="时间:" label-width=50px style="margin-top: 30px;">
                  <el-time-picker v-model="settime" format="HH:mm" value-format="HH:mm" style="position:absolute;left:0px;width: 3cm" placeholder="请选择">
                  </el-time-picker>
                </el-form-item>
              </el-form-item>
            </div>
          </div>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="preStepTask">上一步</el-button>
          <el-button @click="cancelTask">取 消</el-button>
          <el-button type="primary" @click="saveAndSubmitTestTask">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import {
    testCasesKcpList,
    testCasesSearchKcpList,
    testCasesOneList,
    testCasesSearchOneList,
    projectsList,
    busModules,
    deteEnv,
    checkRunningTask,
    submitCasesList,
    saveTestTask,
    startRunTask
  } from "../apis/apis"
  import {Loading} from "element-ui"
  import NavMenu from "./navMenu"

  export default {
    components: {NavMenu},
    data() {
      // this.nodesChartExtend = {
      //   legend: {show: true},  //隐藏legend
      //   series: {
      //     center: ['50%', '50%']
      //   }
      // };
      // this.nodesRingColor = ["#43DCFF", "#C0EF84","#f5f259"];
      return {
        activeIndex:"1",
        stepActive:0,
        stepStatus:"",
        username: JSON.parse(sessionStorage.getItem('username')),
        currentPage: 1,
        pagesize: 10,
        total: 0,
        headers: {Authorization: 'Bearer ' + JSON.parse(sessionStorage.getItem('token'))},
        kcpToken: "",
        apps:["allure"],
        defaultProjectId: "0",
        projects: [],
        projectGroupId: 0,
        projectGroupProjectList:[],
        caseslist: [],
        checked: true,
        submited:false,
        timer:null,
        multipleSelection: [],
        labelPosition:'left',
        nextEnvValue:true,
        dialogEnvDeteVisible:false,
        kcpBridgeStatus:'deteing',
        kcpCtlStatus:'deteing',
        kcpAllureStatus:'deteing',
        oneBridgeStatus:'deteing',
        oneCtlStatus:'deteing',
        oneAllureStatus:'deteing',
        nextChangeValue:true,
        nextResourceValue:true,
        nextValue:true,
        dialogFormVisible: false,
        advanceVisible: false,
        settime: "",
        currentProject: "",
        currentProjectId: "",
        submitProjectId: "",
        submitCaseData: [],
        defaultTaskName: "",
        offset: 300,
        rescnrt: {
          code: 0
        },
        reqCasesList: {},
        resCasesList: {
          code: 0,
          runningTaskFlag: "",
          message: ""
        },
        reqSaveTask: {
          taskName: "",
          casesTotal:0,
          taskRunFlag: "",
          optUser: JSON.parse(sessionStorage.getItem('username')),
          projectGroup_id: 0,
          project_id: 0,
          runMode:"1",
          runPlatform:"1",
          runNum:1,
          repeatMode:"02",
          runTime:"",
          reRunFlag:"False"
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
          runPlatform:"1",
          runNum:0,
          repeatMode:"",
          runTime:"",
          reRunFlag:"False"
        },
        reqUpdateRunTask: {
          taskName: "",
          project_id: 0,
          runFlag: "",
          runMode:"0",
          runPlatform:"1",
          runNum:0,
          repeatMode:"",
          runTime:"",
          reRunFlag:"False"
        },
        resRunTask: {
          code: 0,
          msg: "",
          runningFlag: ""
        },
        tableModuleOptions:[],
        resourceExist: true,
        moduleKey:0,
        search: {
          moduleOptions:[],
          caseNo: "",
          title: "",
          typeOptions:[{
            value:"1",
            label:"冒烟测试"
          },
          {
            value:"['1','2']",
            label:"全部"
          }],
          levelOptions:[{
            value:"1",
            label:"高"
          },
          {
            value:"2",
            label:"中"
          },
          {
            value:"3",
            label:"低"
          }]
        },
        form:{
          taskname: "",
          // modeOptionsStatus:false,
          modeOptions:[{
            value:"1",
            label:"全部执行"
          },
          {
            value:"2",
            label:"失败即停止"
          }],
          RepeatValueOptions:[{
            value:"02",
            label:"逐一迭代"
          },
          {
            value:"01",
            label:"顺序迭代"
          }],
          defaultModeValue: "1",
          num: 1,
          defaultRepeatValue: "02"
        },
        projectGroupOptions: [],
        defaultProjectGroup: "更新中...",
      }
    },
    methods: {
      advanceSettings() {
        if (this.advanceVisible) {
          this.advanceVisible = false
        } else {
          this.advanceVisible = true
        }
      },
      closeEnvDialog() {
        this.stepActive = 0
        this.dialogEnvDeteVisible = false
      },
      closeSubmitTaskDialog() {
        this.stepActive = 0
        this.dialogFormVisible = false
      },
      EnvDeteAgain() {
          this.projectEnvDete()
      },
      preStepTask() {
        this.dialogFormVisible = false
        this.envDete()
      },
      cancelTask() {
        this.stepActive = 0
        this.dialogFormVisible = false
      },
      startTestTask() {
        this.stepStatus = ""
        this.dialogEnvDeteVisible = false
        this.dialogFormVisible = true
        let projectName = ""
        for (let pjs in (JSON.parse(sessionStorage.getItem("projects")))) {
          if (JSON.parse(sessionStorage.getItem("projects"))[pjs].project_id.toString() === sessionStorage.getItem("defaultProjectId")) {
            projectName = JSON.parse(sessionStorage.getItem("projects"))[pjs].project
          }
        }
        this.form.taskname = this.reqSaveTask.optUser + '_' + projectName + '_' + this.$moment().format('YYYY-MM-DD HH:mm:ss')
      },
      submitTestTask() {
        this.stepStatus = ""
        this.stepActive = 0
        if (this.multipleSelection.length === 0) {
          this.$message.error({
            type: "error",
            showClose: true,
            offset: this.offset,
            message: "请至少选择一条用例"
          })
        } else {
          sessionStorage.setItem("flag", "1")
          this.dialogEnvDeteVisible = true
          this.projectEnvDete()
        }
      },
      envDete() {
        this.stepStatus = ""
        this.dialogEnvDeteVisible = true
        if (this.submitProjectId === "1") {
          this.stepStatus = "success"
          this.stepActive = 1
          this.dialogDnsDeteVisible = false
        }
        this.stepActive = 0
        this.projectEnvDete()
      },
      async projectEnvDete() {
        let _this = this
        _this.kcpBridgeStatus = 'false'
        _this.kcpCtlStatus = 'false'
        _this.kcpAllureStatus = 'false'
        _this.oneBridgeStatus = 'false'
        _this.oneCtlStatus = 'false'
        _this.oneAllureStatus = 'false'
        this.nextValue = true
        let params = {
          'project': parseInt(this.submitProjectId)
        }
        await deteEnv(this.headers, params).then(res => {
          if (res.code === 2000 && (parseInt(this.submitProjectId) === 1)) {
            this.kcpBridgeStatus = 'true'
            this.kcpCtlStatus = res.kcpCtlStatus
            this.kcpAllureStatus = res.allureStatus
            if (this.kcpCtlStatus === 'true' && this.kcpAllureStatus === 'true') {
              this.nextValue = false
            } else {
              this.nextValue = true
            }
          } else if (res.code === 2000 && (parseInt(this.submitProjectId) === 2)) {
            this.oneBridgeStatus = 'true'
            this.oneCtlStatus = res.oneCtlStatus
            this.oneAllureStatus = res.allureStatus
            if (this.oneCtlStatus === 'true' && this.oneAllureStatus === 'true') {
              this.nextValue = false
            } else {
              this.nextValue = true
            }
          }
        }).catch(function (error) {
          _this.kcpBridgeStatus = 'false'
          _this.kcpCtlStatus = 'false'
          _this.kcpAllureStatus = 'false'
          _this.oneBridgeStatus = 'false'
          _this.oneCtlStatus = 'false'
          _this.oneAllureStatus = 'false'
        })
      },
      saveAndSubmitTestTask() {
        this.stepStatus = ""
        // if (this.form.num <= 0) {
        //   this.$message({
        //     type: "error",
        //     showClose: true,
        //     offset: this.offset,
        //     message: '请输入大于0的整数'
        //   })
        // }
        let isIntNum = /^\+?[1-9][0-9]*$/;
        if (this.form.taskname === "" || !isIntNum.test(this.form.num)) {
          if (this.form.taskname === "") {
            this.$message({
              type: "error",
              showClose: true,
              offset: this.offset,
              message: '任务名称不能为空'
            })
          }
          if (!isIntNum.test(this.form.num)) {
            this.$message({
              type: "error",
              showClose: true,
              offset: this.offset,
              message: '重复执行次数请输入大于0的整数'
            })
          }
        } else {
          let taskRunFlag = "unRun"
          let _this = this
          this.checkNotRunningTask(parseInt(this.submitProjectId)).then(res => {
            // console.log(this.rescnrt.code)
            if (this.rescnrt.code === 2000) {
              // console.log(this.stepStatus)
              this.$message({
                type: 'error',
                showClose: true,
                offset: this.offset,
                message: '当前有测试任务在进行，请稍后提交'
              })
            } else {
              // this.runCasesTest().then(res => {
              //   if (this.resCasesList.code === 2000) {
              this.saveRunTestTask(this.form.taskname, taskRunFlag, this.projectGroupId, parseInt(this.submitProjectId)).then(res => {
                if (this.resSaveTask.taskName === this.form.taskname) {
                  const options_runCases = {
                    text: '正在保存用例执行列表，请稍等...',
                    customClass: "login_loading",
                    spinner: "el-icon-loading",
                    lock: true,
                    background: 'rgba(0,0,0,0.5)'
                  }
                  this.loadingInstanceRunCases = Loading.service(options_runCases)
                  this.runCasesTest().then(res => {
                    if (this.resCasesList.code === 2000) {
                      this.loadingInstanceRunCases.close()
                      this.runTestTask(this.form.taskname, parseInt(this.submitProjectId), taskRunFlag).then(res => {
                        if (this.resRunTask.code === 2000) {
                          // this.$message({
                          //   type: 'success',
                          //   showClose: true,
                          //   duration: 5000,
                          //   offset: this.offset,
                          //   message: '测试任务【' + this.form.taskname + '】执行中...'
                          // })
                          this.stepStatus = "success"
                          const options_task = {
                            text: '测试任务【' + this.form.taskname + '】执行中，即将跳转到个人任务',
                            customClass: "login_loading",
                            spinner: "el-icon-success",
                            lock: true,
                            background: 'rgba(0,0,0,0.5)'
                          }
                          this.loadingInstanceTask = Loading.service(options_task)
                          sessionStorage.setItem("flag", "2")
                          setTimeout(() => {
                            this.dialogFormVisible = false
                            this.loadingInstanceTask.close()
                            this.$router.push({name: 'taskList'}) // 强制切换当前路由 path
                          }, 5000)
                        } else {
                          this.$message.error({
                            type: "error",
                            showClose: true,
                            offset: this.offset,
                            message: "当前有测试任务在进行，请稍后提交"
                          })
                        }
                      })
                    } else {
                      const options_runCases_fail = {
                        text: '保存用例执行列表失败，请联系管理员！',
                        customClass: "login_loading",
                        spinner: "el-icon-error",
                        lock: true,
                        background: 'rgba(0,0,0,0.5)'
                      }
                      this.loadingInstanceRunCasesFail = Loading.service(options_runCases_fail)
                      setTimeout(() => {
                        this.loadingInstanceRunCasesFail.close()
                      }, 3000)
                      // this.$message.error({
                      //   type: "error",
                      //   showClose: true,
                      //   offset: this.offset,
                      //   message: this.resCasesList.message
                      // })
                    }
                  }).catch(function (error) {
                  _this.$message.error({
                    type: "error",
                    showClose: true,
                    offset: _this.offset,
                    message: "请求超时或错误"
                  })
                  _this.loadingInstanceRunCases.close()
                })
                }
              }).catch(function (error) {
                _this.$message.error({
                  type: "error",
                  showClose: true,
                  offset: _this.offset,
                  message: "该测试任务已存在"
                })
              })
            }
          })
        }
      },
      selectItem(val) {
        this.reqSaveTask.runMode = val
        // console.log(this.reqSaveTask.runMode)
      },
      selectPlatformItem(val) {
        this.reqSaveTask.runPlatform = val
        // console.log(this.reqSaveTask.runMode)
      },
      selectRepeatItem(val) {
        this.reqSaveTask.repeatMode = val
      },
      standardTypeFormat(row, column) {
        if (row.standardType === "1") {
          return "标准"
        } else {
          return "非标"
        }
      },
      typeFormat(row, column) {
        if (row.caseType === "1") {
          return "冒烟测试"
        } else {
          return "回归测试"
        }
      },
      levelFormat(row, column) {
        if (row.caseLevel === "1") {
          return "高"
        } else if (row.caseLevel === "2") {
          return "中"
        } else if (row.caseLevel === "3") {
          return "低"
        }
      },
      moduleFormat(row,column) {
        for (let i = 0; i < this.tableModuleOptions.length; i++) {
          if (row.busmodule === this.tableModuleOptions[i].value) {
            return this.tableModuleOptions[i].label
          }
        }
      },
      handleSizeChange(val) {
        this.pagesize = val
        this.getCasesList(2, this.currentPage, this.pagesize)
      },
      handleCurrentChange(val) {
        this.currentPage = val
        this.getCasesList(2, this.currentPage, this.pagesize)
      },
      //获取项目列表
      async getProjectList() {
        // console.log(this.$store.state.user)
        // let headers = {Authorization: 'Bearer ' + JSON.parse(sessionStorage.getItem('token'))}
        let _this = this
        await projectsList(this.headers).then(res => {
          if (res.code === 2000) {
            this.projectGroupOptions = []
            this.projectGroupProjectList = res.data
            if (sessionStorage.getItem("defaultProjectGroup")) {
              this.defaultProjectGroup = sessionStorage.getItem("defaultProjectGroup")
            } else {
              this.defaultProjectGroup = res.data[0].projectGroup
            }
            if (sessionStorage.getItem("projectGroup")) {
              this.projectGroupId = sessionStorage.getItem("projectGroup")
            } else {
              this.projectGroupId = res.data[0].projectGroup_id
            }
            if (sessionStorage.getItem('projects')) {
              this.projects = JSON.parse(sessionStorage.getItem('projects'))
            } else {
              this.projects = res.data[0].data
            }
            // this.currentProject = this.projects[0].project
            if (sessionStorage.getItem('defaultProjectId')) {
              this.defaultProjectId = sessionStorage.getItem('defaultProjectId')
            } else {
              this.defaultProjectId = this.projects[0].project_id.toString()
            }
            for (let i = 0; i < res.data.length; i++) {
              let projectGroupData = {"value": res.data[i].projectGroup_id, "label": res.data[i].projectGroup}
              this.projectGroupOptions.push(projectGroupData)
            }
            sessionStorage.setItem('projectGroupProjectList', JSON.stringify(this.projectGroupProjectList))
            sessionStorage.setItem('projectGroupOptions', JSON.stringify(this.projectGroupOptions))
            sessionStorage.setItem('defaultProjectId', this.defaultProjectId)
            sessionStorage.setItem('projects', JSON.stringify(this.projects))
            sessionStorage.setItem('projectGroup', this.projectGroupId)
          } else {
            this.$message.error({
              type: "error",
              showClose: true,
              offset: this.offset,
              message: "获取项目列表失败"
            })
          }
        }).catch(function (error) {
          _this.$message.error({
            type: "error",
            showClose: true,
            offset: _this.offset,
            message: "获取项目列表超时，请稍后重试"
          })
        })
        this.getDefaultCasesList()
      },
      //默认获取第一个项目测试用例列表
      getDefaultCasesList() {
        this.tableModuleOptions = []
        this.search.moduleOptions = []

        let params = {
          'page': this.currentPage,
          'page_size': 100000,
          'projectGroup': sessionStorage.getItem("projectGroup"),
          'project': sessionStorage.getItem("defaultProjectId"),
          'status': '1'
        }
        const options = {
          text: "正在加载...",
          customClass: "login_loading",
          spinner: "el-icon-loading",
          lock: true,
          background: 'rgba(0,0,0,0)'
        }

        this.loadingDefaultCases = Loading.service(options)

        if (parseInt(params.project) > 0) {
          busModules(this.headers,params).then(res => {
            this.search.moduleOptions = res.results
            this.tableModuleOptions = this.search.moduleOptions
          })
        }

        if (sessionStorage.getItem("defaultProjectId") === "1" && parseInt(params.project) > 0) {
          testCasesKcpList(this.headers, params).then(res => {
            this.caseslist = res.results
            this.total = res.count
            this.currentPage = 1
            if (this.total <= 10) {
              this.pagesize = 10
            } else if (this.total > 10 && this.total <= 20) {
              this.pagesize = 20
            } else if (this.total > 20 && this.total <= 30) {
              this.pagesize = 30
            } else if (this.total > 30 && this.total <= 50) {
              this.pagesize = 50
            } else if (this.total > 50 && this.total <= 100) {
              this.pagesize = 100
            } else if (this.total > 100 && this.total <= 500) {
              this.pagesize = 500
            } else if (this.total > 500 && this.total <= 1000) {
              this.pagesize = 1000
            } else if (this.total > 1000 && this.total <= 5000) {
              this.pagesize = 5000
            } else if (this.total > 5000 && this.total <= 10000) {
              this.pagesize = 10000
            } else if (this.total > 10000 && this.total <= 20000) {
              this.pagesize = 20000
            } else {
              this.pagesize = 30000
            }
          })
        } else if (sessionStorage.getItem("defaultProjectId") === "2" && parseInt(params.project) > 0) {
          testCasesOneList(this.headers, params).then(res => {
            this.caseslist = res.results
            this.total = res.count
            this.currentPage = 1
            if (this.total <= 10) {
              this.pagesize = 10
            } else if (this.total > 10 && this.total <= 20) {
              this.pagesize = 20
            } else if (this.total > 20 && this.total <= 30) {
              this.pagesize = 30
            } else if (this.total > 30 && this.total <= 50) {
              this.pagesize = 50
            } else if (this.total > 50 && this.total <= 100) {
              this.pagesize = 100
            } else if (this.total > 100 && this.total <= 500) {
              this.pagesize = 500
            } else if (this.total > 500 && this.total <= 1000) {
              this.pagesize = 1000
            } else if (this.total > 1000 && this.total <= 5000) {
              this.pagesize = 5000
            } else if (this.total > 5000 && this.total <= 10000) {
              this.pagesize = 10000
            } else if (this.total > 10000 && this.total <= 20000) {
              this.pagesize = 20000
            } else {
              this.pagesize = 30000
            }
          })
        }
      this.loadingDefaultCases.close()
      },
      handlerChange(name) {
        // console.log(this.tableModuleOptions)
        // console.log(this.search.moduleOptions)
        this.tableModuleOptions = []
        this.search.moduleOptions = []
        if (name.name !== undefined) {
          sessionStorage.setItem("defaultProjectId", name.name)
        }
        this.currentProjectId = name.name
        this.moduleKey += 1
        this.getCasesList(1, 1, 100000)
      },
      tableRowClassName({row, rowIndex}) {
        if ((rowIndex % 2) === 0) {
          return 'success-row-case'
        } else {
          return 'warning-row-case'
        }
      },
      //获取测试用例列表
      getCasesList(flag, currentPage, pageSize) {
        // console.log(name.label)
        // sessionStorage.setItem("project",name.name)
        // console.log(name.name)
        // console.log(this.defaultProjectId)
        // console.log(this.currentProjectId)

        // console.log(this.tableModuleOptions)
        // console.log(this.search.moduleOptions)
        // this.tableModuleOptions = []
        // this.search.moduleOptions = []

        if (name.name === undefined) {
          this.submitProjectId = this.defaultProjectId
        } else {
          this.submitProjectId = this.currentProjectId
        }
        let params = {
          'page': currentPage,
          'page_size': pageSize,
          'projectGroup': sessionStorage.getItem("projectGroup"),
          'project': parseInt(this.submitProjectId),
          'status': '1'
        }

        const options = {
          text: "正在加载...",
          customClass: "login_loading",
          spinner: "el-icon-loading",
          lock: true,
          background: 'rgba(0,0,0,0)'
        }
        this.loadingCases = Loading.service(options)

        if (parseInt(params.project) > 0) {
          busModules(this.headers,params).then(res => {
            this.search.moduleOptions = res.results
            this.tableModuleOptions = this.search.moduleOptions
          })
        }

        if (sessionStorage.getItem("defaultProjectId") === "1" && parseInt(params.project) > 0) {
          testCasesKcpList(this.headers, params).then(res => {
            this.caseslist = res.results
            this.total = res.count
            let ttl = 0
            if (flag === 1) {
              ttl = res.count
              this.currentPage = 1
            } else {
              ttl = this.caseslist.length
              this.currentPage = currentPage
            }
            if (this.total <= 10) {
              this.pagesize = 10
            } else if (ttl > 10 && ttl <= 20) {
              this.pagesize = 20
            } else if (ttl > 20 && ttl <= 30) {
              this.pagesize = 30
            } else if (this.total > 30 && this.total <= 50) {
              this.pagesize = 50
            } else if (this.total > 50 && this.total <= 100) {
              this.pagesize = 100
            } else if (this.total > 100 && this.total <= 500) {
              this.pagesize = 500
            } else if (this.total > 500 && this.total <= 1000) {
              this.pagesize = 1000
            } else if (this.total > 1000 && this.total <= 5000) {
              this.pagesize = 5000
            } else if (this.total > 5000 && this.total <= 10000) {
              this.pagesize = 10000
            } else if (this.total > 10000 && this.total <= 20000) {
              this.pagesize = 20000
            } else {
              this.pagesize = 30000
            }
          })
        } else if (sessionStorage.getItem("defaultProjectId") === "2" && parseInt(params.project) > 0) {
          testCasesOneList(this.headers, params).then(res => {
            this.caseslist = res.results
            this.total = res.count
            let ttl = 0
            if (flag === 1) {
              ttl = res.count
              this.currentPage = 1
            } else {
              ttl = this.caseslist.length
              this.currentPage = currentPage
            }
            if (this.total <= 10) {
              this.pagesize = 10
            } else if (ttl > 10 && ttl <= 20) {
              this.pagesize = 20
            } else if (ttl > 20 && ttl <= 30) {
              this.pagesize = 30
            } else if (this.total > 30 && this.total <= 50) {
              this.pagesize = 50
            } else if (this.total > 50 && this.total <= 100) {
              this.pagesize = 100
            } else if (this.total > 100 && this.total <= 500) {
              this.pagesize = 500
            } else if (this.total > 500 && this.total <= 1000) {
              this.pagesize = 1000
            } else if (this.total > 1000 && this.total <= 5000) {
              this.pagesize = 5000
            } else if (this.total > 5000 && this.total <= 10000) {
              this.pagesize = 10000
            } else if (this.total > 10000 && this.total <= 20000) {
              this.pagesize = 20000
            } else {
              this.pagesize = 30000
            }
          })
        }
      this.$refs.multipleTable.reloadData(this.caseslist)
      this.loadingCases.close()
      },
      searchcases() {
        this.caseslist = []
        // console.log(this.search.title,this.search.type,this.search.level)
        if (name.name === undefined) {
          this.submitProjectId = this.defaultProjectId
        } else {
          this.submitProjectId = this.currentProject
        }
        const options = {
          text: "正在加载...",
          customClass: "login_loading",
          spinner: "el-icon-loading",
          lock: true,
          background: 'rgba(0,0,0,0)'
        }

        this.loadingSearchMulCases = Loading.service(options)

        let params = {
          "project_id": parseInt(this.submitProjectId),
          "busmodule": this.search.moduleOptions.value,
          "caseNo": this.search.caseNo.replace(/(^\s*)|(\s*$)/g, ""),
          "casename": this.search.title.replace(/(^\s*)|(\s*$)/g, ""),
          "caseType": this.search.typeOptions.value,
          "caseLevel": this.search.levelOptions.value,
          'status': '1'
          // "caseRunPlatform": this.search.PlatformOptions.value
        }
        if (params.caseType === undefined) {
          params["caseType"] = ['1','2']
        }

        if (params.caseLevel === undefined) {
          params["caseLevel"] = ['1','2','3']
        } else {
          if (params.caseLevel.length === 0) {
            params["caseLevel"] = ['1','2','3']
          }
        }

        if (params.busmodule === undefined) {
          params["busmodule"] = []
        } else {
          if (params.busmodule.length === 0) {
            params["busmodule"] = []
          }
        }

        if (sessionStorage.getItem("defaultProjectId") === "1") {
          testCasesSearchKcpList(this.headers, params).then(res => {
            let {data} = res
            this.caseslist = this.caseslist.concat(data)
            this.total = this.caseslist.length
          })
        } else if (sessionStorage.getItem("defaultProjectId") === "2") {
          testCasesSearchOneList(this.headers, params).then(res => {
            let {data} = res
            this.caseslist = this.caseslist.concat(data)
            this.total = this.caseslist.length
          })
        }

        this.currentPage = 1
        if (this.total <= 10) {
          this.pagesize = 10
        } else if (this.total > 10 && this.total <= 20) {
          this.pagesize = 20
        } else if (this.total > 20 && this.total <= 30) {
          this.pagesize = 30
        } else if (this.total > 30 && this.total <= 50) {
          this.pagesize = 50
        } else if (this.total > 50 && this.total <= 100) {
          this.pagesize = 100
        } else if (this.total > 100 && this.total <= 500) {
          this.pagesize = 500
        } else if (this.total > 500 && this.total <= 1000) {
          this.pagesize = 1000
        } else if (this.total > 1000 && this.total <= 5000) {
          this.pagesize = 5000
        } else if (this.total > 5000 && this.total <= 10000) {
          this.pagesize = 10000
        } else if (this.total > 10000 && this.total <= 20000) {
          this.pagesize = 20000
        } else {
          this.pagesize = 30000
        }
        this.loadingSearchMulCases.close()
      },
      //重置搜索条件
      reset() {
        this.search.moduleOptions.value = undefined
        this.search.caseNo = ""
        this.search.title = ""
        this.search.typeOptions.value = undefined
        this.search.levelOptions.value = undefined
      },
      //检测当前项目是否有测试任务
      async checkNotRunningTask(projectId) {
        let params = {"project": projectId}
        await checkRunningTask(this.headers, params).then(res => {
          let {code} = res
          this.rescnrt.code = code
        })
      },
      //提交要执行的测试用例
      async runCasesTest() {
        this.reqCasesList["taskId"] = this.resSaveTask.taskId
        await submitCasesList(this.headers, JSON.stringify(this.reqCasesList)).then(res => {
          let {code, runningTaskFlag, message} = res
          this.resCasesList.code = code
          this.resCasesList.runningTaskFlag = runningTaskFlag
          this.resCasesList.message = message
        })
      },
      //保存测试任务
      async saveRunTestTask(taskName, taskRunFlag, projectGroup_id, project_id) {
        this.reqSaveTask.taskName = taskName
        this.reqSaveTask.casesTotal = this.submitCaseData.length
        this.reqSaveTask.taskRunFlag = taskRunFlag
        this.reqSaveTask.projectGroup_id = projectGroup_id
        this.reqSaveTask.project_id = project_id
        this.reqSaveTask.runNum = this.form.num
        this.reqSaveTask.runTime = this.settime
        await saveTestTask(this.headers, this.reqSaveTask).then(res => {
          let {id, taskName, optUser, taskRunFlag} = res
          this.resSaveTask.taskId = id
          this.resSaveTask.taskName = taskName
          this.resSaveTask.optUser = optUser
          this.resSaveTask.taskRunFlag = taskRunFlag
        })
      },
      //启动测试任务
      async runTestTask(taskName, project_id, taskRunFlag) {
        this.reqRunTask.taskId = this.resSaveTask.taskId
        this.reqRunTask.taskName = taskName
        this.reqRunTask.project_id = project_id
        this.reqRunTask.runFlag = taskRunFlag
        this.reqRunTask.runMode = this.reqSaveTask.runMode
        this.reqRunTask.runPlatform = this.reqSaveTask.runPlatform
        this.reqRunTask.runNum = this.form.num
        this.reqRunTask.repeatMode = this.reqSaveTask.repeatMode
        this.reqRunTask.runTime = this.settime
        // console.log(this.reqRunTask)
        await startRunTask(this.headers, this.reqRunTask).then(res => {
          let {code, msg, runningFlag} = res
          this.resRunTask.code = code
          this.resRunTask.msg = msg
          this.resRunTask.runningFlag = runningFlag
        })
      },
      //当前页全选
      tgaSelected() {
        this.$refs.multipleTable.toggleAllSelection()
      },
      selectionChange(slt) {
        this.multipleSelection = slt
        this.submitCaseData = []
        if (name.name === undefined) {
          this.submitProjectId = this.defaultProjectId
        } else {
          this.submitProjectId = this.currentProject
        }
        sessionStorage.setItem("projectId",this.submitProjectId)
        // console.log(this.multipleSelection)
        for (let ms in this.multipleSelection) {
          this.submitCaseData.push({
            "id": this.multipleSelection[ms].id,
            "busmodule":this.multipleSelection[ms].busmodule,
            "caseNo":this.multipleSelection[ms].caseNo,
            "casename": this.multipleSelection[ms].casename,
            "caseType": this.multipleSelection[ms].caseType,
            "caseLevel": this.multipleSelection[ms].caseLevel,
            "caseFile": this.multipleSelection[ms].caseFile,
            "caseModule": this.multipleSelection[ms].caseModule,
            "casePcFunction": this.multipleSelection[ms].casePcFunction,
            "caseMobileFunction": this.multipleSelection[ms].caseMobileFunction,
            // "caseRunPlatform":this.multipleSelection[ms].caseRunPlatform
          })
        }
        this.reqCasesList = {
          "runType": "1",
          "projectGroup": this.projectGroupId,
          "project": parseInt(this.submitProjectId),
          "taskId":0,
          "data": this.submitCaseData
        }
      }
    },
    mounted() {
      this.getProjectList()
      this.$refs.NavMenu.changeProjectGroup()
    }
  }
</script>

<style>
  .el-table .warning-row-case {
    background: #fdf5e6;
  }

  .el-table .success-row-case {
    background: #f0f9eb;
  }

  #sdDete {
    top: 5%;
  }

  #sdDete .sdDeteSye {
    border-radius: 10px;
  }

  #sdDete .el-dialog__header {
    background-color: rgba(17, 9, 5, 0.90);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #submitTask {
    top: 10%;
  }

  #submitTask .submitTaskSye {
    border-radius: 10px;
  }

  #submitTask .el-dialog__header {
    background-color: rgba(17, 9, 5, 0.90);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  .el-form-item label:after {
    content: "";
    display: inline-block;
    /*width: 30%;*/
  }

  .el-form-item__label {
    text-align: justify;
    /*height: 30px;*/
  }

  .el-form-item.is-required .el-form-item__label:before {
    content: none !important;
  }
</style>
