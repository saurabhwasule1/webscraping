	var mbNps = {
		host : document.domain,
		provider : "https://nps.magicbricks.com",
		source : "35703",
		npsLocation : '',
		contactData : '',
		htmlLocation : '',
		comm_n : '',
		comm_e : '',
		comm_m : '',
		comm_mc : '',
		isFrame : false,
		init : function() {
			//alert('widget');
			if (mbNps.showWidget()) {
				if (!window.jQuery) {
					var script = document.createElement('script');
					script.type = "text/javascript";
					script.src = "https://cdn.staticmb.com/scripts/jquery-1.7.2.min.js";
					document.getElementsByTagName('head')[0].appendChild(script);
				}
				var contactLocalData = "{\"uMob\":"+mbNps.comm_m+",\"uNam\":\""+mbNps.comm_n+"\",\"uEmail\":\""+mbNps.comm_e+"\"";
				mbNps.contactData = contactLocalData + ",\"uMobIsd\":\""+mbNps.comm_mc+"\",\"source\":\""+mbNps.source+"\"}";
				this.getNpsWidget();
				this.createCookie('mbNps','Y',15);

			}
		},
		getNpsWidget : function() {
			var urlStrContact = this.provider + "/nps/feedbackUser"; 
			$.ajax({
				dataType : "json",
				contentType: "application/json; charset=utf-8",
				type : "POST",
				data: mbNps.contactData,
				url : urlStrContact,
				crossDomain:true,
				cache : false,
				async : false,
				success : function(data, textStatus, request) {
					mbNps.npsLocation = data['Location']+"";
				}
			});
			var urlStr = this.provider + "/nps/feedback?code="+mbNps.source;
			$.ajax({
				dataType : "html",
				type : "GET",
				url : urlStr,
				crossDomain:true,
				cache : true,
				async : true,
				success : function(obj) {
					if(mbNps.isFrame){
						// window.parent.document.getElementById(mbNps.htmlLocation).innerHTML = obj+"";
						// alert("fram1");
						$('#'+mbNps.htmlLocation, window.parent.document).html(obj);
						 if(mbNps.comm_n!=''){
								$('#successName', window.parent.document).html(mbNps.comm_n+",");
                          }
                         if($("#npsSidePopWrap", window.parent.document).length > 0){
							 setTimeout(function(){
								$("#npsSidePopWrap", window.parent.document).addClass("open");
								$(".bgNpsLayer", window.parent.document).css("display","block");
							}, 2000);
						 }

					} else {
						$('#'+mbNps.htmlLocation).html(obj);
						if(mbNps.comm_n!=''){
							$('#successName').html(mbNps.comm_n+",");
						}
						if($("#npsSidePopWrap").length > 0)
							setTimeout(function(){jqNpsSlideOpen("npsSidePopWrap");}, 5000);
					}
				}
			});
				
		},
		getLocation : function(){
			//alert(mbNps.npsLocation+'ghghgh');
			return mbNps.npsLocation;
		},
		showWidget : function() {
			var val = this.readCookie("mbNps");
			var randomNum = Math.floor((Math.random() * 10) + 1);
			// 30 % user check
			//alert(randomNum < 4);
			if (val == null) {
				return true;
			}
			return false;
		},
		createCookie : function(name, value, days) {
			var expires = "";
			if (days) {
				var date = new Date();
				date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
				expires = "; expires=" + date.toGMTString();
			}
			document.cookie = name + "=" + value + expires + "; domain=.magicbricks.com; path=/";
		},
		readCookie : function(name) {
			var ca = document.cookie.split(';');
			var nameEQ = name + "=";
			for (var i = 0; i < ca.length; i++) {
				var c = ca[i];
				while (c.charAt(0) == ' ')
					c = c.substring(1, c.length); //delete spaces
				if (c.indexOf(nameEQ) == 0) {

					retVal = c.substring(nameEQ.length, c.length);

					return retVal;
				}
			}
			return null;
		}
	};

function readCookieContactDetails(name) {
	var ca = document.cookie.split(';');
	var nameEQ = name + "=";
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ')
			c = c.substring(1, c.length); //delete spaces
		if (c.indexOf(nameEQ) == 0) {
			retVal = c.substring(nameEQ.length, c.length);
			if (name == 'userType' && retVal.indexOf(",") > 0)
				return retVal.substring(0, retVal.indexOf(","));
			else if (name == 'userEmail') {
				return retVal.replace(/^"(.\*)"$/, '$1');
			} else if (name == 'userName') {
				return retVal.replace(/^"(.\*)"$/, '$1');
			} else
				return retVal;
		}
	}
	return null;
}


$("body").on("click", "input[name='npsRating']",function(){
	$(".npsBtnContinue a").addClass("continue");
})
