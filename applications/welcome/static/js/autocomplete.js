/* 
 * Open items:
 * 1.  Update the Jquery Post to full ajax call 
 *     (timeout and onerror, stop spinning)
 * 
 * 
 * 
 * 
 */


/* Adding array search functionality */
String.prototype.startsWith = function(str) 
  {
    return (this.match("^"+str)==str)
  }

Array.prototype.beginsWith = function(searchStr) {
  var returnArray = false;
  for (i=0; i<this.length; i++) {
    if (this[i].startsWith(searchStr)){
      if (returnArray == false){
        returnArray = new Array();
      }
      returnArray.push(this[i]);
    }
  }
  return returnArray;
}

/* AutoComplete Class */
function AutoComplete() {
  var self = this;
  
  this.typingDelay = 300; //milliseconds
  this.cacheData = new Array();
  this.filtered;
  this.currentSearchLength = 0;
  this.cachingInProgress = false;
  this.ajaxCallCount = 0; 
  this.noResultsPoint = 0; 
  this.partialsearch = ""; 
  this.stage = 0;

  this.onkeypress = function (partialsearch,e) {
    c = String.fromCharCode(e.keyCode);
    this.partialsearch = partialsearch;
    if (this.currentSearchLength == 0){
      
      if (e.KeyCode || 40){
        //down
        this.stage = (this.stage + 1) % 4;
        $("#select0").hover(function() {alert(1);});
      }
      if (e.KeyCode == 38){ 
        //up
        this.stage = (this.stage - 1) % 4;
      }
    }
    
    this.execute(true);
  } 

  this.execute = function(initial) {
    this.ajaxCallCount = this.ajaxCallCount + 1;
    //Callback function (used later)
    callback = function (x,y) { 
                    return function () {
                         self.updateCache(x,y);
                    };
                };
    
    if (this.partialsearch == "") {
      //clear results
      $('#searchtextgrey').val("");    
      this.clearResults();    
    }
    else { 
     //if (c.match(/\w/)){
       
      if (this.cacheData.length > 0){
        //search
        this.filtered = this.cacheData.beginsWith(this.partialsearch.toLowerCase());
       
        if (this.filtered.length > 0){
          //found match, display results
          this.displayResults();
        }
        else {
          if (initial){
            $('#searchtextgrey').val("");
            this.clearResults();
            $('#searchtext').css('background-image',"url('../static/images/ajax-loader.gif')");
            setTimeout(callback(this.partialsearch, this.ajaxCallCount), this.typingDelay);
          }
        }
      }
      else {
        if (initial){
          $('#searchtextgrey').val("");
          this.clearResults();
          $('#searchtext').css('background-image',"url('../static/images/ajax-loader.gif')");
          setTimeout(callback(this.partialsearch, this.ajaxCallCount), this.typingDelay);
        }
      }
    }
  }


  /* Callback Function */
  this.updateCache = function(partialsearch, callCount) {
    if (callCount == self.ajaxCallCount) {
      $.post("livesearch", { partialsearch: partialsearch },
        function(data){
          self.cacheUpdated(data);      
        }, "json");
      self.ajaxCallCount = 0;
    } 
  }

  this.cacheUpdated = function(data) {
    this.cacheData = data;
    $('#searchtext').css('background-image',"");
    //Display results in dropdown box
    this.execute(false);
  }
  
  this.displayResults = function() {
    $('#searchtextgrey').val(this.partialsearch + 
                             this.filtered[0].substring(this.partialsearch.length,500));
                             
                             
     //Display results in dropdown box
     html = "<table id=\"resultstable\">";
     for (i = 0; i < Math.min(4,this.filtered.length); i++){
       html = html + "<tr><td class=\"resultsrow\" id=\"select"+ i +"\">" + this.partialsearch + this.filtered[i].substring(this.partialsearch.length,500) + "</td></tr>";
       
     }
     html = html + "</table>";
    $('#searchresults').html(html);
    $('#searchresults').show();
    $(".resultsrow").click(
        function(){
          $('#searchtext').val($(this).text()).focus();
          $('#searchresults').hide();
          $('#searchtextgrey').val('');
         
        }
    );     
              
  }
  
  this.clearResults = function() {
    $('#searchresults').hide();
    $('#searchresults').html("");
  
  }
}

var ac = new AutoComplete(); //AutoComplete Instance

$(document).ready(function() {
      // put all your jQuery goodness in here.
      
      $("#searchtext").focus(); //kepress not supported by iphone
      $("#searchtext").keyup( function (e) {
          ac.onkeypress($(this).val(),e);
        }
      );
   }
);