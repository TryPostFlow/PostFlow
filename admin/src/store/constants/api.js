import Axios from 'axios'

let axios

if (process.env.NODE_ENV === 'production') {
  axios = Axios.create({
    baseURL: '/api',
  })
}else{
  axios = Axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
  })
}

if (localStorage.getItem('auth')) {
  var auth = JSON.parse(localStorage.getItem('auth'))
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + auth.access_token
}

export default axios