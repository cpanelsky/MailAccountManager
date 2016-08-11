function idsmatch(text, match){
 var regex = new RegExp( match, 'g' ) ;
 return text.match(match) ;
}



function trimsuu(text){
 return text.replace(/_s___/, "");
}



function includesv(texts) {
  if  ( holderarray.indexOf(texts) >= 1 ) {
    return "1";
  } else {
      return "0";
    }
}


var holderarray = []



function hideList(){
      document.getElementById('ourul').style.visibility = "hidden";

}



function morecleaning(itedit){
           if ( itedit !== null && itedit !== undefined ) {
          itedit = itedit;
           holderarray = holderarray.filter(function(s){
           return ~s.indexOf(itedit);
           });
  }
}



function showList() {
   var txtValue = document.getElementById("searchinput").value;
      if ( txtValue.length >= 3 ) {
      document.getElementById('ourul').style.visibility = "visible";

   Array.prototype.forEach.call( ids, function( el, i ) {
      if ( el.id.indexOf("_s___") >= 0 )  {
      var it =  idsmatch(el.id, txtValue);
      var itedit = trimsuu(el.id);
       if ( it  ) {
          if ( el.id  ) {
          var arraycontains = includesv(itedit) ;
           holderarray = holderarray.filter(function(s){
           return ~s.indexOf(itedit);
           });

          if ( arraycontains === "0" ) {
	  var ul = document.getElementById("ourul");
	  var li = document.createElement("li");
          var ahreft = "#_s___" + itedit ;
          var lihrefId = "_sxhr___" + itedit ; 
          var safetyelement = document.getElementById(lihrefId);
          if ( safetyelement !== null ) {
          safetyelement.parentNode.removeChild(safetyelement);
           }
          li.className = "upside";
          li.id = lihrefId
          li.setAttribute('onClick', 'scrolltoxhref(this)');
          ul.appendChild(li);
          li.appendChild(document.createTextNode(itedit));
          holderarray.push(itedit);
          pruneArray();
           holderarray = holderarray.filter(function(s){
           return ~s.indexOf(itedit);
           });
          morecleaning(itedit);
           }
                            } 
	 		 }
                      }
	        });
         }
	  else if ( txtValue.length <= 1 ) {
           Array.prototype.forEach.call( ids, function( el, i ) {
           if ( el.id !== undefined  ) {
             document.getElementById('ourul').style.visibility = "hidden";
	     var empty = document.getElementsByClassName('upside');
		while(empty[0]) {
		    empty[0].parentNode.removeChild(empty[0]);
		}
          }
      });
   }
}



var searchelement = document.getElementById("searchinput")
   if (searchelement) {
      searchelement.addEventListener( "keyup", showList );
}



function pruneArray(){
    var duplicateChk = {};
    $('ul[id]').each (function () {
    if (duplicateChk.hasOwnProperty(this.id)) {
       $(this).remove();
    } else {
       duplicateChk[this.id] = 'true';
   		 }
	});
}



function scrolltoxhref(text) {
    var target = text.id.toString() ;
    target = trimsxhr(target)
        var element = document.getElementById(target);
        target = document.getElementById(target);
        var targstring = target.toString();
        target.scrollIntoView();
        target.click();
        var targets = getParents(target);
        target.scrollIntoView();

}



function trimsxhr(text){
 return text.replace(/_sxhr___/, "_s___");
}



function getParents(id) {
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

