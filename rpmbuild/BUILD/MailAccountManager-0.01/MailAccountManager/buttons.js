function showAll(){
$("#report tr:not(.odd)").show();
}

function hideAll(){
$("#report tr:not(.odd)").hide();
}


function extractEmail(text){
  return text.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi);
}
function extractAcct(text){
  return text.match(/_(([a-zA-Z0-9]+))/gi);
}
function trimU(text){
  return text.replace("_", "");
}
function trimUb(text){
  return text.replace(/^[a-z]*_/, "");
}
function getMessage(text){
  text = text.match(/messages\\":\[(.*)\]/gi).toString();
  text = text.replace(/messages\\":\[|\"|\]|\\/g, "");
  return(text);
}
function getReason(text){
  text = text.match(/reason\\":(.*)\\"/gi).toString();
  text = text.replace(/reason\\":\\"|command|result|version|\":1|,|\"|\\|:|[a-z]+_[a-z]+_[a-z]+/g, "");
  return(text);
}

function getErrors(text){
  if ( text !== null ) {
  held = text.match(/errors\\":(null)/gi).toString();
 if ( held !== null ) { 
  
 var message = "No errors";

 return (message);

} else {
  return(text);
}
}
}


function getUrl(text, action){
$.get(text, function(data){
   console.log(data);
   var stringy = JSON.stringify(data);
   if ( stringy.indexOf("apiversion\\\":3")  >= 1  ) {
    if ( stringy.indexOf("messages\\\":null") >= 1 ) {
         var errors = getErrors(stringy);
         displayNotification(action + "\r\n" +  errors) ; 
   } else { 
   var testsa = getMessage(stringy);
   displayNotification(action + "\r\n" + testsa);
  }
} else if ( stringy.indexOf("version\\\":1")  >= 1 ) { 

   var testsa = getReason(stringy);
   displayNotification(action + "\r\n" + testsa);
}
}, 'json');
}






function updateStatusDiv(ele) {
  var id = ele.id;
  var url =  ele.href;

	if (id.indexOf("asuspout_") >= 0) { 
		var acct    = extractAcct(id).toString();
		var acctm   = trimU(acct);
		var action = "Suspend Outgoing for " + acctm + " returned:\n\n";
                var edivid  = "susp-" + acctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("SO:") <= 0 ) {
                    document.getElementById(edivid).innerHTML = "SO:&#x02A02;";

                 }
                getUrl(url, action);
	}
	else if (id.indexOf("unsuspout_") >= 0) { 
                var acct = extractAcct(id).toString();
                var acctm = trimU(acct);
                var action = "Unsuspend Outgoing for " + acctm + " returned:\n\n";
                var edivid  = "susp-" + acctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("SO:") >= 0 ) {
                    document.getElementById(edivid).innerHTML = "&nbsp;";
                      
                  }
                getUrl(url, action);
        }
	else if (id.indexOf("holdout_") >= 0) { 
                var acct = extractAcct(id).toString();
                var acctm = trimU(acct);
                var action = "Hold Outgoing for " + acctm + " returned:\n\n";
                var edivid  = "held-" + acctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("H:") <= 0 ) {

                   document.getElementById(edivid).innerHTML = "H:&#9888;";
                 }
                getUrl(url, action);
	}
	else if (id.indexOf("relout_") >= 0) { 
                var acct = extractAcct(id).toString();
                var acctm = trimU(acct);
                var action = "Release Outgoing for " + acctm + " returned:\n\n";
                var edivid  = "held-" + acctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("H:") >= 0 ) {
                    document.getElementById(edivid).innerHTML = "&nbsp;";

                 } 

                getUrl(url, action);
	} 
	else if (id.indexOf("msusin_") >= 0) { 
                var acct = extractEmail(id).toString();
                var macctm = trimUb(acct);
                var action = "Suspend Incoming for " + macctm + " returned:\n\n";
                var edivid  = "incsusp_" + macctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("SI:") <= 0 ) {
                   document.getElementById(edivid).innerHTML = "SI:&#x02A02;";
                 }
                getUrl(url, action);
	}
	else if (id.indexOf("munsusin_") >= 0) { 
                var acct = extractEmail(id).toString();
                var macctm = trimUb(acct);
                var action = "Unsuspended Incoming for " + macctm + " returned:\n\n";
                var edivid  = "incsusp_" + macctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("SI:") >= 0 ) {
                    document.getElementById(edivid).innerHTML = "&nbsp;";

                 } 
                getUrl(url, action);
        }
	else if (id.indexOf("amsusl_") >= 0) { 
                var acct = extractEmail(id).toString();
                var macctm = trimUb(acct);
                var action = "Suspend Logins for " + macctm + " returned:\n\n";
                var edivid  = "login_" + macctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("L:") <= 0 ) {
                    document.getElementById(edivid).innerHTML = "L:&#9888;";

                 } 
                getUrl(url, action);
        }
	else if (id.indexOf("munsusl_") >= 0) { 
                var acct = extractEmail(id).toString();
                var macctm = trimUb(acct);
                var action = "Unsuspending Login for " + macctm + " returned:\n\n";
                var edivid  = "login_" + macctm;
                var evar    = document.getElementById(edivid).innerHTML;
                 if ( evar.indexOf("L:") >= 0 ) {
                    document.getElementById(edivid).innerHTML = "&nbsp;";

		 } 
                getUrl(url, action);
	}
}




function displayNotification(text){
    document.getElementById('notifications').style.visibility = "visible";
    var ul = document.getElementById('notifications');
    var li = document.createElement("li");
    li.className = "popup";
    ul.appendChild(li);
    var ul = document.getElementById("notifications");
    li.appendChild(document.createTextNode(text));
    setTimeout(function(){ li.remove(); 
    if ( ul.childNodes.length === 0 ) {
         document.getElementById('notifications').style.visibility = "hidden";
   }
}, 7500);
}
