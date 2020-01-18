'use strict';

function set_contest(id, nameContest) {
    var el = document.getElementById(id);el.value = nameContest;
}

function regionChanged(value) {
    var district = document.getElementById('id_district');
    var city = document.getElementById('id_city');
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
    return url.searchParams.get(prm);
}

function setValueElementById(id, value) {
    var el = document.getElementById(id);
    el.value = value;
}

function setValueFIO(id, name) {
    var count_input = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 3;
    var btn = arguments[3];

    var el = document.getElementById(id);
    el.value = '';
    var elements = document.getElementsByName(name);
    var value = '';
    var step = 0;
    elements.forEach(function (item, i, arr) {

        if (item.value.toLowerCase() !== item.value.toUpperCase()) {
            var str = item.value.trim();
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
function setValueFIOmymoskvichi(id, name) {
    var count_input = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 3;
    var btn = arguments[3];


    var el = document.getElementById(id);
    var elements = document.getElementsByName(name);
    if (el.value && elements.length === 0) {
        return true;
    }

    var value = '';
    var step = 0;
    elements.forEach(function (item, i, arr) {

        if (item.value.toLowerCase() !== item.value.toUpperCase()) {
            var str = item.value.trim();
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
    var button = document.createElement('button');
    button.innerHTML = '&#10006';
    button.className = 'btn btn-sm btn-danger delete-button-block-fio';
    button.addEventListener('click', function () {
        el.remove();
    });
    el.appendChild(button);
}

function addBlockFio(parent, child) {
    addButton(child);
    child.querySelectorAll('input').forEach(function (item, i) {
        item.value = '';
        if (item.lastChild) {
            item.value += ',';
        }
    });
    parent.appendChild(child);
}