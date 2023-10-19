let item_list = document.querySelectorAll('.input-area__item')
let view_list = document.querySelectorAll('.input-area__item .item__pc')
let input_area = document.querySelector('.input-area')
let item_checkboxs = NaN
let btn_uncheck = document.querySelector('.btn_uncheck')
let btn_start = document.querySelector('.btn_start')
let btn_calendar = document.querySelector('.btn_calendar')
let count_input = document.querySelector('#count')

// let date_from = document.querySelector('#Date_start')
// let date_to = document.querySelector('#Date_end')

_clss = {
    active : '_active'
}

// const getDiapsTime = () => {
//     date_from_val = date_from.value
//     date_to_val = date_to.value
//     console.log(date_from_val)
//     console.log(date_to_val)
//     return[date_from_val, date_to_val]
// }

// const setDiapsTime = () => {
//     getDiapsTime()
//     let currentDate = new Date();
//     let currentYear = currentDate.getFullYear() 
//     date_from.value =  `${currentYear-1}-08-01`
//     date_to.value =  `${currentYear}-07-31`
// }
// setDiapsTime()

const toggleItem = (e) => {
    element = e.target
    element_parrent = element.parentElement.parentElement
    if(element_parrent.classList.contains(_clss.active)) {
        element_parrent.classList.remove(_clss.active)
        element.innerText = '+'
    } else {
        element_parrent.classList.add(_clss.active)
        element.innerText = '-'
    }
}

const uncheck_inputs = (items) => {
    getDiapsTime()
    items.forEach(item =>{
        item.checked = false
    })
}

const toggle_disabled_btn = (act) => {
    btn_uncheck.disabled = act
    btn_start.disabled = act
    btn_calendar.disabled = act
}

const program_start = (items, act = false) =>{
    check_list = []
    items.forEach(item =>{
        leg_data = {

        }
        if (item.checked == true) {
            leg_data['country'] = item.dataset.country;
            leg_data['ligue'] = item.dataset.leg;
            leg_data['season'] = item.dataset.ses;
            leg_data['href'] = item.dataset.link;
            check_list.push(leg_data)
        }
    })
    toggle_disabled_btn(true)
    count_val = count_input.value
    eel.start(check_list, act, count_val)().then(e=>{toggle_disabled_btn(false)})
}

btn_uncheck.addEventListener('click', e =>{
    e.preventDefault()
    uncheck_inputs(item_checkboxs)
})

btn_start.addEventListener('click', e=>{
    e.preventDefault()
    program_start(item_checkboxs)
})

btn_calendar.addEventListener('click', e=>{
    e.preventDefault()
    program_start(item_checkboxs, true)
})

const lesten_items = () => {
    view_list = document.querySelectorAll('.input-area__item .item__pc')
    view_list.forEach(view_item => {
        view_item.addEventListener('click', toggleItem)
    })
    item_checkboxs = document.querySelectorAll('input[type="checkbox"]')
    console.log(item_checkboxs)
}

const generete_items = () =>{
    eel.get_seasons_data()().then(e=>{
        console.log(typeof e)
        result_html = ''
        for (const [item_key, item_value] of Object.entries(e)) {
            let item_key_refact = item_key.replace(' ', "_")
            item = e[item_key]
            let leg_el_html = ''
            for (const [leg_item_key, leg_item_value] of Object.entries(item_value)) {
                let leg_item_key_refact = item_key_refact + "_" + leg_item_key.replace(' ', "_")
                let ses_el_html = ''
                
                leg_item_value['seasons'].forEach(ses_item_value => {
                    ses_item_key = ses_item_value['name']
                    let ses_item_key_refact = item_key_refact + "_" + leg_item_key_refact + "_" + ses_item_key.replace(' ', "_")
                    ses_el_html += `
                        <div class="input-area__item">
                            <div class="item__area"><input class="subitem_input" data-ses="${ses_item_key}" data-leg=${leg_item_key} data-country=${item_key} data-link="${ses_item_value['href']}" type="checkbox" name="${ses_item_key_refact}" id="${ses_item_key_refact}"><label for="${ses_item_key_refact}">${ses_item_key}</label></div>
                        </div>
                    `
                });
                leg_el_html += `
                    <div class="input-area__item">
                        <div class="item__area"><span class="item__pc">+</span><label id="${leg_item_key_refact}">${leg_item_key}</label></div>
                        <div class="item__popup">
                            ${ses_el_html}
                        </div>
                    </div>
                `
            }
            
            elem_html = `
                <div class="input-area__item">
                    <div class="item__area"><span class="item__pc">+</span><label id="${item_key_refact}">${item_key}</label></div>
                    <div class="item__popup">
                        ${leg_el_html}
                    </div>
                </div>
            `
            result_html += elem_html
          }
        input_area.innerHTML = result_html
        lesten_items()
    });
}
generete_items()


