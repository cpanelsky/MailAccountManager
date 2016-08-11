function scrolltoxhref(text) {
    var target = text.id.toString() ;
    target = trimsxhr(target)
        var element = document.getElementById(target);
	target = document.getElementById(target);
        var targets = GetParents(target);
	target.scrollIntoView();
}

function trimsxhr(text){
 return text.replace(/_sxhr___/, "_s___");
}

function GetParents(id) {
    var parents = $(id).parents();
        for(var i = 0; i < parents.length; i++){
        var checkvar = parents[i]; 
            if ( checkvar !== undefined && checkvar !== null ) {
            checkvar = checkvar.nodeName.toString();
                if ( checkvar !== undefined && checkvar !== null ) {
                    if ( checkvar.toString() == "TR" ){
                    parents[i].style.display = "table-row";
				}
			}
		}
	}
}
