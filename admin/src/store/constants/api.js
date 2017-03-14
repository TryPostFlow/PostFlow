import Axios from 'axios'

const axios = Axios.create({
    baseURL: apiBaseURL
  })

if (localStorage.getItem('auth')) {
  var auth = JSON.parse(localStorage.getItem('auth'))
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + auth.access_token
}

export default axios