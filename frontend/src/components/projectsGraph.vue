<template>
  <div>
    <nav-menu :activeIndex="activeIndex" :username="username" ref="NavMenu" :projectGroupOptions="projectGroupOptions"></nav-menu>
    <div v-if="authUsers.indexOf(username) !== -1" style="margin-top:50px;margin-left:15px;margin-right:15px">
      <el-form label-width="100px">
        <el-row>
          <el-col :span="6">
              <el-form-item>
                <label>项目：</label>
                <el-select v-model="defProject" style="width: 150px" @change="selectProject" placeholder="请选择">
                  <el-option
                    v-for="item in projects"
                    :key="item.project_id"
                    :label="item.project"
                    :value="item.project_id">
                  </el-option>
                </el-select>
              </el-form-item>
          </el-col>
          <el-col :span="6">
              <el-form-item>
                <label>最近任务次数：</label>
                <el-select v-model="taskNum" style="width: 80px" @change="selectTaskNum" placeholder="请选择">
                  <el-option
                    v-for="item in taskNumOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-button type="warning" @click="submitGraph">确定</el-button>
          </el-col>
        </el-row>
      </el-form>
      <div id="myChart" :style="{width: '1750px', height: '600px'}"></div>
    </div>
    <div v-if="authUsers.indexOf(username) === -1" style="margin-top:5%;margin-left:30%;">
<!--      <div class="qhimgs" style="float:left;"><img src="../assets/qhimgs.jpg" alt="qhimgs"></div>-->
      <div style="float:left;margin-top:25%;">
        <h3 style="color: #4f91cb;font-size: 20px">Sorry，</h3>
        <p style="color: #8ebce5;font-size: 16px">你没有权限访问该页面......</p>
      </div>

<!--      <div style="float:left;background:#f00;">div1</div>-->
<!--      <div style="float:left;background:#0f0;margin-left:10px;">div2</div>-->
    </div>
  </div>
</template>

