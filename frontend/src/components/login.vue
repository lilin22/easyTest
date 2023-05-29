<template>
  <div class="container">
    <div class="homeBox">
      <ul class="tyg-div">
        <li>让</li>
        <li><div style="margin-left:20px;">测</div></li>
        <li><div style="margin-left:40px;">试</div></li>
        <li><div style="margin-left:60px;">变</div></li>
        <li><div style="margin-left:80px;">得</div></li>
        <li><div style="margin-left:100px;">简</div></li>
        <li><div style="margin-left:120px;">单</div></li>
      </ul>
      <div style="width:32%;height: auto;margin-left: 30%">
        <div class="title0">soEasy自动化测试平台</div>
        <div class="title1">项目管理、人员管理、权限管理、用例管理、任务管理、测试报告、任务设置</div>
        <div class="lun-container">
            <div class="carouse" id="carouse">
                <div class="pic1"><img src="../assets/page1_0.png" alt="pic1"></div>
                <div class="pic2"><img src="../assets/page1_1.png" alt="pic2"></div>
                <div class="pic3"><img src="../assets/page1_2.png" alt="pic3"></div>
            </div>
        </div>
        <img class="img-login" src="../assets/page1_3.jpg"/>
      </div>
    </div>
    <el-form :model="user" ref="user" label-position="left" label-width="0px" class="login-page" :rules="rules" >
      <h2 class="title">系统登录</h2>
      <el-form-item prop="username">
        <el-input v-model.trim="user.username" id="username" name="username" ref="focusInput" auto-complete="off" placeholder="请输入用户名">
<!--          <el-button slot="prepend" icon="el-icon-user"></el-button>-->
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model.trim="user.password" id="password" name="password" type="password" auto-complete="off" placeholder="请输入密码">
<!--          <el-button slot="prepend" icon="el-icon-key"></el-button>-->
        </el-input>
      </el-form-item>
      <el-button type="primary" icon="el-icon-user-solid" id="submit" @click="login">登 录</el-button>
    </el-form>
  </div>
</template>
<script>
  import { login } from '../apis/apis'

  export default {
    data() {
      return {
        offset:300,
        user: {
          username: "",
          password: ""
        },
        rules: {
          username: [{ require: true,message: "请输入用户名",trigger: "blur"}],
          password: [{ require: true,message: "请输入密码",trigger: "blur"}]
        }
      }
    },
    methods: {
      inputFocus() {
        this.$nextTick(function () {
          this.$refs.focusInput.$el.querySelector('input').focus()
        })
      },
      carouselPicture() {
        this.ab(1)
      },
      ab(num){
        var carouse = document.getElementsByClassName("carouse");
        carouse.item(0).id = 'carouse'+num;
      },
      login() {
        let _this = this
        let user = {
          "username":this.user.username,
          "password":this.user.password
        }

      //   this.$refs.user.validate(valid => {
      //     if (valid) {
      //       console.log(valid)
      //   }
      // })

        if (!user.username) {
          _this.$message.error({
                        type:"error",
                        showClose: true,
                        offset:_this.offset,
                        message:"用户名不能为空"
                        })
            return;
          }
          if (!user.password) {
            _this.$message.error({
                        type:"error",
                        showClose: true,
                        offset:_this.offset,
                        message:"密码不能为空"
                        })
            return;
          }

        login(user).then(res => {
          let { access,refresh } = res
          // console.log(access,refresh)
          sessionStorage.setItem('username',JSON.stringify(user.username));
          // this.$store.commit({
          //   type:"setUsername",
          //   username:sessionStorage.getItem('username')
          // })
          // console.log(this.$store.state.username)
          sessionStorage.setItem('token',JSON.stringify(access))
          this.$router.push({name: 'casesList'})
        }).catch(function (error) {
          _this.$message.error({
            type:"error",
            showClose: true,
            offset:_this.offset,
            message:"用户名或者密码错误"
          })
        })
      }
    },
    mounted() {
      this.inputFocus()
      this.carouselPicture()
    }
  }
</script>
<style scoped>
.homeBox {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0px;
  background-color: #191c2c;
}
.carouse .pic1{
  transform: rotateY(0deg) translateZ(160px);
}
.carouse .pic2{
  transform: rotateY(120deg) translateZ(160px);
}
.carouse .pic3{
  transform: rotateY(240deg) translateZ(160px);
}
.img-login {
  margin-top: -35%;
  width: 100%;
  height: auto;
}
.tyg-div {
  color: #2ec0f6;
  z-index: -1000;
  float: left;
  position: absolute;
  left: 5%;
  top: 20%;
  font-size: 30px;
  list-style-type:none
}
.lun-container{
  width: 210px;
  height:140px;
  position: relative;
  font-size: 32px;
  color: #FFFFFF;
  text-align: center;
  line-height: 90px;
  margin: 200px auto;
  margin-bottom: 0px;
  margin-top:48%;
  perspective: 1000px;
  z-index: 1000;
}
.carouse{
  transform-style:preserve-3d;
}
.carouse div{
  display: block;
  position: absolute;
  width: 140px;
  height: 90px;
}

.carouse .pic1{
  transform: rotateY(0deg) translateZ(160px);
}
.carouse .pic2{
  transform: rotateY(120deg) translateZ(160px);
}
.carouse .pic3{
  transform: rotateY(240deg) translateZ(160px);
}
/*=== 下一个动画 ===*/
@keyframes to-scroll1 {
  0%{
    transform: rotateY(0deg);
  }

  33%{
    transform: rotateY(-120deg);
  }
  66%{
    transform: rotateY(-240deg);
  }
  100%{
    transform: rotateY(-360deg);
  }
}
#carouse1{
    animation: to-scroll1  10s ease infinite;
    /*animation-fill-mode: both;*/
}
.login-page {
  /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
  position: absolute;
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-clip: padding-box;
  /*margin: 180px auto;*/
  /*margin-top: 10%;*/
  /*right: 50px;*/
  width: 300px;
  padding: 35px 35px 15px 35px;
  background: #23305a;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
  z-index: 1000;
  float: right;
  right: 4%;
  top: 25%;
}
.title {
  margin: 0px auto 40px auto;
  text-align: center;
  color: #2ec0f6;
}
.title0 {
  position: absolute;
  top: 10%;
  left: -41px;
  width: 100%;
  text-align: center;
  color: #2ec0f6;
  font-size: 40px;
  height: 70px;
  line-height: 70px;
  /*<!--margin: -300px 0 0 0;-->*/
  z-index: 1000;
}
.title1 {
  position: absolute;
  top: 16%;
  left: -41px;
  width: 100%;
  text-align: center;
  color: #eaeaea;
  font-size: 20px;
  height: 70px;
  line-height: 70px;
  /*<!--margin: -300px 0 0 0;-->*/
  z-index: 1000;
  margin-top: 25px;
}
</style>
