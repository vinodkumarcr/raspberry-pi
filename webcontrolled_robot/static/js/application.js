
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    
    //receive details from server
    socket.on('newnumber', function(msg){
        $('#Status').html(msg.number[0]);
        $('#loc').html(msg.number[1]);
        
    });

});