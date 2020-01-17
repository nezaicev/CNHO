function clearSearchBar(id){
    let el=document.getElementById(id);
    el.value='';

}
document.addEventListener("DOMContentLoaded",clearSearchBar('searchbar'));
