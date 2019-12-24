function regionChanged(value) {
    district = document.getElementById('id_district');
    city = document.getElementById('id_city');
    if (value === '77') {
        district.style.display = 'block';
        city.value = 'г. Москва';
        city.setAttribute('type', 'hidden');
    } else {
        district.style.display = 'none';
        city.setAttribute('type', 'text');
        city.value = '';
    }


}

function getParameterUrl(prm) {
    url = new URL(document.location.href);
    return url.searchParams.get(prm)
}

function setValueElementById(id, value) {
    let el = document.getElementById(id);
    el.value = value;


}

function setValueFIO(id, name, count_input = 3, btn) {
    let el = document.getElementById(id);
    el.value = '';
    let elements = document.getElementsByName(name);
    let value = '';
    let step = 0;
    elements.forEach(function (item, i, arr) {

        if (item.value.toLowerCase() !== item.value.toUpperCase()) {
            let str = item.value.trim();
            str = str[0].toUpperCase() + str.substring(1).toLowerCase();

            if (step === count_input) {

                value += ', ' + str;
                step = 0;
            } else {
                value += ' ' + str;
            }
            step++;
        }

    });

    if (el.value && el.value !== value) {
        el.value += ',';
        el.value += value;

    } else {
        el.value = value;

    }

}

function addButton(el) {
    let button = document.createElement('button');
    button.innerHTML = '&#10006';
    button.className = 'btn btn-sm btn-danger delete-button-block-fio';
    button.addEventListener('click', function () {
        el.remove()
    });
    el.appendChild(button);
}

function addBlockFio(parent, child,) {
    addButton(child);
    child.querySelectorAll('input').forEach(function (item, i) {
        item.value = '';
        if (item.lastChild) {
            item.value += ','
        }
    });
    parent.appendChild(child);


}
