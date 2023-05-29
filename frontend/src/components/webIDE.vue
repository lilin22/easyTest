<template>
  <div>
    <nav-menu :activeIndex="activeIndex" :username="username" ref="NavMenu" :projectGroupOptions="projectGroupOptions"></nav-menu>
    <div v-if="username == '李淋'" class="editor-box">
      <ace
          ref="editor"
          :value="content"
          @init="initEditor"
          :lang="lang"
          :height="height === 0 ? '100%' : height"
          width="100%"
          :theme="theme"
          :options="options"
          v-bind="config">
      </ace>
    </div>
  </div>
</template>

<script>
  import NavMenu from "./navMenu"
  import ace from 'vue2-ace-editor'
  export default {
    name: "webIDE",
    components:{
      ace,NavMenu
    },
    data() {
      return {
        activeIndex:"4",
        username: JSON.parse(sessionStorage.getItem('username')),
        projectGroupOptions: [],
      }
    },
    props: {
      content: {
          type: String,
          default: ''
      },
      height: {
          type: Number,
          default: 1000
      },
      readOnly: {
          type: Boolean,
          default: false
      },
      theme: {
          type: String,
          default: 'monokai'
      },
      lang: {
          type: String,
          default: 'python'
      },
      config: {
        type: Object,
        default: () => {
            return {
                font_size: 16,
                py_atom: true
            }
        }
      }
    },
    computed: {
      options () {
        if (this.readOnly) {
          return {
              enableBasicAutocompletion: true,
              enableSnippets: true,
              enableLiveAutocompletion: this.config.py_atom,
              showPrintMargin: false,
              fontSize: this.config.font_size,
              readOnly: true
          }
        }
        return {
          enableBasicAutocompletion: true,
          enableSnippets: true,
          enableLiveAutocompletion: this.config.py_atom,
          showPrintMargin: false,
          fontSize: this.config.font_size
        }
      }
    },
    created () {
    },
    methods: {
      initEditor (editor) {
        require('brace/ext/language_tools')
        // 设置语言
        require('brace/mode/python')
        require('brace/snippets/python')
        // 设置主题 按需加载
        require('brace/theme/monokai')
        require('brace/theme/chrome')
        require('brace/theme/crimson_editor')
        // 监听值的变化
        editor.getSession().on('change', val => {
            this.$emit('change', editor.getValue())
        })
      }
    }
  }
</script>

<style scoped>

</style>
