
const form = document.getElementById('genImage')
form.onsubmit = form_submit

function form_submit(event){
    event.preventDefault()
    let button = document.getElementById('genImageButton')
    button.innerText = 'начал генерацию...'
    // отправка формы
    form.submit()
}

