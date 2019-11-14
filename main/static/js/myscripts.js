



function regionChanged(value) {
        district=document.getElementById('id_district');
        city=document.getElementById('id_city');
        if (value==='77'){
            district.style.display='block';
            city.value='г. Москва';
            city.setAttribute('type','hidden');}
        else{
            district.style.display='none';
            city.setAttribute('type','text');
            city.value='';
        }


    }

    function getParameterUrl(prm) {
        url=new URL(document.location.href);
        return url.searchParams.get(prm)
    }

    function setValueElementById(id,value) {
        let el=document.getElementById(id);
        el.value=value;


    }
    function setValueFIO(id,name){
        let elements=document.getElementsByName(name);
        let value='';
        elements.forEach(function (item,i,arr) {
            if (item!==undefined){
                let str=item.value.trim();
                str = str[0].toUpperCase() + str.substring(1).toLowerCase();
                value+=' '+str;
            }
        });
        let el=document.getElementById(id);
        el.value=value;

    }