<script>
  import NavMenu from "./navMenu"

  import {lastTasks} from "../apis/apis"

  // 引入基本模板
  let echarts = require('echarts/lib/echarts')
  // 引入柱状图组件
  require('echarts/lib/chart/bar')
  // 引入提示框和title组件
  require('echarts/lib/component/tooltip')
  require('echarts/lib/component/title')
  require('echarts/lib/chart/line')
  require('echarts/lib/component/legend')

  export default {
    name: "graph",
    components: {NavMenu},
    data() {
      return {
        activeIndex: "4",
        headers: {Authorization: 'Bearer ' + JSON.parse(sessionStorage.getItem('token'))},
        projectGroupOptions: JSON.parse(sessionStorage.getItem('projectGroupOptions')),
        username: JSON.parse(sessionStorage.getItem('username')),
        projectGroupProjectList:JSON.parse(sessionStorage.getItem('projectGroupProjectList')),
        projects:JSON.parse(sessionStorage.getItem('projects')),
        // authUsers: ["李淋"],
        authUsers: ["李淋","张佳达","余锃","胡原","黄俊豪","李风霆"],
        taskNumOptions:[{
          value:"10",
          label:"10"
        },
        {
          value:"20",
          label:"20"
        },
        {
          value:"50",
          label:"50"
        }],
        defProject:JSON.parse(sessionStorage.getItem('projects'))[0].project_id,
        taskNum: "10",
        project_id: JSON.parse(sessionStorage.getItem('projects'))[0].project_id,
        realityTaskNum: 0,
        xdata: [],
        ydata: []
      }
    },
    methods: {
      drawLine () {
        // 基于准备好的dom，初始化echarts实例
        let myChart = echarts.init(document.getElementById('myChart'));
        // 绘制图表
        myChart.setOption({
          title: {
            text: '',
            subtext: ''
          },
          tooltip: {
            trigger: 'axis',
            show: true,
            // formatter: '{b0}<br/>{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%<br />{a3}: {c3}%<br />{a4}: {c4}%'
            formatter: '{b0}<br/>{a0}: {c0}%'
          },
          grid: {
            bottom: '20%'
          },
          legend: {
            // data:['最高','最低']
            data:['通过率']
          },
          toolbox: {
            show: true,
            feature: {
              dataZoom: {
                  yAxisIndex: 'none'
              },
              dataView: {readOnly: false},
              magicType: {type: ['line', 'bar']},
              restore: {},
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'category',
            // name: '日期',
            boundaryGap: false,
            axisLabel: {
              interval: 0,
              rotate: 40
            },
            // data: ['2019-02-25','2019-03-04','2019-03-18','2019-03-26','2019-04-16','2019-04-26','2019-05-04']
            data: Object.values(this.xdata)
          },
          yAxis: {
            type: 'value',
            // name: '通过率',
            axisLabel: {
              formatter: '{value}%'
            }
          },
          series: [
            {
              itemStyle : {normal : {color:'#051a2f', //改变折线点的颜色
								lineStyle:{color:'#051a2f'} //改变折线颜色
								},
							},
              name:'通过率',
              type:'line',
              // data:[1, 1, 0.2, 0.6, 1, 0.5, 1],
              // data:['100%', '100%', '20%', '60%', '100%', '50%', '100%'],
              // data:[100, 100, 20, 60, 100, 50, 100],
              data: Object.values(this.ydata),
              markPoint: {
                data: [
                  {type: 'max', name: '最大值'},
                  {type: 'min', name: '最小值'}
                ]
              },
              markLine: {
                data: [
                  {type: 'average', name: '平均值',formatter: '{average}%'}
                ]
              }
          },
            // {
            //   name:'最低',
            //   type:'line',
            //   data:[11, 11, 15, 13, 12, 13, 10],
            //   markPoint: {
            //     data: [
            //         {name: '周最低', value: 2, xAxis: 1, yAxis: 1.5}
            //     ]
            //   },
            //     markLine: {
            //       data: [
            //         {type: 'average', name: '平均值'},
            //           [{
            //             symbol: 'none',
            //             x: '90%',
            //             yAxis: 'max'
            //           }, {
            //             symbol: 'circle',
            //             label: {
            //                 normal: {
            //                     position: 'start',
            //                     formatter: '最大值'
            //                 }
            //             },
            //             type: 'max',
            //             name: '最高点'
            //           }]
            //       ]
            //     }
            // }
          ]
        });
      },
      selectProject (val) {
        this.project_id = val
      },
      selectTaskNum (val) {
        this.taskNum = val
      },
      async submitGraph () {
        this.xdata = []
        this.ydata = []
        let params = {
          "page":1,
          "page_size":this.taskNum,
          "projectGroup_id": sessionStorage.getItem('projectGroup'),
          "project_id": this.project_id,
          "taskRunFlag": "False",
          "ordering": "-createTime"}
        await lastTasks(this.headers,params).then(res => {
          if (res.results.length < this.taskNum) {
            this.realityTaskNum = res.results.length
          } else {
            this.realityTaskNum = this.taskNum
          }

          let i = 1
          for (let index in res.results) {
            let idx = this.realityTaskNum - i
            if (res.results[idx].createTime !== null && res.results[idx].ratio !== null) {
              this.xdata.push(res.results[idx].createTime)
              this.ydata.push(parseFloat(res.results[idx].ratio.replace("%","")))
              i += 1
            } else {
              i += 1
            }
          }
        })
        // console.log(Object.values(this.xdata))
        // console.log(Object.values(this.ydata))
        //调用drawLineChart()
        this.drawLine()
      },
    },
    watch: {
        projects (newVal,oldVal) {
          this.defProject = JSON.parse(sessionStorage.getItem('projects'))[0].project_id
          this.project_id = JSON.parse(sessionStorage.getItem('projects'))[0].project_id
          this.submitGraph()
        }
      },
    mounted () {
      this.submitGraph()
      //调用drawLineChart()
      // this.drawLine()
    }
  }
</script>

<style scoped>

</style>
