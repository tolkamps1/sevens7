function querySt(name) {
    queryString = window.location.search.substring(1);
    queryParams = queryString.split("&");
    for (i = 0; i < queryParams.length; i++) {
        paramName = queryParams[i].split("=");
        if (paramName[0] == name) {
            return paramName[1];
        }
    }
}
var user_id = querySt("user_id");
if (!!user_id) {
    document.getElementsByName('user_id')[0].value = user_id;
}