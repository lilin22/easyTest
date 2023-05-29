import axios from 'axios';
// export const baseurl= 'http://127.0.0.1:8000'
//export const baseurl= window.location.origin;
export const baseurl = 'http://172.16.23.62:8000'
export const kcpbaseurl = 'http://172.16.23.63:18080'
export const onebaseurl = 'http://172.16.23.61:18080'

// const request = axios.create({})
const request = axios.create({
  // baseURL: '',
  // headers: {
  //   'Content-Type': 'application/json'
  // },
  timeout: 3000
});

const retry = 2
const retryDelay = 1000

request.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// request.interceptors.request.use(function (response) {
//     // 对响应数据做点什么
//     return response;
//   }, function (error) {
//     // 对响应错误做点什么
//     return Promise.reject(error);
//   })

request.interceptors.response.use(undefined, function axiosRetryInterceptor (error) {
  // return Promise.reject(error)
  let config = error.config
  // console.log(config)
  // If config does not exist or the retry option is not set, reject
  if (!config || !config.retry) {
    console.log("未配置config")
    return Promise.reject(error)
  }

  // Set the variable for keeping track of the retry count
  config.__retryCount = config.__retryCount || 0

  // Check if we've maxed out the total number of retries
  if (config.__retryCount >= config.retry) {
    // Reject with the error
    return Promise.reject(error)
  }

  // Increase the retry count
  config.__retryCount += 1

  // Create new promise to handle exponential backoff
  let backoff = new Promise(function (resolve) {
    setTimeout(function () {
      resolve()
    }, config.retryDelay || 1)
  })

  // Return the promise in which recalls axios to retry the request
  return backoff.then(function () {
    return request(config)
  })
})

//用户登录
export const login = params => {
  return request.post(`${baseurl}/api/token`,params,{ retry: retry, retryDelay: retryDelay }).then(res => res.data);
};
//修改密码
export const modifyPassword = (headers,params) => {
  return request.post(`${baseurl}/user/modifyPassword`,params,{headers: headers,retry: retry, retryDelay: retryDelay }).then(res => res.data);
};
//用户登录
export const loginKcp = params => {
  return request.post(`${kcpbaseurl}/kcp/login`,params,{ retry: retry, retryDelay: retryDelay }).then(res => res.data);
};

//用户登录
export const loginOne = params => {
  return request.post(`${onebaseurl}/one/login`,params,{ retry: retry, retryDelay: retryDelay }).then(res => res.data);
};

//获取用户项目列表
export const projectsList = (headers) => {
  return request.get(`${baseurl}/projectManage/getProjects`, {headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//获取项目的业务模块
export const busModules = (headers,params) => {
  return request.get(`${baseurl}/projectManage/busModules`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//获取用户kcp项目组的测试用例列表
export const testCasesKcpList = (headers,params) => {
  return request.get(`${baseurl}/testCases/testCasesKcpList`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//搜索kcp测试用例列表
export const testCasesSearchKcpList = (headers,params) => {
  return request.post(`${baseurl}/testCases/testCasesSearchKcpList`,params,{headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//获取用户one项目组的测试用例列表
export const testCasesOneList = (headers,params) => {
  return request.get(`${baseurl}/testCases/testCasesOneList`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//搜索one测试用例列表
export const testCasesSearchOneList = (headers,params) => {
  return request.post(`${baseurl}/testCases/testCasesSearchOneList`,params,{headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//环境检测
export const deteEnv = (headers,params) => {
  return request.get(`${baseurl}/projectManage/appsDete`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//查询当前项目是否有测试任务
export const checkRunningTask = (headers,params) => {
  return request.get(`${baseurl}/testTask/testRunStart`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//提交测试用例执行列表
export const submitCasesList = (headers,params) => {
  return request.post(`${baseurl}/testCases/testCasesRunList`,params,{headers: headers, timeout: 600000}).then(res => res.data);
};
//保存测试任务
export const saveTestTask = (headers,params) => {
  return request.post(`${baseurl}/testTask/taskHistoryList/`,params,{headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//更新测试任务
export const updateTestTask = (id,headers,params) => {
  return request.put(`${baseurl}/testTask/taskHistoryList/${id}/`,params,{headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//启动测试任务
export const startRunTask = (headers,params) => {
  return request.post(`${baseurl}/testTask/testRunStart`,params,{headers: headers,retry: retry, retryDelay: retryDelay, timeout: 10000}).then(res => res.data);
};
//获取个人任务列表
export const testtasksList = (headers,params) => {
  return request.get(`${baseurl}/testTask/taskHistoryList/`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
//kcp查询个人任务状态
export const queryKcpPersonTask = (headers,params) => {
  return request.post(`${kcpbaseurl}/kcp/queryPersonTask`,{params: params, headers: headers},{timeout: 5000}).then(res => res.data);
};
//kcp查询个人任务进度
export const queryKcpProcessTask = (params) => {
  return request.get(`${kcpbaseurl}/kcp/taskProcess`,{params: params},{timeout: 5000}).then(res => res.data);
}
//kcp撤销任务
export const destroyKcpTask = (headers,params) => {
  return request.post(`${kcpbaseurl}/kcp/destroyTask`,{params: params, headers: headers},{timeout: 100000}).then(res => res.data);
};
//one查询个人任务状态
export const queryOnePersonTask = (headers,params) => {
  return request.post(`${onebaseurl}/one/queryPersonTask`,{params: params, headers: headers},{timeout: 5000}).then(res => res.data);
};
//one查询个人任务进度
export const queryOneProcessTask = (params) => {
  return request.get(`${onebaseurl}/one/taskProcess`,{params: params},{timeout: 5000}).then(res => res.data);
}
//one撤销任务
export const destroyOneTask = (headers,params) => {
  return request.post(`${onebaseurl}/one/destroyTask`,{params: params, headers: headers},{timeout: 100000}).then(res => res.data);
};
//获取最近次数任务列表
export const lastTasks = (headers,params) => {
  return request.get(`${baseurl}/testTask/taskHistoryList/`,{params: params, headers: headers,retry: retry, retryDelay: retryDelay}).then(res => res.data);
};
