 var calendar = null;
 function calSelected(cal, date) {
   cal.sel.value = date;

   var updateFlexElements = document.getElementsByName('updateF' + cal.sel.name.substring(1));
   if ((typeof updateFlexElements != "undefined") && (updateFlexElements.length > 0)) {
		var elem = updateFlexElements[0];
		if (elem.type == "checkbox") {
		   elem.checked = true;
		}
	 }
	cal.callCloseHandler();
 } // calSelected

 function calCloseHandler(cal) {
  cal.hide();
 } // calCloseHandler

 function calShow(id) {
   var el = document.getElementById(id);
   if (calendar != null) {
     calendar.hide();		// hide the existing calendar
     calendar.parseDate(el.value); // set it to a new date
   } else {
     var cal = new Calendar(false, null, calSelected, calCloseHandler);
     var now = new Date();
     calendar = cal;
     //calendar.setDateFormat('mm/dd/y');
     calendar.setDateFormat('y-mm-dd');
     calendar.setRange(now.getFullYear() - 50, now.getFullYear() + 50);
     calendar.weekNumbers = false;
     calendar.create();
   }
   calendar.sel = el;
   calendar.showAtElement(el);
   //calendar.addEvent(document, "mousedown", checkCalendar);
   return false;
 } // calShow