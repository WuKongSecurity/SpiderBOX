const form = document.querySelector('form')
const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

const successMessage = document.querySelector('.success-message')
const errorMessage = document.querySelector('.error-message')

form.addEventListener('submit', (_e) => {
  _e.preventDefault()

  const dt = {
    username: _e.target[0].value,
    email: _e.target[1].value,
    telephone: _e.target[2].value,
    wechat: _e.target[3].value,
    qq: _e.target[4].value,
    comments: _e.target[5].value
  }
  axios.post('https://api.wukongsec.com/contact', dt).then(res => {
    successMessage.classList.add('active')
    errorMessage.classList.remove('active')
    form.reset()
  }).catch(err => {
    console.error(err)
  })
})
