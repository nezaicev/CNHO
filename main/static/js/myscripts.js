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

function setValueFIO(id, name) {
    let elements = document.getElementsByName(name);
    let value = '';
    if (elements.childElementCount) {
        elements.forEach(function (item, i, arr) {
            if (item !== undefined) {
                let str = item.value.trim();
                str = str[0].toUpperCase() + str.substring(1).toLowerCase();
                if (((i) % 3) !== 0 || i === 0) {
                    value += ' ' + str;
                } else {
                    value += ', ' + str;
                }

            }

        });
    }
    let el = document.getElementById(id);
    console.log(el.value);
    el.value += value;

}

function addBlockFio(parent, child) {
    let button = document.createElement('button');
    button.innerHTML = '&#10006';
    button.className = 'btn btn-sm btn-danger delete-button-block-fio';
    button.addEventListener('click', function () {
        child.remove()
    });
    child.appendChild(button);
    child.querySelectorAll('input').forEach(function (item, i) {
        item.value = '';
        if (item.lastChild) {
            item.value += ','
        }
    });
    parent.appendChild(child);


}
